import sys
import datetime

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator

class FirebaseConnector:
    def __init__(self) -> None:
        self.config = Configurator

    # create connection to firebase
    def createConnection(self):
        pass

    # load all known tours
    def loadTours(self):
        # dummy
        dummyTours = [{ "owner": "itsMe",
                        "date": datetime.datetime.today(),
                        "distance": "123",
                        "elevation": "1000",
                        "velocity": "27",
                        "participants": ["itsYou"]
                            },
                        {"owner": "itsYou",
                        "date": datetime.datetime.today(),
                        "distance": "56",
                        "elevation": "256",
                        "velocity": "22",
                        "participants": ["itsYou"]
                    }]
        return dummyTours
