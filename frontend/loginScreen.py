import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

import streamlit as st

from config import Configurator


class Login:
    def __init__(self) -> None:
        self.config = Configurator()

    def loginOrRegister(self):
        # Login 
        self.login()

        # if register new is already choosen
        if "login" in st.session_state and st.session_state["login"]["state"] == "register":
            self.register()
        
    def login(self):
        if "login" not in st.session_state or st.session_state["login"]["state"] not in ["success", "register"]:
            credents = {}

            # Tab1: Login Credentials 
            credents["user"] = st.text_input("Username or Email", key="loginUser")
            credents["password"] = st.text_input("Password", type="password", key="loginPass")

            # Missing ROLE 
            credents["role"] = "guide"

            # columns for buttons
            cols = st.columns(3)

            cols[0].button("Login", on_click=self.stateCallback, args=(credents, ), key="loginBut")  # missing: roles

            # Register
            cols[2].button("Register now", on_click=self.registerCallback, key="registerButEntry")

    def register(self):

        # Tab2: Register new 
        credentsNew = {}
        credentsNew["email"] = st.text_input("Email", key="registerMail")
        credentsNew["user"] = st.text_input("Username", key="registerUser")
        credentsNew["password"] = st.text_input("Password", type="password", key="registerPass")

        # following buttons
        cols = st.columns(3)

        # send register credentials
        registerBut = cols[0].button("Register", on_click=self.sendRegisterCallback, key="registerButton")

        # back to login
        cols[-1].button("Back to Login", on_click=self.unregisterCallback, key="registerCredentsButton")

    # Set Login state
    def stateCallback(self, credents: dict):
            st.session_state["login"] = {"credents": credents, "state": "success", "role": credents["role"]}

    # Register Callback
    def registerCallback(self):
        # set register state
        st.session_state["login"] = {"state": "register"}
    
    # Back to Login callback
    def unregisterCallback(self):
        # set register state
        st.session_state["login"] = {"state": "login"}

    # Send register callback for credentials
    def sendRegisterCallback(self):
        st.write("MISSING: Register")