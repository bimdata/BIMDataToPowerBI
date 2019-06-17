#!/usr/bin/env python3.7

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
    'IfcZone'
]

with open('../get_elements.py', 'r') as model:
    model_content = model.read()

for type in types:
    with open('get_{}s.py'.format('_'.join(re.split('(?=[A-Z])', type)[1:]).lower()), 'w') as f:
        f.write(model_content.replace('IfcType', type))




