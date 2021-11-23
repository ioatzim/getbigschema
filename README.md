# getbigschema
POST DBMLs to bigschema.io app. Configure and create DBML files from databases, data flows and spreadsheets.

## Requirements
Requires Python 3.6 or above. ???

## Main features
getbigschema provides the following features:
* Generating dbml files, from existing databases and spreadsheets
* Generating dbml files, from existing manifest.json and catalog.json files that are produced with dbt methods
* Uploading dbml files to API
* Requesting dbml files from API

## Usage
Code can be executed in any Python interpreter/terminal or framework, including Jupyter, Conda, Pycharm, etc

## Examples

### 1. Turn SQL schemas and individual sheets to DBML
getbigschema can turn SQL schemas to dbml files. Most databases are supported. User must enter the database details in schema_to_dbml.py file in the following field. Database url/connection string rules can be found at https://docs.sqlalchemy.org/en/14/core/engines.html

```
databases = [
{'name': 'database_1', 'url': 'sqlite:///test.db'}
]
```

It also supports google spreadsheets. User must enter the google spreadsheet url in the following field:

```
google_sheets = [
{'name': 'Hospital Bed Utilization', 'url': "https://docs.google.com/spreadsheets/d/1I1S9WW4OEHaNpqebM0L5sumoElrmVBCXCTVItHNZdbs/edit?usp=sharing"}
]
```

Output includes one dbml file for each database and one additional dbml file for all the spreadsheets. 

*full code is included in file ``` schema_to_dbml.py ```*

### 2. Turn DBT output files to DBML
DBT (data build tool) enables analytics engineers to transform data in their warehouses by simply writing select statements. dbt handles turning these select statements into tables and views. Details of these tables and views are included in dbt-output files manifest.json and catalog.json. Getbigschema can read these files and produce dbml reports. An example of "manifest.json", "catalog.json" and "dbml_file" are shown below:

##### manifest.json example:
```
{"metadata": {...},
 "nodes":  {"basic.test_db.users": {...},            
 "sources":{"source.test_db.changes": {...},    
  ...,
 "parent_map": {"basic.test_db.users": ["source.test_db.changes"],
                "source.test_db.changes": []},
 "child_map":{"source.test_db.changes": ["basic.test_db.users"],
	      "basic.test_db.users": [] } }
```

##### catalog.json example:
```
{"metadata": {...},
 "nodes": {"basic.test_db.users": {...} },    
 "sources": {"source.test_db.changes": {...} },    
 "errors": null }
```

##### dbml_file example:
```
table "source.test_db.changes" [gridX: 0] {
   "eventid" NUMBER
   "event_type" TEXT
   Note: "BASE TABLE"
}

//ref_parents: []
//ref_children: ['basic.test_db.users']

table "basic.test_db.users" [gridX: 1] {
   "userid" NUMBER
   "name" TEXT
   "occupation" TEXT
   Note: "VIEW"
}

//ref_parents: ['source.test_db.changes']
//ref_children: []
```

Output also includes topological_sort.json, a file that includes all tables, with their gridX order. This order represents the stage that the table was created at, for example it is 0 for source tables, 1 for tables (or views) created based on source ones, 2 for tables (or views) created based on tables of order 0 and 1 etc. The      general rule is that each table has an order equal with the max order of its creators, plus 1  

##### topological_sort.json file example:
```
{"source.test_db.changes": 0, "basic.test_db.users": 1}
```

*full code is included in file ``` dbt_to_dbml.py ```*

### 3. Upload DBML files to bigschema.io app
We can upload dbml files to bigschema.io app, executing the file dbml_to_api.py
All we need is the API url and a folder with all dbml files to upload
When upload is completed, api returns a unique id per file.
All ids are save in the file "response_ids.json", in key-value pairs, as below:

##### response_ids.json file example:
```
{
"file_1.dbml": "6192b2c21c2a512293fea622",
"file_2.dbml": "6172a2c21f2b3a17793fqa342"
}
```

*full code is included in file ``` dbml_to_api.py ```*

### 4. Retrieve DBML files from bigschema.io app
Using the API url and the unique id of the file form previous step, we can retrieve the file from the API with the following 2 commands:

##### code th retrieve a dbml from api:
```
res = requests.get(f'{url}/{id}')
file = json.loads(res.json()['contents'])
```
*full code is included in file ``` dbml_from_api.py ```*

## Code of Conduct
All contributors are expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).
