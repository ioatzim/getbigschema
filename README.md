# getbigschema
Creation of dbml files from given databases and spreadsheets.
Upload dbmls to API

## Requirements
Requires Python 3.6 or above. ???

## Main features
The main features provided by getbigschema are:
Generating dbml files, from existing databases and spreadsheets
Generating dbml files, from existing manifest.json and catalog.json files that are produced with dbt methods
Uploading dbml files to API
Requesting dbml files from API

## Usage
Code can be executed in any Python interpreter/terminal or framework, including Jupyter, Conda, Pycharm, etc

## Examples


### Example1: # DBT
DBT example --> manifest.json, .. --> to how to run "dbt2dbml.py"

#### Example2: # For SQL DBs (BigQuery, RedShift, etc.)
..--> how to run "schema2dbml.py" for some db (e.g, MySql)

#### Example3: # POST to bigschema.io app
--> how to run "dbml2draw.py"



## Code of Conduct
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
   
