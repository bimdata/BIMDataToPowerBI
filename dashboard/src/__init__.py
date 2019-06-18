#!/usr/bin/env python3.7

from sty import fg
from get_elements import GetElements
import sys

def print_begin(function):
    print('{}Getting {} from API... {}'.format(fg(10, 255, 10), function.__name__.split('_')[2], fg.rs))

def print_end(function):
    print('{}Finished get {}'.format(fg(10, 255, 10), ' '.join(function.__name__.split('_')[2:])))
    print('=============={}'.format(fg.rs))

def get_ifc_doors(debug_type, excludes=[]):
    get_elements_doors = GetElements(ifc_type='IfcDoor', debug=debug_type, properties_options={'excludes': excludes})
    print_begin(get_ifc_doors)
    Elements = get_elements_doors.run()
    print_end(get_ifc_doors)

def get_ifc_railling(debug_type, excludes=[]):
    get_elements_railling = GetElements(ifc_type='IfcRailling', debug=debug_type, properties_options={'excludes': excludes})
    print_begin(get_ifc_railling)
    Elements = get_elements_railling.run()
    print_end(get_ifc_railling)
    print("Finished get railling")

def get_ifc_roof(debug_type, excludes=[]):
    get_elements_roof = GetElements(ifc_type='IfcRoof', debug=debug_type, properties_options={'excludes': excludes})
    print_begin(get_ifc_roof)
    Elements = get_elements_roof.run()
    print_end(get_ifc_roof)

def get_ifc_slab(debug_type, excludes=[]):
    get_elements_slab = GetElements(ifc_type='IfcSlab', debug=debug_type, properties_options={'excludes': excludes})
    print_begin(get_ifc_slab)
    Elements = get_elements_slab.run()
    print_end(get_ifc_slab)

def get_ifc_wall(debug_type, excludes=[]):
    get_elements_wall = GetElements(ifc_type='IfcWall', debug=debug_type, properties_options={'excludes': excludes})
    print_begin(get_ifc_wall)
    Elements = get_elements_wall.run()
    print_end(get_ifc_wall)

def get_ifc_wall_standard_case(debug_type, excludes=[]):
    get_elements_wall_standard_case = GetElements(ifc_type='IfcWallStandardCase', debug=debug_type, properties_options={'excludes': excludes})
    print_begin(get_ifc_wall_standard_case)
    Elements = get_elements_wall_standard_case.run()
    print_end(get_ifc_wall_standard_case)

if __name__ == '__main__':
    debug_type = sys.argv[1] if len(sys.argv) == 2 else 'nodebug'
    get_ifc_doors(debug_type)
    get_ifc_railling(debug_type)
    get_ifc_roof(debug_type)
    get_ifc_slab(debug_type)
    get_ifc_wall(debug_type, ['Width'])
    get_ifc_wall_standard_case(debug_type)