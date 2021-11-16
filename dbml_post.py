import requests
import os
import json
import datetime

'''
Code that uploads dbml files to API, using a POST request
'''

#path of the file that contains the dbml files that must be uploaded to API
files = os.listdir(r'C:\Users\grbus\Dropbox\Jobs\upwork\projects\pr36_PK_python library for DBs spreadsheets\getbigschema\dbml_files')

#url of the API
url='http://ec2-54-167-67-34.compute-1.amazonaws.com/api/dbmls'
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

#main code. It uploads all dbmls files to API, receives on id per file and creates a json file that contains all files and their associated ids
response_ids = {}
for file in files:
    with open(file, encoding="utf8") as f:
        t=f.read()
        r = requests.post(url, data={'filename': file, 'contents':json.dumps(t)})
        response_ids[file] = json.loads(r.text)['id']
    now = datetime.datetime.now()
    now = str(now)[:19]
    now=now.replace(' ', '-').replace(':', '-')
    with open(f'response_ids_{now}.json', 'w') as f:
        json.dump(response_ids, f)

'''
#code that pulls a dbml file from the API. It needs the file id, found in the 'response_ids.json' file generated in previous step   
id = '6192b1f31c2a512293fea940'
res = requests.get(f'http://ec2-54-167-67-34.compute-1.amazonaws.com/api/dbmls/{id}')
dbml = json.loads(res.json()['contents'])
'''
