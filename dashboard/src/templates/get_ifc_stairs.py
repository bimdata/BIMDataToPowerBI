#!/usr/bin/env python3.7

import pandas as pd
import bimdata_api_client
import sys
import json
import logging

import pprint
pp = pprint.PrettyPrinter(indent=2, width=120)

class GetElements:
    def __init__(self, dataset=None, ifc_type=None, debug='nodebug', properties_options={'excludes': []}, **kwargs):
        self.ifc_type = ifc_type
        self.debug = debug
        self.properties_options = properties_options
        self.elements = {}
        self.flat_elements = {}
        self.property_names = []
        if dataset is not None:
            self.access_token = dataset['access_token'][0]
            self.cloud_pk = str(dataset['cloud_id'][0])
            self.project_pk = str(dataset['project_id'][0])
            self.ifc_pk = str(dataset['ifc_id'][0])
        else:
            with open('.env', 'r') as env:
                self.access_token = env.readline().strip()
                self.cloud_pk = env.readline().strip()
                self.project_pk = env.readline().strip()
                self.ifc_pk = env.readline().strip()

    def config(self):
        configuration = bimdata_api_client.Configuration()
        configuration.api_key['Authorization'] = self.access_token
        configuration.api_key_prefix['Authorization'] = 'Bearer'
        configuration.host = 'https://api-staging.bimdata.io'
        return configuration

    def debug_data(self, data, function_name='MISSING_FUNCTION_NAME'):
        if 'nodebug' in self.debug:
            return
        print('====== DEBUG IN {} ======'.format(function_name))
        if 'soft' in self.debug:
            print('Found {} elements in the'.format(len(data), type(data)))
        elif 'hard' in self.debug:
            pp.pprint(data)

    def get_all_properties_name(self):
        for element in self.elements:
            for pset in element['property_sets']:
                for prop in pset['properties']:
                    if prop['definition']['name'] not in self.property_names and prop['definition']['name'] not in self.properties_options['excludes']:
                        self.property_names.append(prop['definition']['name'])

    def get_properties_from_elements(self):
        self.get_all_properties_name()
        for element in self.elements:
            element['properties'] = []
            for prop_name in self.property_names:
                prop = {'value': '', 'name': prop_name}
                element['properties'].append(prop)
        for element in self.elements:
            for pset in element['property_sets']:
                for prop in pset['properties']:
                    for prop_target in element['properties']:
                        if prop_target['name'] == prop['definition']['name']:
                            prop_target['value'] = prop['value'] if prop['value'] not in ['', None] else ''

    def format_properties_for_power_bi(self):
        for prop_name in self.property_names:
            if prop_name not in self.flat_elements:
                self.flat_elements[prop_name] = []
        for element in self.elements:
            for prop in element['properties']:
                self.flat_elements[prop['name']].append(prop['value'])

    def remove_useless_properties(self):
        max = len(self.flat_elements['uuid'])
        list_of_key_to_delete = []
        for key in self.flat_elements.keys():
            if len(self.flat_elements[key]) > max:
                list_of_key_to_delete.append(key)
        for key_to_delete in list_of_key_to_delete:
            del self.flat_elements[key_to_delete]

    def equalize_properties(self):
        self.remove_useless_properties()

    def raw_elements_to_elements(self, api_response):
        raw_elements = api_response.to_dict()

        for definition in raw_elements['definitions']:
            definition['unit'] = raw_elements['units'][definition['unit_id']] if definition['unit_id'] else None
            del definition['unit_id']

        for pset in raw_elements['property_sets']:
            for prop in pset['properties']:
                prop['definition'] = raw_elements['definitions'][prop['def_id']]
                del prop['def_id']

        for elem in raw_elements['elements']:
            elem['attributes'] = raw_elements['property_sets'][elem['attributes']]
            elem['classifications'] = list(map(lambda class_id: raw_elements['classifications'][class_id], elem['classifications']))
            elem['property_sets'] = list(map(lambda pset_id: raw_elements['property_sets'][pset_id], elem['psets']))
            del elem['psets']
            self.elements[elem['uuid']] = elem

    def filter_by_types(self):
        if self.ifc_type:
            self.elements = [elem for elem in self.elements.values() if elem['type'] == self.ifc_type]
            return
        self.elements = [elem for elem in self.elements.values()]

    def run(self):
        configuration = self.config()
        ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))

        try:
            api_response = ifc_api.get_raw_elements(self.cloud_pk, self.ifc_pk, self.project_pk)
            self.raw_elements_to_elements(api_response)
            self.filter_by_types()
            self.flat_elements = {}
            self.flat_elements['uuid'] = [elem['uuid'] for elem in self.elements]
            self.flat_elements['type'] = [elem['type'] for elem in self.elements]
            self.get_properties_from_elements()
            self.format_properties_for_power_bi()
            self.debug_data(self.flat_elements, sys._getframe().f_code.co_name)
            return pd.DataFrame(self.flat_elements)
        except:
            raise Exception("An error occured during data retrieving, try to refresh the token with the request BIMDataMicrosoftConnect.RefreshToken()")

if __name__ == '__main__':
    get_elements = GetElements(dataset=dataset, ifc_type='IfcStair', properties_options={'excludes': []})
    IfcStairs = get_elements.run()