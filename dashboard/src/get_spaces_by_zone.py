#!/usr/bin/env python3.7

import pandas as pd
import bimdata_api_client

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

        self.parent_zone_uuids = []
        self.zone_uuids = []
        self.space_uuids = []


    def config(self):
        configuration = bimdata_api_client.Configuration()
        configuration.access_token = self.access_token
        configuration.host = self.api_url
        return configuration

    def recursive_parse(self, zones, parent_zone_uuid=None):
        for zone in zones:
            self.recursive_parse(zone.zones, parent_zone_uuid=zone.uuid)
            for space in zone.spaces:
                self.parent_zone_uuids.append(parent_zone_uuid)
                self.zone_uuids.append(zone.uuid)
                self.space_uuids.append(space.uuid)

    def run(self):
        configuration = self.config()
        ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))

        for ifc_pk in self.ifc_pks:
            zones = ifc_api.get_zones(self.cloud_pk, ifc_pk, self.project_pk)
            self.recursive_parse(zones)
        data = {
            "parent_zone_UUID": self.parent_zone_uuids,
            "zone_UUID": self.zone_uuids,
            "space_UUID": self.space_uuids,
        }
        self.df = pd.DataFrame(data)
        return self.df

if __name__ == "__main__":
    get_spaces = GetSpaces(dataset=dataset)
    BIMData_info = get_spaces.run()
