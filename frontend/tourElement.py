import time
import streamlit as st
import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")
sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/backend")

from config import Configurator
from firebaseConn import FirebaseConnector


# helper: modulo
def helpMod(x, num):
    while x > num:
        x -= num
    return x

class TourWidget:
    def __init__(self) -> None:
        self.config = Configurator()
        self.base = FirebaseConnector()

        # which keys should not showed?
        self.notAttributes = ["unique"]

        # All attributes of a tour with display type
        self.attributes = {"title": "text",
                            "date": "date",
                            "distance": "metric",
                           "elevation": "metric",
                           "velocity": "metric",
                           "climbs" : "metric",
                           "gpx": "map"
                        } 
        # units of attributes
        self.units = {"title": "", 
                      "date": "",
                      "distance": "km",
                      "velocity": "km/h",
                      "elevation": "hm",
                      "climbs": "",
                      "gpx": ""}

    # build tour widget
    def buildWidget(self, tour):

        # Size for columns in grid
        c = int(self.config.tour["columnSize"])

        # build a title from the date and custom title name
        title = f"{tour['date']} | {tour['title']}"

        # unique Key of this tour
        uniqKey = tour["unique"]

        # widget
        with st.expander(title, expanded = False):
        
            cols = st.columns(c)

            for i, key in enumerate(tour.keys()):
                # take value
                v = tour[key]

                # Jump to the correct column
                j = helpMod(i, c-1)

                # Manage different display types

                # 1. From owner input
                if key in self.attributes:
                    # Add a unit
                    v = f"{v} {self.units[key]}"

                    if self.attributes[key] == "text":
                        cols[j].text(f"{key}: {v}")
                    elif self.attributes[key] == "metric":
                        cols[j].metric(label=key, value=v)
                    elif self.attributes[key] == "date":
                        cols[j].text(f"{key}: {v}")

                # dont show key
                elif key in self.notAttributes:   
                    continue
                # Not from owner attributes
                else:
                    cols[j].text(f"{key}: {v}")

            # Add participation option
            cols = st.columns(5)
            owner = st.session_state["login"]["credents"]["user"]
            if owner in tour["participants"]:  # already participant
                cols[-1].button("unparticipate", on_click = self.unparticipateCallback, args=(tour.copy(), ), key=str(uniqKey) + "unparticipate")
            else:  # not participant
                cols[-1].button("participate", on_click = self.participateCallback, args=(tour.copy(), ) ,key=str(uniqKey) + "participate")

    # Pariticpation callback
    def participateCallback(self, tour : dict):

        # Add user to given unique ident
        user = st.session_state["login"]["credents"]["user"]
        tour["participants"].append(user)

        self.base.updateEntry(tour)

    # Un - pariticpation callback
    def unparticipateCallback(self, tour : dict):

        # Add user to given unique ident
        user = st.session_state["login"]["credents"]["user"]
        tour["participants"] = [p for p in tour["participants"] if p != user]

        self.base.updateEntry(tour)
