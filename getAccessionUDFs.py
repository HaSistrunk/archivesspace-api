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

endpoint = '/repositories/3/accessions?all_ids=true'

ids = requests.get(baseURL + endpoint, headers=headers).json()

udfs = []
for id in ids:
    print id
    endpoint = '/repositories/3/accessions/'+str(id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    try:
        userDefined = output['user_defined']
        for k, v in userDefined.items():
            if k not in udfs:
                udfs.append(k)
    except:
        userDefined = ''
udfs.sort()
udfsHeader = ['title', 'uri'] + udfs
f=csv.writer(open('accessionsUdfs.csv', 'wb'))
f.writerow(udfsHeader)

for id in ids:
    print id
    endpoint = '/repositories/3/accessions/'+str(id)
    output = requests.get(baseURL + endpoint, headers=headers).json()
    title = output['title'].encode('utf-8')
    uri = output['uri']
    accessionUdfs = []
    for udf in udfs:
        try:
            keyValue = udf+'|'+output['user_defined'][udf].encode('utf-8')
        except:
            keyValue = udf+'|'
        accessionUdfs.append(keyValue)
    accessionUdfs.sort()
    accessionUdfsUpdated = []
    for accessionUdf in accessionUdfs:
        edited = accessionUdf[accessionUdf.index('|')+1:]
        accessionUdfsUpdated.append(edited)
    accessionUdfsRow = [title, uri] + accessionUdfsUpdated
    f.writerow(accessionUdfsRow)

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
