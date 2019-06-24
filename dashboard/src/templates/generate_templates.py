#!/usr/bin/env python3.7

'''
    This script generates Python scripts based on get_elements.py file and replace IfcType by one the IfcType in the types list below.
    If you want to add an IfcType, just add it in the list.
'''

import re

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
    'IfcStair',
    'IfcWall',
    'IfcWallStandardCase',
    'IfcWindow',
    'IfcZone',
    'IfcSpace'
]

with open('../get_elements.py', 'r') as model:
    model_content = model.read()

for type in types:
    with open('get_{}s.py'.format('_'.join(re.split('(?=[A-Z])', type)[1:]).lower()), 'w') as f:
        f.write(model_content.replace('IfcType', type))




