# getbigschema
Creation of dbml files from given databases and spreadsheets.
Upload dbmls to API

## Requirements
Requires Python 3.6 or above. ???

### Main features
getbigschema provides the following features:
* Generating dbml files, from existing databases and spreadsheets
* Generating dbml files, from existing manifest.json and catalog.json files that are produced with dbt methods
* Uploading dbml files to API
* Requesting dbml files from API

### Usage
Code can be executed in any Python interpreter/terminal or framework, including Jupyter, Conda, Pycharm, etc

### Examples


### 1. Turn DBT output files to DBML
DBT (data build tool) enables analytics engineers to transform data in their warehouses by simply writing select statements. dbt handles turning these select statements into tables and views. Details of these tables and views are included in dbt-output files manifest.json and catalog.json. Getbigschema can read these files and produce dbml reports. The dbml file looks like below:

##### manifest.json example:
```
{
    "metadata": {...},
    "nodes":
    {
        "model.demo_dbt.users":
        {"raw_sql": "select ...", "compiled": true, "resource_type": "model",
            "depends_on":
            {   "macros": [],
                "nodes":
                [   "source.demo_dbt.user",
                    "source.demo_dbt.invitation"]
            },
            "config": {...}, "database": "demo_dev",
            "schema": "demo", "fqn": ["demo_dbt", ""], "unique_id": "model.demo_dbt.users",
            "package_name": "demo_dbt", "root_path": "", "path": "all_users.sql",
            "original_file_path": "models/all_users.sql", "name": "all_users",
            "alias": "all_users", "checksum": {...}, "tags": [], "refs": [],
            "sources": [...], "description": "Select *all* entries in source `user` table",
            "columns":
            {   "user_id":
                {
                    "name": "user_id",
                    "description": "",
                    "meta":
                    {},
                    "data_type": null,
                    "quote": null,
                    "tags":
                    []
                }
            },
            "meta": {}, "docs": {"show": true}, "patch_path": "models/all.yml",
            "build_path": "", "deferred": false, "unrendered_config": {...},
            "compiled_sql": "", "extra_ctes_injected": true, "extra_ctes": [], "relation_name": ""
        }
    },            
    "sources":
    {
        "source.demo_dbt.events.generic_metrics_master":
        {   "fqn": [...], "database": "", "schema": "", "unique_id": "", "package_name": "",
            "root_path": "", "path": "", "original_file_path": "", "name": "", "source_name": "",
            "source_description": "", "loader": "", "identifier": "", "resource_type": "source",
            "quoting": {...}, "loaded_at_field": null, "freshness": {...}, "external": null,
            "description": "The \"Generic Metrics Master\" table of the respective target\n",
            "columns": {}, "meta": {}, "source_meta": {}, "tags": [], "config": {...},
            "patch_path": null, "unrendered_config": {}, "relation_name": ""
        }
    },    
    "macros":
    {
        "macro.demo_dbt.test": {...}
    },    
    "docs": {...},  
    "exposures": {},
    "selectors": {},
    "disabled": [],
    "parent_map":
    {
        "model.demo_dbt.users":
        [
            "source.demo_dbt.events.generic_metrics_master"
			
        ],
		"source.demo_dbt.events.generic_metrics_master":
		[]
    },
    "child_map":
    {
        "source.demo_dbt.events.generic_metrics_master":
        [
            "model.demo_dbt.users"
        ],
		"model.demo_dbt.users":
		[]
    }
	}
```

##### catalog.json example:
```
{
    "metadata": {...},
    "nodes":
    {
        "model.demo_dbt.users":
        {
            "metadata": {...},
            "columns":
            {
                "ACCOUNT_ID":
                {
                    "type": "NUMBER",
                    "index": 1,
                    "name": "ACCOUNT_ID",
                    "comment": null
                },
                "NAME": {...},
                "ACCOUNT_STATUS_ID": {...},
                "TAX_IDENTIFIER": {...},
                "CREATED_AT": {...}
            },
            "unique_id": "model.demo_dbt"
        }
    },    
    "sources":
    {
        "source.demo_dbt.events.generic_metrics_master":
        {
            "metadata": {...},
            "columns":
            {
                "FEATURE_ID":
                {
                    "type": "NUMBER",
                    "index": 1,
                    "name": "FEATURE_ID",
                    "comment": null
                },
                "NAME": {...}
            },
            "unique_id": "source.demo_dbt"
        }
    },    
    "errors": null
}
```

##### dbml_file example:
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

Output also includes topological_sort.json, a file that includes all tables, with their gridX order. This order represents the stage that the table was created at, for example it is 0 for source tables, 1 for tables (or views) created based on source ones, 2 for tables (or views) created based on tables of order 0 and 1 etc. The      general rule is that each table has an order equal with the max order of its creators, plus 1  

##### topological_sort.json file example:
```
{"source.demo_dbt.events.generic_metrics_master": 0, "model.demo_dbt.users": 1}
```

*full code is included in file ``` dbt_to_dbml.py ```*

### 2. Turn SQL schemas and individual sheets to DBML
getbigschema can turn SQL schemas to dbml files. Most databases are supported. User must enter the database details in schema_to_dbml.py file in the folollowing field:

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

### 3. Upload DBML files to bigschema.io app
We can upload dbml files to bigschema.io app, executing the file dbml_to_api.py
All we need is the API url and a folder with all dbml files to upload
When upload is completed, api returns a unique id per file.
All ids are save in the file "response_ids.json", in key-value pairs, as below:

##### response_ids.json file example:
```
{
"file_1.dmbl": "6192b2c21c2a512293fea622",
"file_2.dmbl": "6172a2c21f2b3a17793fqa342"
}
```

*full code is included in file ``` dbml_to_api.py ```*

### 4. Retreive DBML files from bigschema.io app
Using the API url and the unique id of the file form previous step, we can retreive the file from the API with the following 2 commands:

##### code th retreive a dbml from api:
```
res = requests.get(f'{url}/{id}')
file = json.loads(res.json()['contents'])
```
*full code is included in file ``` dbml_from_api.py ```*

### Code of Conduct
All contributors are expected to follow the PyPA Code of Conduct.
