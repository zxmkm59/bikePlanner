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
            data.append([point.longitude, point.latitude, point.elevation])  # ,point.elevation

        cols = ["longitude", "latitude", "elevation"]

        df = pd.DataFrame(data, columns=cols)

        #st.map(df)
        ds = df.to_dict('series')
        ds = {k:list(ds[k]) for k in ds}

        import plotly.graph_objects as go

        fig 

        print(ds.keys())

        



    # streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/Spielwiese3.py