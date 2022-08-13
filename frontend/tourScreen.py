import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

import streamlit as st
import datetime
import uuid
import time

from config import Configurator
from tourElement import TourWidget
from gpxReader import GpxViewer

# helper: modulo
def helpMod(x, num):
    while x > num:
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
        cols = st.columns(5)

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
            self.tourWidget.buildWidget(tour)

    # create new tour
    def createTour(self):
        # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = True

        # extra widget
        with st.expander("create new tour", expanded = True):
                with st.container():
                    c = int(self.config.tour["columnSize"])
                    cols = st.columns(c)

                    tourAttr = {}

                    for i, a in enumerate(self.attributes):
                        # Jump to the correct column
                        j = helpMod(i, c-1)

                        # Manage different display types
                        if self.attributes[a] in ["text", "metric"]:
                            tourAttr[a] = cols[j].text_input(a)                         
                        elif self.attributes[a] == "date":
                            tourAttr[a] = datetime.datetime.today().timestamp()   # missing: cols[j].date_input(a, min_value=datetime.datetime.today())
    
                    # Add Gpx import and viewer
                    tourAttr["gpx"] = self.gpx.addGpx()

                    # Add the autor:
                    tourAttr["owner"] = st.session_state["login"]["credents"]["user"]

                    # Add a unique Key
                    tourAttr["unique"] = str(uuid.uuid1())

                    # participants empty at beginning
                    tourAttr["participants"] = []
                
                    # save new tour
                    cols = st.columns(5)

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

