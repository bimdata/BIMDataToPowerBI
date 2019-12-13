import json
import pandas as pd
import bimdata_api_client
    
def smart_cast(value):
    if value not in {"true", "false", None}:
        try:
            a = float(value)
            if a.is_integer() and "." not in value:
                return int(a)
            return a
        except ValueError:
            return value
    else:
        if value == "true":
            return True
        if value == "false":
            return False
        return None
    

class GetElements:
    def __init__(self, dataset, **kwargs):
        self.access_token = dataset["access_token"][0]
        self.cloud_pk = str(dataset["cloud_id"][0])
        self.project_pk = str(dataset["project_id"][0])
        self.ifc_pks = str(dataset["ifc_id"][0]).split(",")
        self.api_url = dataset["api_url"][0]
        self.ifc_type = str(dataset["ifc_type"][0])

        self.elements = []
        self.formatted_elements = {}
        self.all_properties = set()

    def config(self):
        configuration = bimdata_api_client.Configuration()
        configuration.access_token = self.access_token
        configuration.host = self.api_url
        return configuration

    def get_properties_from_elements(self):
        # Formating elements properties
        self.formatted_elements["UUID"] = []
        self.formatted_elements["TYPE"] = []
        for element in self.elements:
            self.formatted_elements["UUID"].append(element["uuid"])
            self.formatted_elements["TYPE"].append(element["type"])
            element["values"] = {}
            for pset in element["property_sets"]:
                for prop in pset["properties"]:
                    full_name = (pset["name"], prop["definition"]["name"])
                    self.all_properties.add(full_name)
                    element["values"][full_name] = prop["value"]
            for prop in element["attributes"]["properties"]:
                full_name = ("Attributes", prop["definition"]["name"])
                self.all_properties.add(full_name)
                element["values"][full_name] = smart_cast(prop["value"])

        sort_by_prop_name = sorted(self.all_properties, key=lambda name: name[1])
        sort_by_pset_name = sorted(sort_by_prop_name, key=lambda name: name[0])
        for full_name in sort_by_pset_name:
            self.formatted_elements[f"{full_name[0]}.{full_name[1]}"] = [element["values"].get(full_name, None) for element in self.elements]

    def raw_elements_to_elements(self, api_response):
        raw_elements = api_response.to_dict()

        for definition in raw_elements["definitions"]:
            definition["unit"] = raw_elements["units"][definition["unit_id"]] if definition["unit_id"] else None

        for pset in raw_elements["property_sets"]:
            for prop in pset["properties"]:
                prop["definition"] = raw_elements["definitions"][prop["def_id"]]

        for elem in raw_elements["elements"]:
            elem["attributes"] = raw_elements["property_sets"][elem["attributes"]]
            elem["property_sets"] = [raw_elements["property_sets"][pset_id] for pset_id in elem["psets"]]
            self.elements.append(elem)
        
    def detect_type(self, values):
        types = [str, float, int, bool]
        value_types = [type(value) for value in values]
        for python_type in types:
            if all(value == python_type for value in value_types if value_types != type(None)):
                return python_type
        
        return str 

        
    def force_types(self):
        for column, values in self.formatted_elements.items():
            print(column, self.detect_type(values))
            column_type = self.detect_type(values)
            self.df[column].astype(column_type)

    def run(self):
        configuration = self.config()
        ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))

        for ifc_pk in self.ifc_pks:
            api_response = ifc_api.get_raw_elements(self.cloud_pk, ifc_pk, self.project_pk, type=self.ifc_type)
            self.raw_elements_to_elements(api_response)
        
        self.get_properties_from_elements()
        self.df = pd.DataFrame(self.formatted_elements)
        self.force_types()
        return self.df

if __name__ == "__main__":
    BIMData_info = GetElements(dataset=dataset).run()
    del dataset
