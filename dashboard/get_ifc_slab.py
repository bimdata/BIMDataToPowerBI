# 'dataset' holds the input data for this script


import pandas as pd
import bimdata_api_client

import pprint
pp = pprint.PrettyPrinter(indent=4)

# Access Token assignation depending of if we are in a software or in a standard developement
if 'dataset' in globals():
    access_token = dataset.iloc[0, 0]
else:
    access_token = '9864ee15dcbc4084a17c1e29f91fc725'

ifc_type = 'IfcSlab'

def config():
    # Configure API key authorization: Bearer
    configuration = bimdata_api_client.Configuration()
    configuration.api_key['Authorization'] = access_token
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    configuration.host = 'https://api-staging.bimdata.io'
    return configuration

def raw_elements_to_elements(api_response):
    elements = {}
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
        elements[elem['uuid']] = elem
    return elements

def main():
    configuration = config()
    ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))
    cloud_pk = '305'
    project_pk = '403'
    ifc_pk = '803'

    try:
        api_response = ifc_api.get_raw_elements(cloud_pk, ifc_pk, project_pk)
        elements = raw_elements_to_elements(api_response)
        filtered_elements_by_wall = [elem for elem in elements.values() if elem['type'] == ifc_type]
        pp.pprint(filtered_elements_by_wall)
        elements_uuid = [k for k, elem in elements.items() if elem['type'] == ifc_type]
        sorted_elements = {}
        sorted_elements['uuid'] = [elem['uuid'] for elem in filtered_elements_by_wall]
        sorted_elements['type'] = [elem['type'] for elem in filtered_elements_by_wall]
        return pd.DataFrame(sorted_elements)
    except:
        raise Exception("An error occured during data retrieving, try to refresh the token with the request BIMDataMicrosoftConnect.RefreshToken()")

IfcSlab = main()
