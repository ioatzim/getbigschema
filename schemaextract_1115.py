#exec(open("schemaextract_1115.py", errors='ignore').read())

import os
import getschema
import gspread
import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import MetaData
from sqlalchemy import *
import pandas as pd  
import gsheetsdb
from gsheetsdb import connect
import itertools
import time

#A. Creation of dbml files:

#1. databases
#For each one of your databases, add one record to the following list (records must be separated with comma). Each record must include the name of the database (select a name of your choice), and the url of the database, based on sqlalchemy instructions found here: https://docs.sqlalchemy.org/en/14/core/engines.html:

databases = [
{'name': 'database_1', 'url': 'sqlite:///test.db'}
]

#The following piece of code generates one dbml file per database. Dbml files are saved in the same folder with the python script:
for database in databases:
    engine = create_engine(database['url'])
    m = MetaData()
    m.reflect(engine)
    refs = []       
    with open(f"{database['name']}.dmbl", "w") as output:
        for table_name in m.tables.values():
            output.write('table "'+table_name.name+'" {\n')
            for column in table_name.columns:
                prim_key = 'primary key' if column.primary_key==True else ''
                nullable = 'not null' if column.nullable==False else ''
                unique = 'unique' if column.unique == True else ''
                increment = 'increment' if column.autoincrement==True else ''  
                param = [prim_key, nullable, unique, increment]
                param = [i for i in param if i !='']
                param='[' + ','.join(param) + '] ' if len(param)>0 else ''
                comment = '' if column.comment is None else column.comment
                output.write('   "' + column.name + '" ' +  str(column.type) + ' ' + param + '//' + ' ' + comment + '\n') 
                if len(column.foreign_keys) > 0:
                    for i in column.foreign_keys: 
                        ref = 'Ref: ' + column.table.name + '.' + column.name + ' > ' + i.column.table.name +  '.' + i.column.name
                        refs.append(ref)
            output.write("}\n\n")
        for ref in refs:
            output.write('\n' + ref)
            
#2. spreadsheets
conn = connect()

#For each one google spreadsheet, add one record to the following list. Each record must include the name of the sheet (select a name of your choice), and the url of the sheet. Records must be separated with comma

google_sheets = [
{'name': 'Hospital Bed Utilization', 'url': "https://docs.google.com/spreadsheets/d/1I1S9WW4OEHaNpqebM0L5sumoElrmVBCXCTVItHNZdbs/edit?usp=sharing"}
]

#The following piece of code generates one dbml file for all google sheets. Dbml file is saved in the same folder with the python script:
with open("spreadsheets.dmbl", "w") as output:
    for file in google_sheets:
        output.write('table "'+ file['name'] +'" {\n')
        df=pd.read_sql('select * from "' + file['url'] + '"', conn)
        for column in df.columns:
            output.write('   "' + column + '" ' +  str(df[column].dtype) + '\n') 
        output.write("}\n\n")