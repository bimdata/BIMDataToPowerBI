#!/usr/bin/env python3.7

import pandas as pd
import bimdata_api_client
import requests

"""
    GetStructure class
    Constructor parameters:
        dataset: 
            This is the Power BI global variable that contains a pandas.DataFrame with the datas of the previous step into the request.
            It"s used to get the parameters in Power BI, namely : Access Token, cloud ID, project ID, IFC ID
            It can be None in the case where we are executing these scripts directly from a terminal. So we load the parameters from a .env file
            with keys: TOKEN, CLOUD_ID, PROJECT_ID, IFC_ID
"""

class GetStructure:
    def __init__(self, dataset=None, **kwargs):
        self.access_token = dataset["access_token"][0]
        self.cloud_pk = str(dataset["cloud_id"][0])
        self.project_pk = str(dataset["project_id"][0])
        self.ifc_pks = str(dataset["ifc_id"][0]).split(",")
        self.api_url = str(dataset["api_url"][0]) 

        self.element_UUIDs = []
        self.space_UUIDs = []
        self.storey_UUIDs = []
        self.building_UUIDs = []
        self.site_UUIDs = []

    def config(self):
        configuration = bimdata_api_client.Configuration()
        configuration.access_token = self.access_token
        configuration.host = self.api_url
        return configuration

    def recursive_parse(self, structure, context=None):
        for elem in structure:
            if elem['type'] in ['project', 'site', 'building', 'storey', 'space']:
                # Not useful in this context, going deeper
                if not context:
                    context = {}
                context[elem['type']] = elem['uuid']
                self.recursive_parse(elem['children'], context=context)
            else:
                self.element_UUIDs.append(elem['uuid'])
                self.space_UUIDs.append(context.get('space', None))
                self.storey_UUIDs.append(context['storey'])
                self.building_UUIDs.append(context['building'])
                self.site_UUIDs.append(context['site'])

    def run(self):
        configuration = self.config()
        ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))

        for ifc_pk in self.ifc_pks:
            ifc = ifc_api.get_ifc(self.cloud_pk, ifc_pk, self.project_pk)
            structure_response = requests.get(ifc.structure_file)
            structure_response.raise_for_status()
            structure = structure_response.json()
            self.recursive_parse(structure)
        data = {
            "element_UUID": self.element_UUIDs,
            "space_UUID": self.space_UUIDs,
            "storey_UUID": self.storey_UUIDs,
            "building_UUID": self.building_UUIDs,
            "site_UUID": self.site_UUIDs,
        }
        self.df = pd.DataFrame(data)
        return self.df

if __name__ == "__main__":
    BIMData_info = GetStructure(dataset=dataset).run()
    del dataset