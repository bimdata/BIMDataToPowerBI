# Dashboard's scripts

## This folder

### One file to rules them all.

The `get_elements.py` script is used to retrieve elements from an IFC Model and format data to make it compliant with Power BI.
It makes a GET request on `cloud/id/project/id/ifc/id/elements/raw`.
This script contains a class called `GetElements` where you can enter parameters in the constructors to configure what data you want to retrieve and how you want to format their rendering.

You can test the class using the `__init__.py` script, that instantiates the `GetElements` class multiple times with different parameters.

For more information about the class constructor parameters, you can look into the `get_elements.py` file.

### Execution context

In Power BI, the python script is executed using the `__name__` as `'__main__'`

## Templates folder

As you may know, Power BI runs Python scripts by executing directly in Power Query language context. That means that we can't access to local files, and therefore, cannot use efficiently the OOP logic.
To make up for that, we've made a script, called `generate_templates.py` located in the `templates/` folder, that generates GetElements class files with IfcType pre-defined.
This script takes the content of `get_elements.py` and copies it to a file named `get_ifc_type.py` located in the `templates/` folder.
You have to copy/paste the generated file to Power BI request transformation.
It's that simple! 

For more information concerning `generate_templates.py`, I let you check directly into the file.