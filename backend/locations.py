import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator

class Location:
    def __init__(self) -> None:
        self.config = Configurator()

    # get the current location
    def getLocation(self):
        loc_button = Button(label="Get Location")
        loc_button.js_on_event("button_click", CustomJS(code="""
            navigator.geolocation.getCurrentPosition(
                (loc) => {
                    document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
                }
            )
            """))

        result = None
        result = streamlit_bokeh_events(
                loc_button,
                events="GET_LOCATION",
                key="get_location",
                refresh_on_update=False,
                override_height=75,
                debounce_time=0)

        if result:
            if "GET_LOCATION" in result:
                print(result.get("GET_LOCATION"))

if __name__ == "__main__":
    l = Location()
    l.getLocation()