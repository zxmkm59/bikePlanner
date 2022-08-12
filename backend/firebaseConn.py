import sys
import uuid
import datetime

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator

# Pricing
# https://firebase.google.com/pricing?authuser=0&hl=de

class FirebaseConnector:
    def __init__(self) -> None:
        self.config = Configurator

    # create connection to firebase
    def createConnection(self):
        pass

    # Update an entry
    def updateEntry(self, tour: dict):
        # get the unique ident
        uniqueIdent = tour["unique"]

        print("MISSING: Update a firebase entry")


    # load all known tours
    def loadTours(self):
        # dummy
        dummyTours = [{ "unique":  uuid.uuid1(),
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
                        "unique":  uuid.uuid1(),
                        "title": "Test2",
                        "owner": "itsYou",
                        "climbs": "1",
                        "date": datetime.datetime.today(),
                        "distance": "56",
                        "elevation": "256",
                        "velocity": "22",
                        "participants": ["itsYou"]
                    }]
        return dummyTours
