'''
    File name: get-elements-by-type-pie-chart.py
    Author: Benjamin Audet
    Date created: 10/05/2019
    Date last modified: 22/05/2019
    Python Version: 3.7
'''

import matplotlib.pyplot as plt
import pandas as pd
import bimdata_api_client

# This line will not work outside of Power BI since it's a variable exposed by Power BI only
df = pd.DataFrame(dataset.loc[:1, 'access_token'])
access_token = df.iloc[0][0]

def compute_elements_sum_by_type(api_response, elements_sum_by_type):
    raw_types = list(map(lambda x: x.type, api_response.elements))
    for raw_type in raw_types:
        if raw_type not in elements_sum_by_type.keys():
            elements_sum_by_type[raw_type] = 1
        else:
            elements_sum_by_type[raw_type] += 1

def render_pie_chart(elements_sum_by_type):
    fig1, ax1 = plt.subplots()
    ax1.pie(elements_sum_by_type.values(), labels=elements_sum_by_type.keys(), autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def config():
    # Configure API key authorization: Bearer
    configuration = bimdata_api_client.Configuration()
    configuration.api_key['Authorization'] = access_token
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    configuration.api_key_prefix['Authorization'] = 'Bearer'
    configuration.host = 'https://api-staging.bimdata.io'
    return configuration

def main():
    configuration = config()
    # create an instance of the API class
    ifc_api = bimdata_api_client.IfcApi(bimdata_api_client.ApiClient(configuration))
    cloud_pk = '305'
    project_pk = '403'
    ifc_pk = '803'

    api_response = ifc_api.get_raw_elements(cloud_pk, ifc_pk, project_pk)
    elements_sum_by_type = {}
    compute_elements_sum_by_type(api_response, elements_sum_by_type)
    render_pie_chart(elements_sum_by_type)
    print(elements_sum_by_type)

if __name__ == "__main__":
    main()