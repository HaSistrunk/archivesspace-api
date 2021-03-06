import json
import requests
import secrets
import time
import csv

startTime = time.time()

def findKey(d, key):
    if key in d:
        yield d[key]
    for k in d:
        if isinstance(d[k], list) and k == 'children':
            for i in d[k]:
                for j in findKey(i, key):
                    yield j

baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

id = raw_input('Enter resource ID: ')

treeEndpoint = '/repositories/3/resources/'+str(id)+'/tree'

output = requests.get(baseURL + treeEndpoint, headers=headers).json()
archivalObjects = []
for value in findKey(output, 'record_uri'):
    if 'archival_objects' in value:
        archivalObjects.append(value)
print archivalObjects

for archivalObject in archivalObjects:
    output = requests.get(baseURL + archivalObject, headers=headers).json()
    output['publish'] = False
    asRecord = json.dumps(output)
    post = requests.post(baseURL + archivalObject, headers=headers, data=asRecord).json()
    print post

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
