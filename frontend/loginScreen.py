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
        # Check the login state
        if "login" not in st.session_state or st.session_state["login"]["state"] not in ["success", "register"]:
            with st.container():
                credents = {}

                # Login Credentials 
                credents["user"] = st.text_input("Username or Email", key="loginUser")
                credents["password"] = st.text_input("Password", type="password", key="loginPass")

                # Login with credentials or switch to registration
                # columns for buttons
                cols = st.columns([0.3, 1, 0.3])

                cols[0].button("Login", on_click=self.stateCallback, args=(credents, ), key="loginBut")  

                # Registerbutton
                cols[-1].button("Register now", on_click=self.registerCallback, key="registerButEntry") 

    # Registration 
    def register(self):

        # Create regestration credentials 
        credentsNew = {}
        credentsNew["email"] = st.text_input("Email", key="registerMail")
        credentsNew["user"] = st.text_input("Username", key="registerUser")
        credentsNew["password"] = st.text_input("Password", type="password", key="registerPass")

        # Enter the role 
        cols = st.columns(2)
        roleMember = cols[0].checkbox("Tourmember", value = True, help="If you only want to join a tour", key="registerMember") # default
        roleGuide = cols[1].checkbox("Tourguide", value = False, help="If you want to join and create a tour", key="registerGuide")

        # set the role value
        credentsNew["role"] = "guide" if roleGuide else "member"

        # following buttons
        cols = st.columns(3)

        # send register credentials
        cols[0].button("Register", on_click=self.sendRegisterCallback, key="registerButton", args=(credentsNew, ))

        # back to login
        cols[-1].button("Back to Login", on_click=self.unregisterCallback, key="registerCredentsButton")

    # Set login state if credentials are correct
    def stateCallback(self, credents: dict):
        # check if user and password is correct
        message, role = self.base.loginUserCheck(credents)
        if len(message) > 0:
            st.error(message)
        else:
            st.session_state["login"] = {"credents": credents, "state": "success", "role": role}

    # Register callback
    def registerCallback(self):
        # set register state
        st.session_state["login"] = {"state": "register"}
    
    # Back to login callback
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

