"""path = "C:\\Users\\tobia\\OneDrive\\Desktop\\1108.gpx"

from xml.dom import minidom

fileIn = open(path)

xmldoc = minidom.parse(fileIn)
track = xmldoc.getElementsByTagName('trkpt')
elevation=xmldoc.getElementsByTagName('ele')
datetime=xmldoc.getElementsByTagName('time')
n_track=len(track)
lon_list=[]
lat_list=[]
h_list=[]
time_list=[]
for s in range(n_track):
    lon,lat=track[s].attributes['lon'].value,track[s].attributes['lat'].value
    elev=elevation[s].firstChild.nodeValue
    lon_list.append(float(lon))
    lat_list.append(float(lat))
    h_list.append(float(elev))
    # PARSING TIME ELEMENT
    dt=datetime[s].firstChild.nodeValue
    time_split=dt.split('T')
    hms_split=time_split[1].split(':')
    time_hour=int(hms_split[0])
    time_minute=int(hms_split[1])
    time_second=int(hms_split[2].split('Z')[0])
    total_second=time_hour*3600+time_minute*60+time_second
    time_list.append(total_second)
#print(elevation)

fileIn.close()"""




if __name__ == "__main__":
    import gpxpy 
    import streamlit as st
    import pandas as pd

    file = st.file_uploader("Upload", type =["gpx"], accept_multiple_files=False)
    if file is not None:
        gpx = gpxpy.parse(file)

        track=gpx.tracks[0]

        segment = track.segments[0]

        segment_length = segment.length_3d()

        lats, longs, els = [], [], []
        data = []
        for pooint_idx, point in enumerate(segment.points):
            data.append([point.longitude, point.latitude])  # ,point.elevation

        cols = ["longitude", "latitude"]

        df = pd.DataFrame(data, columns=cols)

        st.map(df)

        



    # streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/Spielwiese3.py