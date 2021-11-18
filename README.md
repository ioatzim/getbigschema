# getbigschema
Creation of dbml files from given databases and spreadsheets.
Upload dbmls to API

## Requirements
Requires Python 3.6 or above. ???

### Main features
The main features provided by getbigschema are:
* Generating dbml files, from existing databases and spreadsheets
* Generating dbml files, from existing manifest.json and catalog.json files that are produced with dbt methods
* Uploading dbml files to API
* Requesting dbml files from API

### Usage
Code can be executed in any Python interpreter/terminal or framework, including Jupyter, Conda, Pycharm, etc

### Examples


#### Example1: # DBT
DBT (data build tool) enables analytics engineers to transform data in their warehouses by simply writing select statements. dbt handles turning these select statements into tables and views. Details of these tables and views are included in dbt-output files manifest.json and catalog.json. Getbigschema can read these files and produce dbml reports. The dbml file looks like below:

###### dbml_file example
```
table "source.demo_dbt.events.generic_metrics_master" [gridX: 0] {
   "FEATURE_ID" NUMBER
   "NAME" TEXT
   Note: "BASE TABLE"
}

//ref_parents: []
//ref_children: ['model.demo_dbt.users']

table "model.demo_dbt.users" [gridX: 1] {
   "ACCOUNT_ID" NUMBER
   "NAME" TEXT
   "ACCOUNT_STATUS_ID" NUMBER
   "TAX_IDENTIFIER" TEXT
   "CREATED_AT" TIMESTAMP_NTZ
   Note: "VIEW"
}

//ref_parents: ['source.demo_dbt.events.generic_metrics_master']
//ref_children: []
```

#### Example2: # For SQL DBs (BigQuery, RedShift, etc.)
getbigschema can turn SQL schemas to dbml files. Most databases are supported. User must enter the database details in schema_to_dbml.py file in the folollowing field:

```databases = [
{'name': 'database_1', 'url': 'sqlite:///test.db'}
]```

It also supports google spreadsheets. User must enter the google spreadsheet url in the following field:

```google_sheets = [
{'name': 'Hospital Bed Utilization', 'url': "https://docs.google.com/spreadsheets/d/1I1S9WW4OEHaNpqebM0L5sumoElrmVBCXCTVItHNZdbs/edit?usp=sharing"}
]```

Output includes one dbml file for each database and one additional dbml file for all the spreadsheets. 

#### Example3: # POST to bigschema.io app
--> how to run "dbml2draw.py"



### Code of Conduct
All contributors are expected to follow the PyPA Code of Conduct.

----------------------------------------------


# Files:
1. schema_extract.py
   User must add databases (name and url) and google spreadsheets (name and url) manually, to databases = [...] and spreadsheets = [...] code lines (see more instructions in      comments inside the files)
   On execution, code creates one dbml file per database and one dbml file for all the spreadsheets.
   
2. parser.py
   Accepts one manifest.json and one catalog.json file as input (these files are created with dbt process)
   On execution, code creates one dbml file and one file named topological_sort.json which includes all tables, with their gridX order. This order represents the stage that        the table is created, eg it's 0 for source tables,1 for tables (or views) created based on source ones, 2 for tables (or views) created based on tables of order 1 etc. The      general rule is that each table has an order greater by 1, than the table (of all tables used for its creation) with max order 

3. dbml_post_to_api.py
   User must manually add a folder-path that contains dbml files. On execution, code uploads all dbml files from this folder to the API and creates a json file/dictionary that    contains filenames as keys and ids as values (eg "demo_full.dmbl": "6192b2c21c2a512293fea123"). An id can be used to get the associated file from the API, with the file        get_dbmlf_from_api.py
   
4. get_dmbl_from_api.py
   User must manually add the id of the dbml file (found in the 'response_ids.json' file generated from dbml_post_to_api.py). On execution, code returns the dbml file from the    api and assigns it to a variable called dbml_file
   
