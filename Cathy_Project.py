import pandas as pd
import streamlit as st

st.title("MAKERERE STUDENT’S ONLINE COMPUTER LAB SYSTEM")

 menu = ["Home", "Admin Login", "Students Login", "SignUp"]
    choice = st.sidebar.selectbox("Makerere University Computer Laboratory "
                                  " Management Sytem", menu)
