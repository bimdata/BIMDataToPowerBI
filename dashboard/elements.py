# 'dataset' holds the input data for this script

import pandas as pd
import bimdata_api_client
import pprint

pp = pprint.PrettyPrinter(indent=2)

access_token = dataset.iloc[0, 0]
# access_token = '1f66d84cbfea4cdcb787124451f4b8b2'


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
        sorted_elements = {}
        sorted_elements['uuid'] = list(elements.keys())
        sorted_elements['type'] = [elem['type'] for elem in elements.values()]
        sorted_elements['classifications'] = [elem['classifications'][0]['description'] for elem in elements.values() if len(elem['classifications'])]
        return pd.DataFrame(sorted_elements)
    except:
        raise Exception("An error occured during data retrieving, try to refresh the token with the request BIMDataMicrosoftConnect.RefreshToken()")

sorted_elements = main()
