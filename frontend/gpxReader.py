import numpy as np
import gpxpy 
import streamlit as st
import pandas as pd
import sys
import plotly.graph_objects as go

#sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

from config import Configurator

class GpxViewer:
    def __init__(self) -> None:
        self.config = Configurator()

    # Import a gpx and show whats imported
    def addGpx(self):
        # initial for output format
        ds = {}

        # Input new gpx file
        file = st.file_uploader("Upload", type =["gpx"], accept_multiple_files=False)

        if file is not None:
            gpx = gpxpy.parse(file)

            # convert to dataframe
            df = self.parseGpx(gpx)

            # show imported gpx
            self.showGpx(df)

            # convert to databse datatype
            ds = df.to_dict('series')
            # convert to list from np.arrays
            ds = {k:list(ds[k]) for k in ds}

        return ds

    # plot a gpx in dataframe format
    def showGpx(self, df: pd.DataFrame or dict):

        # Convert if necessary
        if isinstance(df, dict):
            df = pd.DataFrame.from_dict(df)

        # 1. Show Geo
        st.map(df)

        # 2. Show elevation
        fig = self.elevationChart(df)
        st.plotly_chart(fig, use_container_width=True, sharing ="streamlit")

    # create a elevation chart
    def elevationChart(self, df: pd.DataFrame):
        x=df["distance"].values.tolist()
        y=df["elevation"].values.tolist()
        s=df["slope"].values.tolist()

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

        fig.update_xaxes(
            tickangle = 90)

        return fig

    # parse a gpx with one track to a dataframe
    def parseGpx(self, gpx) -> pd.DataFrame:
        track=gpx.tracks[0]

        segment = track.segments[0]

        distances = []  # distances acc.
        spaces = []     # only spaces between points 
        p0 =  segment.points[0]
        for p in segment.points:
            d0 = distances[-1] if len(distances) > 0 else 0
            distances.append(d0 + p0.distance_2d(p))
            spaces.append(p0.distance_2d(p))
            p0 = p

        # calculate in km
        distances = [d/1000 for d in distances]

        # calculate slope
        slope = [0] + list(np.diff([point.elevation for point in segment.points]))
        slope = [s/(d)*100 if d > 0 else 0 for s, d in zip(slope, spaces)]

        data = [[point.longitude, point.latitude, point.elevation, dist, sl] for point, dist, sl in zip(segment.points, distances, slope)]

        cols = ["longitude", "latitude", "elevation", "distance", "slope"]

        return pd.DataFrame(data, columns=cols)


if __name__ == "__main__":
    g = GpxViewer()
    g.addGpx()

    # streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/frontend/gpxReader.py