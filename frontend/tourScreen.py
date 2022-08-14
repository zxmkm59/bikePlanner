import sys

#sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

import streamlit as st

from config import Configurator
from tourElement import TourWidget
from gpxReader import GpxViewer

# helper: modulo
def helpMod(x, num):
    while x >= num:
        x -= num
    return x

# Pre create Containers 
headContainer = st.container()
createContainer = st.container()

class TourList:
    def __init__(self, base) -> None:
        self.config = Configurator()

        # other instances
        self.tourWidget = TourWidget(base)
        self.gpx = GpxViewer()

        # All attributes of a tour with display type
        self.attributes = self.tourWidget.attributes

        self.base = base

    # Main tour screen
    def mainTour(self):
        # Head line
        self.headLine()

        # All known tours
        self.listTours()

    # Head line
    def headLine(self):
        cols = st.columns([0.3 ,1, 0.3])

        # Create new tour
        if st.session_state["login"]["role"] == "guide":
            cols[0].button("Create new", on_click=self.setCreateState) 
        
        # Open create new tour display after reload
        if "ShowCreateTourWidget" in st.session_state and st.session_state["ShowCreateTourWidget"]:
            self.createTour()
        
        # Logout
        cols[-1].button("Logout", key="logoutButton", on_click=self.logoutCallback)

    def setCreateState(self):
         # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = True

    # List all known tours
    def listTours(self):
        # load all existing tours
        tours = self.base.loadTours()

        # build tours
        for tour in tours:
            try:
                self.tourWidget.tourWidget(tour)
            except:
                print("Eine Tour konnte nicht geladen werden!")

    # create new tour
    def createTour(self):
        # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = True

        # Creation Widget
        with st.expander("create new tour", expanded = True):
            tourAttr = self.tourWidget.createWidget()

            # button options: save and discard
            cols = st.columns([0.3, 1, 0.3])

            cols[0].button("Save",  on_click=self.saveTourCallback, args=(tourAttr,)) # key = "saveNewTour",

            cols[-1].button("discard", on_click=self.discardTourCallback)  # , key="discardNewTour"

    def saveTourCallback(self, tourAttr : dict):
        self.base.insertNewTour(tourAttr)

        st.success("New tour created")

         # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = False

    def discardTourCallback(self):
         # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = False

    # Logout Callback
    def logoutCallback(self):
        del st.session_state["login"]

