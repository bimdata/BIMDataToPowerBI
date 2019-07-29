#!/usr/bin/env python3.7

'''
    This script generates Python scripts based on get_elements.py file and replace IfcType by one the IfcType in the types list below.
    If you want to add an IfcType, just add it in the list.
'''

import re
import os

types = [
    'IfcBeam',
    'IfcBuildingStorey',
    'IfcCurtainWall',
    'IfcDoor',
    'IfcPlate',
    'IfcProject',
    'IfcRailing',
    'IfcRoof',
    'IfcSite',
    'IfcSlab',
    'IfcSpace',
    'IfcStair',
    'IfcWall',
    'IfcWallStandardCase',
    'IfcWindow',
    'IfcZone',
]

with open('./get_elements.py', 'r') as model:
    model_content = model.read()

path = './templates'
if not os.path.exists(path):
    os.makedirs(path)
for type in types:
    with open(f"{path}/get_{'_'.join(re.split('(?=[A-Z])', type)[1:]).lower()}s.py", 'w') as f:
        f.write(model_content.replace('IfcType', type))




