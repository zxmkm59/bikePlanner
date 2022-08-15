import datetime
import sys
import traceback
import firebase_admin
from firebase_admin import firestore

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator

# Pricing
# https://firebase.google.com/pricing?authuser=0&hl=de

# HOW TO USE: 
# https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc

class FirebaseConnector:
    def __init__(self) -> None:
        # load configurations
        self.config = Configurator()

        # Create the connection to firebase
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

    # delete a sepcific tour
    def deleteTour(self, key):
        collection = self.db.collection("Tours")
        collection.document(key).delete()

    # Tour Management 
    # ------------------------------------------------------------------------------------

    # Update an entry
    def updateEntry(self, tour: dict):
        # get the unique ident
        key = tour["unique"]

         # key as document key
        key = tour["unique"]

        # the tour collection
        collection = self.db.collection("Tours")

        # Insert new tour
        self.writer(collection, key, tour)

    # load all known tours
    def loadTours(self) -> list:
        
        # check for old tours
        self.checkStarttime()

        # load all actual tours
        collection = self.db.collection("Tours")

        # tour collection
        tours = self.readerCollection(collection)

        return tours

    # create new tour 
    def insertNewTour(self, tour:dict):
        # key as document key
        key = tour["unique"]

        # tour collection
        collection = self.db.collection("Tours")

        # Insert new tour
        self.writer(collection, key, tour)

    # Check if the starttime is yesterday. Then delete tours
    def checkStarttime(self):
        try:
            collection = self.db.collection("Tours")

            # maximum age of tours
            dtYest = (datetime.datetime.today() - datetime.timedelta(seconds = int(self.config.firebase_connection["tourMaxAge"]))).timestamp()
            qs = collection.where("date", "<=", dtYest).get()

            # convert to dicts
            qs = [q.to_dict() for q in qs]

            print(f"Es sind {len(qs)} Touren abgelaufen und werden gelöscht")

            # deletion
            deleteKeys = [q["unique"] for q in qs]
            [self.deleteTour(key) for key in deleteKeys]
        except:
            print(traceback.print_exc())

    # ------------------------------------------------------------------------------------


    # User Management
    # ------------------------------------------------------------------------------------

    # User Query for register
    # check one key, value pair in the db
    def userQueryRegister(self, equalDict: dict):
        # User collection
        collection = self.db.collection("Users")

        # equalDict has only one key
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

        # Returning: Error message and user role if possible
        if len(ds) >0:
            return "", ds[0]["role"]
        else:
            return "User is unknown", ""

    # register a new User
    def registerUser(self, credents: dict) -> str:

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

            # create new user in db
            self.writer(collection, credents["user"], credents)
        return message

    # wrapper: Login a user
    def loginUserCheck(self, credents):
        message = self.userQueryLogin(credents)
        return message
       




    