import requests
import os
import json
import datetime

'''
Uploads dbml files to API
'''

#path of the folder which contains the dbml files that must be uploaded to the API.User must manually create such a folder and put all dmbl files in it
path = r'...\dbml_files'
files = os.listdir(path)

#url of the API
url='http://ec2-54-167-67-34.compute-1.amazonaws.com/api/dbmls'

#Uploads all dbmls files to API, on execution it returns one id per file and creates a json file which contains all files with their associated ids in key:value format
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
