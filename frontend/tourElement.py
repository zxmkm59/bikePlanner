from datetime import datetime
import time
import streamlit as st
import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator
from gpxReader import GpxViewer

# helper: modulo
def helpMod(x, num):
    while x >= num:
        x -= num
    return x

class TourWidget:
    def __init__(self, base) -> None:
        self.config = Configurator()
        self.base = base
        self.gpx = GpxViewer()

        # which keys should not showed?
        self.notAttributes = ["unique"]

        # All attributes of a tour with display type
        self.attributes = {"distance": "metric",
                           "elevation": "metric",
                           "velocity": "metric",
                           "climbs" : "metric",
                        } 
        # units of attributes
        self.units = {"distance": "km",
                      "velocity": "km/h",
                      "elevation": "hm",
                      "climbs": ""}

    # build tour widget
    def buildWidgetOld(self, tour):

        # Size for columns in grid
        c = int(self.config.tour["columnSize"])

        # build a title from the date and custom title name
        title = f"{tour['date']} | {tour['title']}"

        # unique Key of this tour
        uniqKey = tour["unique"]

        # widget
        with st.expander(title, expanded = False):
        
            cols = st.columns(c)

            for i, key in enumerate(sorted(list(tour.keys()))):
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

    # build tour widget
    def buildWidget(self, tour):

        # starttime of the tour
        date = datetime.fromtimestamp(tour['date'])

        # build a title from the date and custom title name
        title = f"{date} | {tour['title']}"

        # widget
        with st.expander(title, expanded = False):
            
            # Header: date, time, startplace
            # Second: Participants 
            # Third: Meta Data 
            # 4: GPX

            # Header 
            headCols = st.columns(2)
            headCols[0].metric(label="Starttime", value=str(date))
            headCols[1].metric(label="Startplace", value=tour["startplace"]), 
            st.write("---")

            # Second
            self.addCaption(f"Participants")
            self.addCaption(f"total: {len(tour['participants'])}")
            cols2_1 = st.columns(3)
            for i, p in enumerate(tour["participants"]):
                j  = helpMod(i, 3)
                #cols2_1[j].write(p)
                cols2_1[j].button(label=p, key=f"{p}_{tour['unique']}", disabled=True)

            # add participate option
            self.participate(tour)

            # Sum overall

            st.write("---")

            # Third
            self.addCaption("The hard facts")
            cols3 = st.columns(3)
            for i, at in enumerate(self.units):
                j = helpMod(i, 3)
                cols3[j].metric(label=at, value= f"{tour[at]} {self.units[at]}")
            st.write("---")

            # Last: GPX Data
            self.addCaption("GPX")
            gpxCols = st.columns([1,4,1])
            with gpxCols[1]:
                gpxData = tour["gpx"]

                self.gpx.showGpx(gpxData)

    # Add a caption statement
    def addCaption(self, txt: str):
        colsCaption = st.columns(10)
        colsCaption[5].caption(txt)

    # Add participate option
    def participate(self, tour):
        # Add participation option
        cols = st.columns(5)
        owner = st.session_state["login"]["credents"]["user"]
        if owner in tour["participants"]:  # already participant
            cols[-1].button("unparticipate", on_click = self.unparticipateCallback, args=(tour.copy(), ), key=str(tour["unique"]) + "unparticipate")
        else:  # not participant
            cols[-1].button("participate", on_click = self.participateCallback, args=(tour.copy(), ) ,key=str(tour["unique"]) + "participate")


    # Pariticpation callback
    def participateCallback(self, tour : dict):

        # Add user to given unique ident
        user = st.session_state["login"]["credents"]["user"]
        tour["participants"].append(user)

        self.base.insertNewTour(tour)

    # Un - pariticpation callback
    def unparticipateCallback(self, tour : dict):

        # Add user to given unique ident
        user = st.session_state["login"]["credents"]["user"]
        tour["participants"] = [p for p in tour["participants"] if p != user]

        self.base.insertNewTour(tour)
