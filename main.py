import sys
import streamlit as st

sys.path.append("C:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/frontend/")
sys.path.append("/app/frontend")

from mainScreen import MainScreen

# Initial set parameters for the side
if "pageConfigSetted" not in st.session_state:
    """    st.set_page_config(
        page_title="Bike planer",
        page_icon="🧊",
        layout="wide"
    )"""
    st.session_state["pageConfigSetted"] = True


if __name__ == "__main__":
    m = MainScreen()
    m.mainPage()

    # streamlit run c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/main.py