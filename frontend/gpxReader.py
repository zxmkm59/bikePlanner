import numpy as np
import gpxpy 
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config import Configurator

class GpxViewer:
    def __init__(self) -> None:
        self.config = Configurator()

    # Import a gpx and show whats imported
    def addGpx(self):
        # initial for output format
        ds = {}
        fileName = ""

        # Input new gpx file
        file = st.file_uploader("Upload", type =["gpx"], accept_multiple_files=False)

        if file is not None:
            gpx = gpxpy.parse(file)
            
            fileName = file.name.replace(".gpx", "")

            # convert to dataframe
            df = self.parseGpx(gpx)

            # show imported gpx
            self.showGpx(df)

            # convert to databse datatype
            ds = df.to_dict('series')

            # convert to list from np.arrays
            ds = {k:list(ds[k]) for k in ds}

        return ds, fileName

    # plot a gpx in dataframe format
    def showGpx(self, df: pd.DataFrame or dict):

        # Convert if necessary
        if isinstance(df, dict):
            df = pd.DataFrame.from_dict(df)

        # 1. Show geo map 
        st.map(df)

        # 2. Show elevation chart
        fig = self.elevationChart(df)
        st.plotly_chart(fig, use_container_width=True, sharing ="streamlit")

    # create a elevation chart
    def elevationChart(self, df: pd.DataFrame) -> go.Figure:
        # convert to list for figure
        x=df["distance"].values.tolist()
        y=df["elevation"].values.tolist()
        s=df["slope"].values.tolist()

        # create go chart
        fig = go.Figure(data=[go.Scatter(x=x, 
                                        y=y,
                                        text=s,
                                        hovertemplate =
                                            'Elevation: %{y:.2f} hm'+
                                            '<br>Distance: </b>: %{x:.2f} km<br>'+
                                            'Slope: %{text:.1f} %' +
                                            '<extra></extra>',
                                            )
                            ]
                            )
                        
        # Some layout specials
        fig.update_layout(
                #hovermode='x unified',
                title="Elevation profile",
                xaxis_title="Distance [km]",
                yaxis_title="Elevation [hm]",
                font=dict(
                    family="Courier New, monospace",
                    size=20,
                    color="white"
                )
            )

        # Set x axe angle for ticks
        fig.update_xaxes(
            tickangle = 90)

        return fig

    # parse a gpx with one track to a dataframe
    def parseGpx(self, gpx) -> pd.DataFrame:
        # Extract gpx data
        track=gpx.tracks[0]
        segment = track.segments[0]

        # intital: collect values
        distances = []  # distances accumlated
        spaces = []     # only spaces between points 

        # Calculate between points
        p0 =  segment.points[0]
        for p in segment.points:
            d0 = distances[-1] if len(distances) > 0 else 0

            # Space between following points
            spaces.append(p0.distance_2d(p))

            # Accumulated distance to this point
            distances.append(d0 + p0.distance_2d(p))

            p0 = p

        # calculate in km
        distances = [d/1000 for d in distances]

        # calculate slope
        slope = [0] + list(np.diff([point.elevation for point in segment.points]))
        slope = [s/(d)*100 if d > 0 else 0 for s, d in zip(slope, spaces)]

        # prepare for Dataframe
        data = [[point.longitude, point.latitude, point.elevation, dist, sl] for point, dist, sl in zip(segment.points, distances, slope)]

        cols = ["longitude", "latitude", "elevation", "distance", "slope"]

        return pd.DataFrame(data, columns=cols)

    # Calculate hard facts from gpx data
    def calcFromGpx(self, gpxData: dict):

        gpxFacts = {"distance": int(gpxData["distance"][-1]),
                    "elevation": int(sum([n for n in np.diff(gpxData["elevation"]) if n > 0])),  # sum up all positive changes of elevation,
                    "startLat": gpxData["latitude"][0],
                    "startLong": gpxData["longitude"][0],
                    }
        return gpxFacts




if __name__ == "__main__":
    g = GpxViewer()
    g.addGpx()

    # streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/frontend/gpxReader.py