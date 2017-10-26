import requests
import json

with open('pdvs.json') as data_file:
    pdvs = json.load(data_file)

url = 'http://localhost:8000/'

print('\n Failed to populate the following PDVs: \n')
for pdv in pdvs["pdvs"]:
    post_url = url + 'pdvs'
    r = requests.post(post_url, json=pdv)

    errors = 0
    if r.status_code != 201:
        errors += 1
        print('Document: {}'.format(pdv['document']))
        print('Trading Name: {}'.format(pdv['tradingName']))
        print(r.status_code)
        print(r.text)
        print('')
