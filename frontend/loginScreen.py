import sys

sys.path.append("c:/Users/tobia/OneDrive/Desktop/Programming/cyclePlanner/")

import streamlit as st

from config import Configurator


class Login:
    def __init__(self, base) -> None:
        self.config = Configurator()

        self.base = base

    def loginOrRegister(self):
        # Login 
        self.login()

        # if register new is already choosen
        if "login" in st.session_state and st.session_state["login"]["state"] == "register":
            self.register()
        
    def login(self):
        if "login" not in st.session_state or st.session_state["login"]["state"] not in ["success", "register"]:
            with st.container():
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
        registerBut = cols[0].button("Register", on_click=self.sendRegisterCallback, key="registerButton", args=(credentsNew, ))

        # back to login
        cols[-1].button("Back to Login", on_click=self.unregisterCallback, key="registerCredentsButton")

    # Set Login state
    def stateCallback(self, credents: dict):
        # check if user and password is correct
        message = self.base.loginUserCheck(credents)
        if len(message) > 0:
            st.error(message)
        else:
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
    def sendRegisterCallback(self, credents):
        message = self.base.registerUser(credents)

        # Print message if possible
        if len(message) > 0:
            st.error(message)
        else:
            # Back to Login
            self.unregisterCallback()
            st.success("Registered successfully")

