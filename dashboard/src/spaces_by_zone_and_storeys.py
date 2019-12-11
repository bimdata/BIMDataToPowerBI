#!/usr/bin/env python3.7

import pandas as pd
import bimdata_api_client
import requests

"""
    GetSpaces class
    Constructor parameters:
        dataset: 
            This is the Power BI global variable that contains a pandas.DataFrame with the datas of the previous step into the request.
            It"s used to get the parameters in Power BI, namely : Access Token, cloud ID, project ID, IFC ID
            It can be None in the case where we are executing these scripts directly from a terminal. So we load the parameters from a .env file
            with keys: TOKEN, CLOUD_ID, PROJECT_ID, IFC_ID
"""

class GetSpaces:
    def __init__(self, dataset=None, **kwargs):
        self.access_token = dataset["access_token"][0]
        self.cloud_pk = str(dataset["cloud_id"][0])
        self.project_pk = str(dataset["project_id"][0])
        self.ifc_pks = str(dataset["ifc_id"][0]).split(",")
        self.api_url = str(dataset["api_url"][0]) 

        self.space_UUIDs = []
        self.storey_UUIDs = []
        self.parent_zone_uuids = []
        self.zone_uuids = []
        self.spaces = {
            # UUID: {
            #     storey_uuid
            #     zone_uuid
            #     parent_zone_uuid
            # }
        }

    def config(self):
        configuration = bimdata_api_client.Configuration()
        configuration.access_token = self.access_token
        configuration.host = self.api_url
        return configuration

    def recursive_parse_structure(self, structure, storey=None):
        for elem in structure:
            if elem['type'] in ['project', 'building', 'site']:
                # Not useful in this context, going deeper
                self.recursive_parse_structure(elem['children'], storey=storey)
            elif elem['type'] == 'storey':
                self.recursive_parse_structure(elem['children'], storey=elem['uuid'])
            elif storey and elem['type'] == 'space':
                uuid = elem['uuid']
                if uuid not in self.spaces:
                    self.spaces[uuid] = {}
                self.spaces[uuid]["storey_uuid"] = storey
  
    def recursive_parse_zones(self, zones, parent_zone_uuid=None):
        for zone in zones:
            self.recursive_parse_zones(zone.zones, parent_zone_uuid=zone.uuid)
            for space in zone.spaces:
                if space.uuid not in self.spaces:
                    self.spaces[space.uuid] = {}
                self.spaces[space.uuid]["parent_zone_uuid"] = parent_zone_uuid
                self.spaces[space.uuid]["zone_uuid"] = zone.uuid


    def run(self):
        configuration = self.config()
        ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))

        for ifc_pk in self.ifc_pks:
            ifc = ifc_api.get_ifc(self.cloud_pk, ifc_pk, self.project_pk)
            structure_response = requests.get(ifc.structure_file)
            structure_response.raise_for_status()
            structure = structure_response.json()
            self.recursive_parse_structure(structure)
            zones = ifc_api.get_zones(self.cloud_pk, ifc_pk, self.project_pk)
            self.recursive_parse_zones(zones)
        data = {
            "space_UUID": [],
            "parent_zone_UUID": [],
            "zone_UUID": [],
            "storey_UUID": [],
        }
        for space_uuid, parents in self.spaces.items():
            data['space_UUID'].append(space_uuid)
            data['parent_zone_UUID'].append(parents.get("parent_zone_uuid"))
            data['zone_UUID'].append(parents.get("zone_uuid"))
            data['storey_UUID'].append(parents.get("storey_uuid"))

        self.df = pd.DataFrame(data)
        return self.df

if __name__ == "__main__":
    BIMData_info = GetSpaces(dataset=dataset).run()
    del dataset
