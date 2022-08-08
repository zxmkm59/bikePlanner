import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

import streamlit as st

from config import Configurator
from loginScreen import Login
from tourScreen import TourList

class MainScreen:
    def __init__(self) -> None:
        self.config = Configurator()
        self.login = Login()
        self.tour = TourList()

    # Create Main Page
    def mainPage(self):
        
        # Tab 1: Login or Register
        self.login.loginOrRegister()

        # If logged in succesfull:
        if "login" in st.session_state and st.session_state["login"]["state"] == "success":
            
            # Show and create tours
            self.tour.mainTour()

    



if __name__ == "__main__":
    
    m = MainScreen()

    m.mainPage()

    # streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/frontend/mainScreen.py