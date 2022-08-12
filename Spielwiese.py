import firebase_admin
from firebase_admin import credentials, db
import json


import requests

url = 'https://bikeplanner-32f05.firebaseio.com/'

auth_key = "AAAA39A-7bw:APA91bGerE2H8wPcx7mnTRE5uEUFnP3HgBt-YW3H5UU4YgZh8d0dy78VZh_luXCv9DKP-3ZdFvKvmj6BtR1iHYUxxmC-SPXSb99G--IW8MKDqN_OVOjx0mzWh1--3eThiTwb2qiMpFGh"
auth = {"auth":auth_key}

curUrl = f"{url} + test.json"

jFile = str({"test": "123"})


TOKEN = auth_key
HEADERS = {'Authorization': 'token {}'.format(TOKEN)}

with requests.Session() as s:

    s.headers.update(HEADERS)
    response = s.put(url=url, json=jFile)
    
    print(response.status_code)

"""cred = credentials.Certificate("C:\\Users\\tobia\\OneDrive\\Desktop\\Programming\\cyclePlanner\\backend\\bikeplanner-32f05-firebase-adminsdk-iyyzw-7244e2f6a0.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 
})
ref = db.reference("/")

ref.set({
        'boxes': 
            {
                'box001': {
                    'color': 'red',
                    'width': 1,
                    'height': 3,
                    'length': 2
                },
                'box002': {
                    'color': 'green',
                    'width': 1,
                    'height': 2,
                    'length': 3
                },
                'box003': {
                    'color': 'yellow',
                    'width': 3,
                    'height': 2,
                    'length': 1
                }
            }
        })"""