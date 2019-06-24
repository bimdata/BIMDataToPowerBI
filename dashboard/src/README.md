# Dashboard's scripts

## This folder

### One file to rules them all.

The `get_elements.py` script is used to retrieve elements from an IFC Model and format datas to make it compliants with Power BI.
It makes a GET request on `cloud/id/project/id/ifc/id/elements/raw`.
This script contains a class called `GetElements` where you can enters parameters in the constructors in order to configure what datas you want retrieve and how you want to format it.

You can test the class using the `__init__.py` script, that basically instanciates the GetElements class multiples times with differents parameters

For more informations about the class constructor parameters, you can directly check in the `get_elements.py` file.

### Execution context

In Power BI, the python script is executed using the `__name__` as `'__main__'`

## Templates folder

As maybe you know it, Power BI is doing Python scripts executing directly in Power Query language context, that means that we can't access to local files, and therefore, cannot use efficiently the OOP logic.
To make up for that, we've made a script, called `generate_templates.py` located in the `templates/` folder, that generates GetElements class files with IfcType pre-defined.
This script is basically taking the content of `get_elements.py` and copying it to a file named `get_ifc_type.py` in the `templates/` folder.
Like that, you just have to copy/paste the generated file to Power BI request transformation.
 
For more informations concerning `generate_templates.py`, I let you check directly into the file.