#exec(open("parser_1115.py", errors='ignore').read())

import json
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel, validator
from collections import defaultdict
 

with open("manifest_demo_1115.json", encoding="utf8") as f:
    man = json.load(f, strict=False)
    
with open("catalog_demo_1115.json", encoding="utf8") as f:
    cat = json.load(f, strict=False)
    
all_tables = list(man['parent_map'].keys())
    
try:
    db_name = man['nodes'][list(man['nodes'].keys())[0]]['schema']
    if db_name is None:
        db_name = 'undefined'
except:
    db_name = 'undefined'

refs=[]

for table_name in all_tables: 
    for ref_table in man['parent_map'][table_name]:           
        refs.append((ref_table, table_name))
        
refs=set(refs)

gridx = {i:'' for i in all_tables}

for x in all_tables:
    if len([i for i in refs if i[1]==x]) == 0:
        gridx[x] = 0
        for k in refs:
            if k[0]==x:
                gridx[k[1]]=1
 
while True:
    temp = [i for i in gridx if gridx[i]=='']
    if len(temp)==0:
        break
    for i in temp:
        parents = man['parent_map'][i]
        if any([gridx[j]=='' for j in parents]):
            continue
        else:
            gridx[i]=max([gridx[j] for j in parents])+1      

all_tables = {k: v for k, v in sorted(gridx.items(), key=lambda item: item[1])}       

with open(f"{db_name}_full.dmbl", "w") as output:
    for table_name in all_tables: 
        output.write('table "' + table_name + '" [gridX: ' + str(gridx[table_name]) + '] {\n')
        if table_name in cat['nodes'] or table_name in cat['sources']:
            if table_name in cat['nodes']:
                table = cat['nodes'][table_name]
            elif table_name in cat['sources']:
                table = cat['sources'][table_name]
            for column in table['columns']:
                column = table['columns'][column]
                comment = '' if (column['comment'] is None or column['comment'] in ['', ' ']) else ' // ' + column['comment']
                comment = comment.replace('\n', '')
                output.write('   "' + column['name'] + '" ' +  str(column['type']) + comment + '\n') 
            output.write('   Note: "' + table['metadata']['type'] + '"\n')
            output.write("}\n\n")
        elif table_name in man['nodes'] or table_name in man['sources']:
            if table_name in man['nodes']:
                table = man['nodes'][table_name]
            elif table_name in cat['sources']:
                table = man['sources'][table_name]       
            for column in table['columns']:
                column = table['columns'][column]
                comment = '' if (column['description'] is None or column['description'] in ['', ' ']) else ' // ' + column['description']
                comment = comment.replace('\n', '')
                output.write('   "' + column['name'] + '" ' +  str(column['data_type']) + comment + '\n') 
            output.write("}\n")
        output.write("ref_parents: " + str(man['parent_map'][table_name]))
        output.write('\n')
        output.write("ref_children: " + str(man['child_map'][table_name]))
        output.write('\n\n')


with open('topological_sort.json', 'w') as f:
    json.dump(all_tables, f) 