import numpy as np
import pandas as pd
import pydeck as pdk
import gpxpy
import streamlit as st

icon_data = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height":128,
    "anchorY": 128
}
file = open("C:\\Users\\tobia\\OneDrive\\Desktop\\1108.gpx", 'r')
gpx = gpxpy.parse(file)

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

df=pd.DataFrame(data, columns=cols)

coordinates = list(zip(df["longitude"], df["latitude"]))

color = "#ffe800"
name = "tour"

df = pd.DataFrame.from_dict({"coordinates": coordinates, "color": color, "name": name})

st.dataframe(df)

icon_data = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height":128,
    "anchorY": 128
}

data = pd.read_json("https://raw.githubusercontent.com/uber-common/deck.gl-data/master/website/bart-stations.json")
df['icon_data']= None

st.dataframe(data)

for i in df.index:
     df['icon_data'][i] = icon_data

view_state = pdk.ViewState(
    longitude=-122.22,
    latitude=37.76,
    zoom=9,
    pitch=50
)

icon_layer = pdk.Layer(
    type='IconLayer',
    data=df,
    get_icon='icon_data',
    get_size=4,
    pickable=True,
    size_scale=15,
    get_position='coordinates'
)
tooltip = {
   "html": "<b>Address:</b> {address} <br/> <b>Station:</b> {name}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}
r = pdk.Deck(layers=[icon_layer], initial_view_state=view_state, tooltip=tooltip)

st.pydeck_chart(r)

# streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/Spielwiese4.py