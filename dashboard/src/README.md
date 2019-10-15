# Dashboard's scripts

## This folder

### One file to rules them all.

The `get_elements.py` script is used to retrieve elements from an IFC Model and format data to make it compliant with Power BI.
It makes a GET request on `cloud/id/project/id/ifc/id/elements/raw` (see https://developers.bimdata.io/api/index.html#operation--cloud--cloud_pk--project--project_pk--ifc--ifc_pk--element-raw-get).
This script contains a class called `GetElements` where you can enter parameters in the constructors to configure what data you want to retrieve and how you want to format their rendering.

You can test the class using the `__init__.py` script, that instantiates the `GetElements` class multiple times with different parameters.

For more information about the class constructor parameters, you can look into the `get_elements.py` file.

### Execution context

In Power BI, the python script is executed using the `__name__` as `'__main__'`

## Usage
Create 4 parameters:
 - cloudId
 - projectId
 - ifcId
 - apiUrl

ifcId can be a single value or many values split by a comma (eg: 1842,5871,12,456)

Data is retrieved by IfcType.

To get data from BIMData, create an empty Query then add:
`= Table.FromColumns({{cloudId}, {projectId}, {ifcId}, {BIMData.GetToken()}, {apiUrl}, {"IfcWallStandardCase"}}, {"cloud_id", "project_id", "ifc_id", "access_token", "api_url", "ifc_type"})`

replace Your_IFC_Type by the type you want (eg: IfcWall, IfcDoor or IfcWallStandardCase)

In the "transform" tab, click on "add a python script" and copy-paste the content of get_element.py.

## Troubleshooting

### If you get the error "information about a data source is required"
Go to "Source parameters", set both "BIMData" and "python" confidentiality level to "Public" then try again


### If numbers are seen as text and trying to force the type fails
Go to "file => options & parameters => options => Active file => region parameters => force to English (United-States)"

