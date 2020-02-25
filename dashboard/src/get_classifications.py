#!/usr/bin/env python3.7

import pandas as pd
import bimdata_api_client

"""
    GetClassifications class
    Constructor parameters:
        dataset: 
            This is the Power BI global variable that contains a pandas.DataFrame with the datas of the previous step into the request.
            It"s used to get the parameters in Power BI, namely : Access Token, cloud ID, project ID, IFC ID
            It can be None in the case where we are executing these scripts directly from a terminal. So we load the parameters from a .env file
            with keys: TOKEN, CLOUD_ID, PROJECT_ID, IFC_ID
"""

class GetClassifications:
    def __init__(self, dataset=None, **kwargs):
        self.access_token = dataset["access_token"][0]
        self.cloud_pk = str(dataset["cloud_id"][0])
        self.project_pk = str(dataset["project_id"][0])
        self.ifc_pks = str(dataset["ifc_id"][0]).split(",")
        self.api_url = str(dataset["api_url"][0]) 

        self.element_UUIDs = []
        self.classification_names = []
        self.classification_notations = []
        self.classification_titles = []

    def config(self):
        configuration = bimdata_api_client.Configuration()
        configuration.access_token = self.access_token
        configuration.host = self.api_url
        return configuration

    def raw_elements_to_elements(self, classifications_relations):
        for relation in classifications_relations:
            self.element_UUIDs.append(relation.element_uuid)
            classification = self.classifications[relation.classification_id]
            self.classification_names.append(classification.name)
            self.classification_notations.append(classification.notation)
            self.classification_titles.append(classification.title)

    def run(self):
        configuration = self.config()
        ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))
        collaboration_api = bimdata_api_client.CollaborationApi(bimdata_api_client.ApiClient(configuration))

        classifications = collaboration_api.get_classifications(self.cloud_pk, self.project_pk)
        self.classifications = {classification.id: classification for classification in classifications}
        for ifc_pk in self.ifc_pks:
            classifications_relations = ifc_api.list_classification_element_relations(self.cloud_pk, ifc_pk, self.project_pk)
            self.raw_elements_to_elements(classifications_relations)
        data = {
            "element_UUID": self.element_UUIDs,
            "classification_name": self.classification_names,
            "classification_notation": self.classification_notations,
            "classification_title": self.classification_titles,
        }
        self.df = pd.DataFrame(data)
        return self.df

if __name__ == "__main__":
    get_classifications = GetClassifications(dataset=dataset)
    BIMData_info = get_classifications.run()
    del dataset
