import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")
sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/backend")

import streamlit as st
import datetime

from config import Configurator
from tourElement import TourWidget
from firebaseConn import FirebaseConnector

# helper: modulo
def helpMod(x, num):
    while x > num:
        x -= num
    return x

# Pre create Containers 
headContainer = st.container()
toursContainer = st.container()

class TourList:
    def __init__(self) -> None:
        self.config = Configurator()

        self.tourWidget = TourWidget()

        # All attributes of a tour with display type
        self.attributes = self.tourWidget.attributes

        self.base = FirebaseConnector()

    # Main tour screen
    def mainTour(self):
        # Head line
        self.headLine()

        # All known tours
        self.listTours()

    # Head line
    def headLine(self):
        cols = st.columns(5)

        # Create new tour
        if st.session_state["login"]["role"] == "guide":
            cols[0].button("Create new", on_click=self.createTour)
        
        # Logout
        cols[-1].button("Logout", key="logoutButton", on_click=self.logoutCallback)

    # List all known tours
    def listTours(self):
        # load all existing tours
        tours = self.base.loadTours()

        # build tours
        for tour in tours:
            uniKey = self.tourWidget.buildWidget(tour)

            # Add participation optione
            cols = st.columns(5)
            cols[-1].button("participate", key=str(uniKey) + "participate")

    # create new tour
    def createTour(self):
        # extra widget
        with st.expander("create new tour", expanded = True):
            c = int(self.config.tour["columnSize"])
            cols = st.columns(c)

            tourAttr = {}

            for i, a in enumerate(self.attributes):
                # Jump to the correct column
                j = helpMod(i, c-1)

                # Manage different display types
                if self.attributes[a] in ["text", "metric"]:
                    tourAttr[a] = cols[j].text_input(a)
                elif self.attributes[a] == "map":
                    tourAttr[a] = cols[j].multiselect(a, options=[])  # Missing for gpx
                elif self.attributes[a] == "date":
                    tourAttr[a] = cols[j].date_input(a, min_value=datetime.datetime.today())

            # Add the autor:
            tourAttr["owner"] = st.session_state["login"]["credents"]["user"]
        
            # save new tour
            cols = st.columns(5)

            cols[0].button("Save", key = "saveNewTour", on_click=self.saveTourCallback, args=(tourAttr,))

            cols[-1].button("discard", key="discardNewTour", on_click=self.discardTourCallback)

    def saveTourCallback(self, tourAttr : dict):
        st.write("MISSING: FIREBASE SAVING")

    def discardTourCallback(self):
        pass
    
    # Logout Callback
    def logoutCallback(self):
        del st.session_state["login"]

    # Pariticpation callback
    def participateCallback(self):
        st.write("MISSING PARICIAPTE CALLBACK, NEED UNIQ KEY")
