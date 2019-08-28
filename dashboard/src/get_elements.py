#!/usr/bin/env python3.7

import pandas as pd
import bimdata_api_client
import sys
import json
import logging
from decimal import *
from collections import Counter
import time
import pprint
pp = pprint.PrettyPrinter(indent=2, width=120)

getcontext().prec = 6

'''
    GetElements class
    Constructor parameters:
        dataset: 
            This is the Power BI global variable that contains a pandas.DataFrame with the datas of the previous step into the request.
            It's used to get the parameters in Power BI, namely : Access Token, cloud ID, project ID and IFC ID
            It can be None in the case where we are executing these scripts directly from a terminal. So we load the parameters from a .env file
            with keys: TOKEN, CLOUD_ID, PROJECT_ID, IFC_ID
        ifc_type:
            This is a string variable that contains the IfcType.
            Examples: IfcDoor, IfcWall...
            If you don't pass this argument, it will return all the elements without filtering by IfcType.
        debug: 
            Used to define the behavior of the debug that will be applied.
            There are 3 strings that can be understood : 'hard', 'soft' and 'nodebug'
            hard: if you want to debug the whole datas
            soft: if you want to debug the len of array that are retrieved
            nodebug: if you don't want any debug
        properties_options:
            It's a dict with 2 lists in it with keys : excludes and includes.
            You can specify property names to exclude in the excludes list
            You can specify property names to ONLY includes in the includes list
            This is working with XOR logic, if there are elements in includes, excludes will not be considered
'''

def smart_cast(value):
    tests = [float, str, bool]
    if value in ['True', 'False']:
        return bool(value)
    if value.count('.') > 1 or value.upper().isupper():
        return str(value)
    for test in tests:
        try:
            return test(value)
        except ValueError:
            continue
    return value

class GetElements:
    def __init__(self, dataset=None, ifc_type=None, debug='nodebug', properties_options={'excludes': [], 'includes': []}, **kwargs):
        self.ifc_type = ifc_type
        self.debug = debug
        self.properties_options = properties_options
        self.elements = []
        self.flat_elements = {}
        self.properties = {}
        self.properties['name'] = []
        self.properties['pset'] = []
        self.chosen_host = 'staging'
        self.types_ref = {}
        self.hosts = {
            'staging': 'https://api-staging.bimdata.io',
            'next': 'https://api-next.bimdata.io',
            'beta': 'https://api-beta.bimdata.io'
        }
        if dataset is not None:
            self.access_token = dataset['access_token'][0]
            self.cloud_pk = str(dataset['cloud_id'][0])
            self.project_pk = str(dataset['project_id'][0])
            self.ifc_pks = str(dataset['ifc_id'][0]).split(',')
            self.host = str(dataset['host'][0])
        else:
            from dotenv import load_dotenv
            load_dotenv('.env')
            import os
            self.access_token = os.getenv('TOKEN')
            self.cloud_pk = os.getenv('CLOUD_ID')
            self.project_pk = os.getenv('PROJECT_ID')
            self.ifc_pks = os.getenv('IFC_ID').split(',')
            self.chosen_host = os.getenv('HOST')

    def config(self):
        configuration = bimdata_api_client.Configuration()
        configuration.access_token = self.access_token
        configuration.host = self.hosts[self.chosen_host]
        return configuration

    def debug_data(self, data, function_name='MISSING_FUNCTION_NAME'):
        if 'nodebug' in self.debug:
            return
        print('====== DEBUG IN {} ======'.format(function_name))
        if 'soft' in self.debug:
            print('Found {} elements in the {}'.format(len(data) - 2, type(data)))
        elif 'hard' in self.debug:
            pp.pprint(data)

    def get_all_properties_name(self):
        if len(self.properties_options['includes']) > 0:
            self.properties['name'] = self.properties_options['includes']
            return
        for element in self.elements:
            for pset in element['property_sets']:
                for prop in pset['properties']:
                    if prop['definition']['name'] not in self.properties['name'] and prop['definition']['name'] not in self.properties_options['excludes']:
                        self.properties['name'].append(prop['definition']['name'])
                        self.properties['pset'].append(pset['name'])

    def get_properties_from_elements(self):
        self.get_all_properties_name()
        for element in self.elements:
            element['properties'] = []
            for prop_name in self.properties['name']:
                prop = {'value': '', 'name': prop_name}
                element['properties'].append(prop)
        for element in self.elements:
            for pset in element['property_sets']:
                for prop in pset['properties']:
                    for prop_target in element['properties']:
                        if prop_target['name'] == prop['definition']['name']:
                            value = prop['value'] if prop['value'] not in ['', None] else ''
                            prop_target['value'] = value
                            index = self.properties['name'].index(prop_target['name'])
                            key = f"{self.properties['pset'][index]}.{prop_target['name']}"
                            if prop_target['name'] not in self.types_ref.keys():
                                 self.types_ref[key] = []
                            self.types_ref[key].append(type(value).__name__)

    def format_properties_for_power_bi(self):
        for k, prop_name in enumerate(self.properties['name']):
            if prop_name not in self.flat_elements:
                self.flat_elements[f"{self.properties['pset'][k]}.{prop_name}"] = []
        for element in self.elements:
            for prop in element['properties']:
                index = self.properties['name'].index(prop['name'])
                self.flat_elements[f"{self.properties['pset'][index]}.{prop['name']}"].append(prop['value'])

    def remove_useless_properties(self):
        max = len(self.flat_elements['UUID'])
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
            self.elements.append(elem)

    def define_column_types(self):
        for key in self.types_ref:
            c = Counter(self.types_ref[key])
            self.df = self.df.astype({key: c.most_common()[0][0]})

    def fill_void(self):
        for key in self.types_ref:
            for i, value in enumerate(self.flat_elements[key]):
                if value == '':
                    c = Counter(self.types_ref[key])
                    if c.most_common()[0][0] == 'float':
                        self.flat_elements[key][i] = 0.0

    def run(self):
        configuration = self.config()
        ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))
        start_time = time.time()

        try:
            for ifc_pk in self.ifc_pks:
                print(f'retrieving... {ifc_pk}')
                api_response = ifc_api.get_raw_elements(self.cloud_pk, ifc_pk, self.project_pk, type=self.ifc_type)
                self.raw_elements_to_elements(api_response)
                print(f'good for {ifc_pk}')
            self.flat_elements = {}
            self.flat_elements['UUID'] = [elem['uuid'] for elem in self.elements]
            self.flat_elements['TYPE'] = [elem['type'] for elem in self.elements]
            self.get_properties_from_elements()
            self.format_properties_for_power_bi()
            self.debug_data(self.flat_elements, sys._getframe().f_code.co_name)
            # self.fill_void() 
            self.df = pd.DataFrame(self.flat_elements)
            # self.define_column_types()
            print("--- %s seconds ---" % (time.time() - start_time))
            return self.df
        except:
            raise Exception("An error occured during data retrieving, try to refresh the token with the request BIMDataMicrosoftConnect.RefreshToken()")

if __name__ == '__main__':
    get_elements = GetElements(dataset=dataset, ifc_type='IfcType', properties_options={'excludes': [], 'includes': [], 'pset_name': True})
    IfcTypes = get_elements.run()