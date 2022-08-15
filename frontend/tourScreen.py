import traceback
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

        # tabs for general tours own tours and participated tours
        tabs = st.tabs(["all", "own tours", "next tours", "vicinity"])

        # Tab all tours
        with tabs[0]:
            # Head line
            self.headLine()

            # All known tours
            allTours = self.listTours()
        
        # Tab my genereated Tours
        with tabs[1]:
            if st.session_state["login"]["role"] == "guide":
                # all tours by owner
                self.listToursOwner(allTours)

        # list all tours where the user participate
        with tabs[2]:
            self.listToursParticipant(allTours)

        # Find tours in vicinity
        with tabs[3]:
            pass

        # Refresh and logout for each tab
        cols = st.columns([0.05, 1, 0.05])
        cols[0].button("Refresh", key="refreshButton")
        cols[-1].button("Logout", key="logoutButton", on_click=self.logoutCallback)

    # Head line
    def headLine(self):
        # Head line Columns for ordering
        cols = st.columns([0.3 ,1, 0.3])

        # Create new tour
        if st.session_state["login"]["role"] == "guide":
            cols[0].button("Create new", on_click=self.setCreateStateCallback) 
        
        # Open create new tour display after reload
        if "ShowCreateTourWidget" in st.session_state and st.session_state["ShowCreateTourWidget"]:
            self.createTour()
        
    # Callback if a new tour is in creation mode
    def setCreateStateCallback(self):
         # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = True

    # List all known tours
    def listTours(self) -> list:
        # load all existing tours
        tours = self.base.loadTours()

        # build tours
        for tour in tours:
            try:
                self.tourWidget.tourWidget(tour, "all")

            except:
                print(traceback.print_exc())
                print("Eine Tour konnte nicht geladen werden!")
        
        # Returning tours for tab particpate tours
        return tours
        
    # list all tours of the owner
    def listToursOwner(self, allTours:list):
        owner = st.session_state["login"]["credents"]["user"]

        # load tours
        tours = [tour for tour in allTours if tour["owner"] == owner]

         # build tours
        for tour in tours:
            try:
                self.tourWidget.tourWidget(tour, "owner")

            except:
                print(traceback.print_exc())
                print("Eine Tour konnte nicht geladen werden!")
        
    # list all tours with the owner as participant:
    def listToursParticipant(self, allTours:list):
        # the logged in user
        user = st.session_state["login"]["credents"]["user"]

        # subset of the all tours
        tours = [tour for tour in allTours if user in tour["participants"]]
        
         # build each tour
        for tour in tours:
            try:
                self.tourWidget.tourWidget(tour, "participate")
            except:
                print(traceback.print_exc())

    # create new tour
    def createTour(self):
        # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = True

        # Creation Widget
        with st.expander("create new tour", expanded = True):
            tourAttr = self.tourWidget.createWidget()

            # button options: save and discard
            cols = st.columns([0.3, 1, 0.3])

            # Save tour
            cols[0].button("Save",  on_click=self.saveTourCallback, args=(tourAttr,))

            # discard a tour in creation
            cols[-1].button("discard", on_click=self.discardTourCallback)

    # Callback to sava a created tour
    def saveTourCallback(self, tourAttr : dict):
        self.base.insertNewTour(tourAttr)

        st.success("New tour created")

         # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = False

    # Callback to discard a created tour
    def discardTourCallback(self):
         # Set state for reopening create tour widget
        st.session_state["ShowCreateTourWidget"] = False

    # Logout Callback
    def logoutCallback(self):
        # reset login state
        del st.session_state["login"]

