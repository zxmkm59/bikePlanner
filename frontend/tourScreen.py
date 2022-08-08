import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

import streamlit as st

from config import Configurator

# helper: modulo
def helpMod(x, num):
    while x > num:
        x -= num
    return x

class TourList:
    def __init__(self) -> None:
        self.config = Configurator()

        # All attributes of a tour with display type
        self.attributes = {"distance": "text",
                           "height": "text",
                           "average velocity": "text",
                           "climbs" : "text",
                           "gpx": "map"
                        } 

    # Main tour screen
    def mainTour(self):
        # All known tours
        self.listTours()

        # create new tour
        createTourBut = st.button("Create new", on_click=self.createTour)

    # List all known tours
    def listTours(self):
        # load all existing tours
        
        pass

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
                if self.attributes[a] == "text":
                    tourAttr[a] = cols[j].text_input(a)
                elif self.attributes[a] == "map":
                    tourAttr[a] = cols[j].multiselect(a, options=[])  # Missing for gpx
        
            # save new tour
            cols = st.columns(5)

            cols[0].button("Save", key = "saveNewTour", on_click=self.saveTourCallback, args=(tourAttr,))

            cols[-1].button("discard", key="discardNewTour", on_click=self.discardTourCallback)

    def saveTourCallback(self, tourAttr : dict):
        st.write("MISSING: FIREBASE SAVING")

    def discardTourCallback(self):
        pass


