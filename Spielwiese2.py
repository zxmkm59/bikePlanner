

# HOW TO USE: 
# https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc


import firebase_admin
#from firebase_admin import db
import json
from firebase_admin import firestore
import uuid
import datetime
import asyncio


databaseURL = 'https://bikePlanner-32f05.firebaseio.com/'

cred_obj = firebase_admin.credentials.Certificate('./Certificates/firebaseCredents.json')

default_app = firebase_admin.initialize_app(cred_obj)

#db = firestore.client()  # this connects to our Firestore database


testData = [{ "unique":  str(uuid.uuid1()),
                        "title": "Test1",
                        "owner": "itsMe",
                        "date": datetime.datetime.today(),
                        "distance": "123",
                        "climbs" : "3",
                        "elevation": "1000",
                        "velocity": "27",
                        "participants": ["itsYou"],
                            },
                        {
                        "unique":  str(uuid.uuid1()),
                        "title": "Test2",
                        "owner": "itsYou",
                        "climbs": "1",
                        "date": datetime.datetime.today(),
                        "distance": "56",
                        "elevation": "256",
                        "velocity": "22",
                        "participants": ["itsYou"]
                    }]
from google.cloud.firestore import AsyncClient 
from google.oauth2 import service_account     
with open('./Certificates/firebaseCredents.json') as json_file:
    json_data = json.load(json_file)
db = AsyncClient(
    project=json_data['project_id'],
    credentials=service_account.Credentials.from_service_account_info(json_data),
)

async def readData():
    collection = db.collection('Tours')  # opens 'places' collection
    # = collection.document('U')  # specifies the 'rome' document
    res = await collection.where("climbs", "==", "1").get()
    #print("RES: ", [r.to_dict() for r in res])
    return [r.to_dict() for r in res]

# Reading

erg = asyncio.run(readData())
print("RES:", erg)

breakpoint()


# Writing
collection = db.collection('Users')  # opens 'places' collection
res = collection.document('barcelona').set({
    'lat': 41.3851, 'long': 2.1734,
    'weather': 'great',
    'landmarks': [
        'guadí park',
        'gaudí church',
        'gaudí everything'
    ]
})

# Modify
res = collection.document('barcelona').update({
    'weather': 'rain'
})

# Delete

collection.document('barcelona').delete()