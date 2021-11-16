import requests
import os
import json
import datetime

'''
Pulls a dbml file from the API. User must manually add the file id, found in the 'response_ids.json' file generated from dbml_post_to_api.py
'''

url='http://ec2-54-167-67-34.compute-1.amazonaws.com/api/dbmls' 
id = '6192b1f31c2a512293fea940'
res = requests.get(f'{url}/{id}')
dbml_file = json.loads(res.json()['contents'])
