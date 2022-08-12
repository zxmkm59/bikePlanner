import email
from email import message
import sys
import uuid
import datetime
import asyncio
from google.cloud.firestore import AsyncClient 
from google.oauth2 import service_account   
import json
import traceback
import time

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator

# Pricing
# https://firebase.google.com/pricing?authuser=0&hl=de

class FirebaseConnector:
    def __init__(self) -> None:
        self.config = Configurator

        # Initial connect to the database
        self.createConnection()

        #self.loop = asyncio.new_event_loop()

    # create connection to firebase
    def createConnection(self):
        connected = False

        while not connected:
            try:
                # Synchron:
                """                cred_obj = firebase_admin.credentials.Certificate("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/Certificates/firebaseCredents.json")

                default_app = firebase_admin.initialize_app(cred_obj)

                # this connects to Firestore database
                self.db = firestore.client() """ 
                
                with open('./Certificates/firebaseCredents.json') as json_file:
                    json_data = json.load(json_file)

                self.db = AsyncClient(
                    project=json_data['project_id'],
                    credentials=service_account.Credentials.from_service_account_info(json_data),
                )

                connected = True
            except:
                print(traceback.print_exc())
                time.sleep(2)
                print("Firebase Connection Error")

    # create event loops
    def createLoop(self):

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

    # asynchron reader for one document
    async def reader(self, document):
        res = await document.get()
        return res.to_dict()

    # asynchron reader for all documents of one collection
    async def readerCollection(self, collection):
        res = await collection.get()

        # Convert to dictionaries
        docs = [r.to_dict() for r in res]
        return docs

    # Write to a collection
    async def writer(self, collection, key:str, data:dict):
        await collection.document(key).set(data)

    # Tour Management 
    # ------------------------------------------------------------------------------------

    # Update an entry
    def updateEntry(self, tour: dict):
        # get the unique ident
        uniqueIdent = tour["unique"]

        print("MISSING: Update a firebase entry")

    # load all known tours
    def loadTours(self):
        loop = self.createLoop()
        
        collection = self.db.collection("Tours")

        tours = loop.run_until_complete(self.readerCollection(collection))

        return tours
    
    # create new tour 
    def insertNewTour(self, tour):
        loop = self.createLoop()

        # key as document key
        key = tour["unique"]

        collection = self.db.collection("Tours")

        # Insert new tour
        loop.run_until_complete(self.writer(collection, key, tour))

    
    # ------------------------------------------------------------------------------------


    # User Management
    # ------------------------------------------------------------------------------------

    # Async User Query for register
    async def userQueryRegister(self, equalDict: dict):
        # User collection
        collection = self.db.collection("Users")

        key = list(equalDict.keys())[0]

        qs = await collection.where(key, "==", str(equalDict[key])).get()

        return [q.to_dict() for q in qs]

    # async user query for login
    async def userQueryLogin(self, credents: dict):
        # User collection
        collection = self.db.collection("Users")
        
        # check user name and password
        qs = await collection.where("user", "==", credents["user"]).where("password", "==", credents["password"]).get()

        ds = [q.to_dict() for q in qs]

        if len(ds) >0:
            return ""
        else:
            return "User is unknown"

    # register a new User
    def registerUser(self, credents):
        loop = self.createLoop()

        # Check if user is already known
        users = loop.run_until_complete(self.userQueryRegister({"user": credents["user"]}))
        userKnown = len(users) > 0

        # Check if email is already known
        emails = loop.run_until_complete(self.userQueryRegister({"email": credents["email"]}))
        emailKnown = len(emails) > 0

        # Create message
        if emailKnown and userKnown:
            message = "User and Email are already in use"
        elif emailKnown:
            message = "Email is already in use"
        elif userKnown:
            message = "Username is already in uses"
        else:  # create a new user
            message = ""
        
            # User collection
            collection = self.db.collection("Users")

            loop.run_until_complete(self.writer(collection, credents["user"], credents))
        return message

    # wrapper: Login a user
    def loginUserCheck(self, credents):
        loop = self.createLoop()

        message = loop.run_until_complete(self.userQueryLogin(credents))
        return message
       




    