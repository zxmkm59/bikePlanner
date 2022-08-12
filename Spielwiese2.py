

# HOW TO USE: 
# https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc


import firebase_admin
#from firebase_admin import db
import json
from firebase_admin import firestore


databaseURL = 'https://bikePlanner-32f05.firebaseio.com/'

cred_obj = firebase_admin.credentials.Certificate('./backend/firebaseCredents.json')

default_app = firebase_admin.initialize_app(cred_obj)

db = firestore.client()  # this connects to our Firestore database

# Reading
collection = db.collection('Users')  # opens 'places' collection
doc = collection.document('U')  # specifies the 'rome' document
res = doc.get().to_dict()
print(res)


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