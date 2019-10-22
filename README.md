# PowerBI examples using BIMData API

## What is this?

Several examples of things that you can do programmatically with Python requesting BIMData.io's data and exploit them in Power BI.

## Hierarchy

Examples are sorted in folders. Go in it to explore all magnificent things we have done!
All folders have their owns `.pbix` and `.py` allowing you to see the code side and the corresponding Power BI side.

## Pre-requisites

* [Power BI Desktop](https://powerbi.microsoft.com/fr-fr/desktop/)
* [Python >=3.7](https://www.python.org/downloads/release/python-373/)
* [BIMDataConnector](https://github.com/bimdata/BIMDataMicrosoftConnector)

> All `.pbix` files here depend on our data connector [BIMDataConnector](https://github.com/bimdata/BIMDataMicrosoftConnector)

## Installation

Once you have installed all the pre-requisites tools, *clone* the repository.
Then in the folder, type the following command-line (in PowerShell):
`$> python install.py`



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

### If you get a Python error saying you're credentials are invalid
You need to refresh your access to BIMData.io. To do so, click on "source" in the "applied steps" and a message inviting you to refresh your connection will appear.
Click on 'Login with another account' (Even if you don't change the account), then "login".
