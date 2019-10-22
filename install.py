#!/usr/bin/env python3.7

import os
from os import environ, getcwd
getUser = lambda: environ["USERNAME"] if "C:" in getcwd() else environ["USER"]
user = getUser()

os.system('pip install -r requirements.txt')

import requests
res = requests.get('https://github.com/bimdata/BIMDataMicrosoftConnector/releases/download/2.1/BIMData.io.mez')
connector_source = res.content
path = f'C:\\Users\\{user}\\Documents\\Power BI Desktop\\Custom Connectors'
if not os.path.exists(path):
    os.makedirs(path)

with open(f'{path}\\BIMData.io.mez', 'ab') as f:
    f.write(connector_source)
