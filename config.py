# firebase Connection
firebase_connection = {"certFile": "firebaseCredents.json",
                       "tourMaxAge": 60*60*24  # maximum age of tours in seconds
                    }

class Configurator:
    def __init__(self) -> None:
        self.firebase_connection = firebase_connection