#!/usr/bin/env python3.7

from get_elements import GetElements
import sys
import argparse
from datetime import datetime
import os

ifcTypes = [
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
    'IfcZone'
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="enable debug messages, soft will give you the length of the retrieved datas, hard will print everything", choices=['soft', 'hard'])
    parser.add_argument('-e', '--export', help="enable CSV export", action="store_true")
    parser.add_argument('-t', '--type', help="Select a specific type", choices=['IfcBeam', 'IfcBuildingStorey', 'IfcCurtainWall', 'IfcDoor', 'IfcPlate', 'IfcProject', 'IfcRailing', 'IfcRoof', 'IfcSite', 'IfcSlab', 'IfcSpace', 'IfcStair', 'IfcWall', 'IfcWallStandardCase', 'IfcWindow', 'IfcZone'])
    args = parser.parse_args()
    if args.debug != None:
        debug_type = args.debug
    else:
        debug_type = 'nodebug'

    now = datetime.now()
    path = f'./csv_export/{now.strftime("%d_%m_%y_%H-%M-%S")}'
    if not os.path.exists(path):
        os.makedirs(path)
    if args.type:
        Elements = GetElements(ifc_type=args.type, debug=debug_type, properties_options={'excludes': [], 'includes': []}).run()
    else:
        for ifcType in ifcTypes:
            Elements = GetElements(ifc_type=ifcType, debug=debug_type, properties_options={'excludes': [], 'includes': []}).run()
            if args.export:
                with open(f'{path}/{ifcType}.csv', 'a+') as f:
                    f.truncate(0)
                    f.write(Elements.to_csv()[1:])
