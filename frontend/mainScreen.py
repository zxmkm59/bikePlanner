import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/backend")
sys.path.append("/app/backend")

import streamlit as st

from config import Configurator
from loginScreen import Login
from tourScreen import TourList
from firebaseConnSync import FirebaseConnector

class MainScreen:
    def __init__(self) -> None:
        self.config = Configurator()

        # Create Firebase Connection
        self.base = FirebaseConnector()

        # Other instances which use firebase Connector
        self.login = Login(self.base)
        self.tour = TourList(self.base)

    # Create Main Page
    def mainPage(self):
        
        # Login or Register
        self.login.loginOrRegister()

        # If logged in succesfully:
        if "login" in st.session_state and st.session_state["login"]["state"] == "success":
            
            # Show and create tours
            self.tour.mainTour()

def main():
    m = MainScreen()

    m.mainPage()

if __name__ == "__main__":
    main()
    

    # streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/frontend/mainScreen.py