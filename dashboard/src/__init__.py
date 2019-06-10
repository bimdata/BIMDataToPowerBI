from sty import fg
from get_elements import GetElements

def print_begin(function):
    print('{}Getting {} from API... {}'.format(fg(10, 255, 10), function.__name__.split('_')[2], fg.rs))

def print_end(function):
    print('{}Finished get {}'.format(fg(10, 255, 10), function.__name__.split('_')[2]))
    print('=============={}'.format(fg.rs))

def get_ifc_doors():
    get_elements_doors = GetElements(ifc_type='IfcDoor', debug='soft')
    print_begin(get_ifc_doors)
    Elements = get_elements_doors.run()
    print_end(get_ifc_doors)

def get_ifc_railling():
    get_elements_railling = GetElements(ifc_type='IfcRailling', debug='soft')
    print_begin(get_ifc_railling)
    Elements = get_elements_railling.run()
    print_end(get_ifc_railling)
    print("Finished get railling")

def get_ifc_roof():
    get_elements_roof = GetElements(ifc_type='IfcRoof', debug='soft')
    print_begin(get_ifc_roof)
    Elements = get_elements_roof.run()
    print_end(get_ifc_roof)

def get_ifc_slab():
    get_elements_slab = GetElements(ifc_type='IfcSlab', debug='soft')
    print_begin(get_ifc_slab)
    Elements = get_elements_slab.run()
    print_end(get_ifc_slab)

def get_ifc_wall():
    get_elements_wall = GetElements(ifc_type='IfcWall', debug='soft')
    print_begin(get_ifc_wall)
    Elements = get_elements_wall.run()
    print_end(get_ifc_wall)

def get_ifc_wall_standard_case():
    get_elements_wall_standard_case = GetElements(ifc_type='IfcWallStandardCase', debug='soft')
    print_begin(get_ifc_wall_standard_case)
    Elements = get_elements_wall_standard_case.run()
    print_end(get_ifc_wall_standard_case)

def yolo_hey_hi():
    pass

if __name__ == '__main__':
    get_ifc_doors()
    get_ifc_railling()
    get_ifc_roof()
    get_ifc_slab()
    get_ifc_wall()
    get_ifc_wall_standard_case()