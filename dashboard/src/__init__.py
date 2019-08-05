#!/usr/bin/env python3.7

from sty import fg
from get_elements import GetElements
import sys
import argparse
from datetime import datetime
import os

def print_begin(ifc_type):
    print('{}Begin GET {} from API... {}'.format(fg(10, 255, 10), ifc_type, fg.rs))

def print_end(ifc_type):
    print('{}Finished GET {}'.format(fg(10, 255, 10), ifc_type))

def get_ifc_beam(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcBeam'
    get_elements_beam = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_beam.run()
    print_end(ifc_type)
    return Elements

def get_ifc_building_storey(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcBuildingStorey'
    get_elements_building_storey = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_building_storey.run()
    print_end(ifc_type)
    return Elements

def get_ifc_curtain_wall(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcCurtainWall'
    get_elements_curtain_wall = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_curtain_wall.run()
    print_end(ifc_type)
    return Elements

def get_ifc_door(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcDoor'
    get_elements_door = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_door.run()
    print_end(ifc_type)
    return Elements

def get_ifc_plate(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcPlate'
    get_elements_plate = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_plate.run()
    print_end(ifc_type)
    return Elements

def get_ifc_project(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcProject'
    get_elements_project = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_project.run()
    print_end(ifc_type)
    return Elements

def get_ifc_railling(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcRailling'
    get_elements_railling = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_railling.run()
    print_end(ifc_type)
    return Elements
    print("Finished get railling")

def get_ifc_roof(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcRoof'
    get_elements_roof = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_roof.run()
    print_end(ifc_type)
    return Elements

def get_ifc_site(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcSite'
    get_elements_site = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_site.run()
    print_end(ifc_type)
    return Elements

def get_ifc_slab(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcSlab'
    get_elements_slab = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_slab.run()
    print_end(ifc_type)
    return Elements

def get_ifc_space(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcSpace'
    get_elements_space = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_space.run()
    print_end(ifc_type)
    return Elements

def get_ifc_stair(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcStair'
    get_elements_stair = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_stair.run()
    print_end(ifc_type)
    return Elements

def get_ifc_wall(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcWall'
    get_elements_wall = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_wall.run()
    print_end(ifc_type)
    return Elements

def get_ifc_wall_standard_case(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcWallStandardCase'
    get_elements_wall_standard_case = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_wall_standard_case.run()
    print_end(ifc_type)
    return Elements

def get_ifc_window(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcWindow'
    get_elements_window = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_window.run()
    print_end(ifc_type)
    return Elements

def get_ifc_zone(debug_type, excludes=[], includes=[]):
    ifc_type = 'IfcZone'
    get_elements_zone = GetElements(ifc_type=ifc_type, debug=debug_type, properties_options={'excludes': excludes, 'includes': includes})
    print_begin(ifc_type)
    Elements = get_elements_zone.run()
    print_end(ifc_type)
    return Elements

ifcTypes = {
    'IfcBeam': get_ifc_beam,
    'IfcBuildingStorey': get_ifc_building_storey,
    'IfcCurtainWall': get_ifc_curtain_wall,
    'IfcDoor': get_ifc_door,
    'IfcPlate': get_ifc_plate,
    'IfcProject': get_ifc_project,
    'IfcRailing': get_ifc_railling,
    'IfcRoof': get_ifc_roof,
    'IfcSite': get_ifc_site,
    'IfcSlab': get_ifc_slab,
    'IfcSpace': get_ifc_space,
    'IfcStair': get_ifc_stair,
    'IfcWall': get_ifc_wall,
    'IfcWallStandardCase': get_ifc_wall_standard_case,
    'IfcWindow': get_ifc_window,
    'IfcZone': get_ifc_zone,
}

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
        Elements = ifcTypes[args.type](debug_type)
    else:
        for ifcType in ifcTypes.keys():
            Elements = ifcTypes[ifcType](debug_type)
            if args.export:
                with open(f'{path}/{ifcType}.csv', 'a+') as f:
                    f.truncate(0)
                    f.write(Elements.to_csv()[1:])
