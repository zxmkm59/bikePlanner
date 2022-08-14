import sys
import firebase_admin
from firebase_admin import firestore
import streamlit as st
import time

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator

# Pricing
# https://firebase.google.com/pricing?authuser=0&hl=de

class FirebaseConnector:
    def __init__(self) -> None:
        self.config = Configurator

        self.createConnection()

    # create connection to firebase
    def createConnection(self):
        # If openened more than once:
        try:
            firebase_admin.get_app()
        except:
            cred_obj = firebase_admin.credentials.Certificate("./Certificates/firebaseCredents.json")
            default_app = firebase_admin.initialize_app(cred_obj)

        # this connects to Firestore database
        self.db = firestore.client() 

    # reader for one document
    def reader(self, document):
        res = document.get()
        return res.to_dict()

    # reader for all documents of one collection
    def readerCollection(self, collection):
        res = collection.get()

        # Convert to dictionaries
        docs = [r.to_dict() for r in res]
        return docs

    # Write to a collection
    def writer(self, collection, key:str, data:dict):
        collection.document(key).set(data)

    # Tour Management 
    # ------------------------------------------------------------------------------------

    # Update an entry
    def updateEntry(self, tour: dict):
        # get the unique ident
        key = tour["unique"]

         # key as document key
        key = tour["unique"]

        collection = self.db.collection("Tours")

        # Insert new tour
        self.writer(collection, key, tour)

    # load all known tours
    def loadTours(self):
        
        collection = self.db.collection("Tours")

        tours = self.readerCollection(collection)

        return tours
    
    # create new tour 
    def insertNewTour(self, tour):
        # key as document key
        key = tour["unique"]

        collection = self.db.collection("Tours")

        # Insert new tour
        self.writer(collection, key, tour)

    # ------------------------------------------------------------------------------------


    # User Management
    # ------------------------------------------------------------------------------------

    # User Query for register
    def userQueryRegister(self, equalDict: dict):
        # User collection
        collection = self.db.collection("Users")

        key = list(equalDict.keys())[0]

        qs = collection.where(key, "==", str(equalDict[key])).get()

        return [q.to_dict() for q in qs]

    # user query for login
    def userQueryLogin(self, credents: dict):
        # User collection
        collection = self.db.collection("Users")
        
        # check user name and password
        qs = collection.where("user", "==", credents["user"]).where("password", "==", credents["password"]).get()

        ds = [q.to_dict() for q in qs]

        if len(ds) >0:
            return ""
        else:
            return "User is unknown"

    # register a new User
    def registerUser(self, credents):

        # Check if user is already known
        users = self.userQueryRegister({"user": credents["user"]})
        userKnown = len(users) > 0

        # Check if email is already known
        emails = self.userQueryRegister({"email": credents["email"]})
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

            self.writer(collection, credents["user"], credents)
        return message

    # wrapper: Login a user
    def loginUserCheck(self, credents):
        message = self.userQueryLogin(credents)
        return message
       




    