import datetime
import uuid
import streamlit as st

from config import Configurator
from gpxReader import GpxViewer

# helper: modulo
def helpMod(x, num):
    while x >= num:
        x -= num
    return x

class TourWidget:
    def __init__(self, base) -> None:
        # Other instances
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
                      "climbs": "count"}

    # build tour widget
    def tourWidget(self, tour:dict, typ:str):

        # starttime of the tour
        date = datetime.datetime.fromtimestamp(tour['date'])

        # build a title from the date and custom title name
        title = f"{date} | {tour['title']} | {tour['owner']}"

        # widget
        with st.expander(title, expanded = False):
            
            # Organisation Attributes 
            # ------------------------------------------------------------------------
            self.addCaption("Organisation")
            headCols = st.columns(3)

            headCols[0].write("Starttime")
            headCols[1].write("Startplace")
            headCols[2].write("Guide")

            headCols[0].write(str(date))
            headCols[1].write(tour["startplace"])
            headCols[2].write(tour["owner"])

            st.write("---")
            # ------------------------------------------------------------------------

            # Participants
            # ------------------------------------------------------------------------
            self.addCaption(f"Participants ({len(tour['participants'])})")
            colNum = min(len(tour['participants']), 8) 
            cols2_1 = st.columns([0.05 if colNum > 0 else 1 for i in range(colNum)] + [1])
            
            for i, p in enumerate(tour["participants"]):
                j  = helpMod(i, colNum)
                #cols2_1[j].write(p)
                cols2_1[j].button(label=p, key=f"{p}_{tour['unique']}_{typ}", disabled=True)

            # add participate option
            self.participate(tour, typ)
            st.write("---")
        
            # ------------------------------------------------------------------------

            # Sum overall
            # ------------------------------------------------------------------------
            self.addCaption("The hard facts")
            cols3 = st.columns(3)
            for i, at in enumerate(self.units):
                j = helpMod(i, 3)
                cols3[j].metric(label=at, value= f"{tour[at]} {self.units[at]}")
            st.write("---")
            # ------------------------------------------------------------------------

            #  GPX Data
            # ------------------------------------------------------------------------
            self.addCaption("GPX")
            gpxCols = st.columns([1,4,1])
            with gpxCols[1]:
                gpxData = tour["gpx"]

                self.gpx.showGpx(gpxData)
            # ------------------------------------------------------------------------

            # Comments if comments inserted by the owner
            # ------------------------------------------------------------------------
            if len(tour["comments"]) > 0:
                st.write("---")
                self.addCaption("Comments")

                st.write(tour["comments"])
            # ------------------------------------------------------------------------


            # Editing
            # ------------------------------------------------------------------------
            if st.session_state["login"]["credents"]["user"] == tour["owner"]:
                st.write("---")
                self.addCaption("Editing")
                cols4 = st.columns(3)
                cols4[-1].button(label="Delete this tour", on_click=self.deleteCallback, args=(tour, ), key=f"delete_{tour['unique']}_{typ}")

    # build widget for new tour creation
    def createWidget(self):
        with st.container():
            # initials
            tourAttr = {}  # collect tour attributes
            tempGpx = {}  # collect gpx calculated attributes
            
            # Organisation Attributes 
            # ------------------------------------------------------------------------
            # Title
            # Placeholder to overwrite if gpx is uploaded
            titlePlace = st.empty()
            tourAttr["title"] = titlePlace.text_input("Title", key="titleUserInput")

            # default title if no title inserted
            tourAttr["title"] = "no title" if len(tourAttr["title"]) == 0 else tourAttr["title"]

            # Header
            headCols = st.columns(3)
            date = headCols[0].date_input("start date", min_value=datetime.datetime.today())
            time_of_date = headCols[1].time_input("start time")
            tourAttr["date"] = datetime.datetime.combine(date, time_of_date).timestamp()

            tourAttr["startplace"] = headCols[2].text_input(label="start place")
            st.write("---")
            # ------------------------------------------------------------------------

            # GPX
            # ------------------------------------------------------------------------
            # Add Gpx import and viewer
            gpxCols = st.columns([1,4,1])
            with gpxCols[1]:
                tourAttr["gpx"], title = self.gpx.addGpx()

                # overwrite title with gpx name
                tourAttr["title"] = titlePlace.text_input("Title", value=title, key="titleGpxInput")

                # Calculate some hard facts from gpx data
                if len(tourAttr["gpx"])> 0 :
                    tempGpx = self.gpx.calcFromGpx(tourAttr["gpx"])
            st.write("---")
            # ------------------------------------------------------------------------

            # Hard Facts
            # ------------------------------------------------------------------------
            # Write hard facts (or reuse from gpx data befor) 
            cols2 = st.columns(3)
            for i, at in enumerate(sorted(self.attributes)):
                j = helpMod(i, 3)

                # is there a value from inserting gpx data ?
                value = tempGpx[at] if at in tempGpx else ""

                # the label contains the name and unit
                label = f"{at} [{self.units[at]}]"

                tourAttr[at] = cols2[j].text_input(label=label, value = value)
            # ------------------------------------------------------------------------

            # Comments 
            # ------------------------------------------------------------------------
            st.write("---")
            tourAttr["comments"] = st.text_area(label="Comments")
            # ------------------------------------------------------------------------
            
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
    def participate(self, tour:dict, typ:str):
        # Add participation option
        cols = st.columns(5)
        user = st.session_state["login"]["credents"]["user"]

        # no option if tour owner and user are the same
        if tour["owner"] == user:
            return

        # Check if is already a participant
        if user in tour["participants"]:  # already participant
            cols[-1].button("unparticipate", on_click = self.unparticipateCallback, args=(tour.copy(), ), key=str(tour["unique"]) + "unparticipate" + typ)
        else:  # not participant
            cols[-1].button("participate", on_click = self.participateCallback, args=(tour.copy(), ) ,key=str(tour["unique"]) + "participate" + typ)

    # Pariticpation callback
    def participateCallback(self, tour : dict):

        # Add user to given unique ident
        user = st.session_state["login"]["credents"]["user"]
        tour["participants"].append(user)

        # Create a new tour with more participants
        self.base.insertNewTour(tour)

    # Un - pariticpation callback
    def unparticipateCallback(self, tour : dict):

        # Add user to given unique ident
        user = st.session_state["login"]["credents"]["user"]
        tour["participants"] = [p for p in tour["participants"] if p != user]

        # Create a new tour with less participants
        self.base.insertNewTour(tour)

    # Delete tour as owner callback
    def deleteCallback(self, tour):
        self.base.deleteTour(tour["unique"])

    # TODO: Vicinity 
    def vicinity(self):
        pass