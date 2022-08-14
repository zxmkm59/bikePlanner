import datetime
import uuid
import streamlit as st
import sys

#sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

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
    def tourWidget(self, tour):

        # starttime of the tour
        date = datetime.datetime.fromtimestamp(tour['date'])

        # build a title from the date and custom title name
        title = f"{date} | {tour['title']} | {tour['owner']}"

        # widget
        with st.expander(title, expanded = False):
            
            # Header 
            headCols = st.columns(3)
            headCols[0].metric(label="Starttime", value=str(date))
            headCols[1].metric(label="Startplace", value=tour["startplace"]) 
            headCols[2].metric(label="Guide", value=tour["owner"]) 
            st.write("---")

            # Second
            self.addCaption(f"Participants ({len(tour['participants'])})")
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

            # The 

    # build widget for new tour creation
    def createWidget(self):
        with st.container():
            tourAttr = {}

            # Title
            tourAttr["title"] = st.text_input("Title")

            # Header
            headCols = st.columns(3)
            date = headCols[0].date_input("start date", min_value=datetime.datetime.today())
            time_of_date = headCols[1].time_input("start time")
            tourAttr["date"] = datetime.datetime.combine(date, time_of_date).timestamp()

            tourAttr["startplace"] = headCols[2].text_input(label="start place")

            # Second 
            cols2 = st.columns(3)
            for i, at in enumerate(sorted(self.attributes)):
                j = helpMod(i, 3)
                tourAttr[at] = cols2[j].text_input(label=at)

            # Add Gpx import and viewer
            gpxCols = st.columns([1,4,1])
            with gpxCols[1]:
                tourAttr["gpx"] = self.gpx.addGpx()

            # Add unique key
            tourAttr["unique"] = str(uuid.uuid1())

            # Add the autor:
            tourAttr["owner"] = st.session_state["login"]["credents"]["user"]

            # participants empty at beginning
            tourAttr["participants"] = []
    
        return tourAttr


    # Add a caption statement
    def addCaption(self, txt: str):
        colsCaption = st.columns([1,0.5,1])
        colsCaption[1].caption(txt)

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
