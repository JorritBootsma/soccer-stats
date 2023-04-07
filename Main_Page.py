import yaml
from yaml.loader import SafeLoader

import streamlit as st
import streamlit_authenticator as stauth

import style_config
from helper_funcs.streamlit_components import insert_page_heading

st.set_page_config(
    page_title=style_config.page_titles,
    page_icon=style_config.page_favicon
)

insert_page_heading("# 🏟️ Main page", style_config.page_favicon)

# st.sidebar.markdown("# 🏟️ Main page")
st.sidebar.image(style_config.page_favicon)

st.markdown(
    """
    Welcome to your Soccer Buddy! _The_ place the organise your soccer stats. \n
    """
)
st.write(" ")

# Do login
with open('configs/users.yaml') as file:
    users = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    users['credentials'],
    users['cookie']['name'],
    users['cookie']['key'],
    users['cookie']['expiry_days'],
    users['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    st.session_state["team"] = users["credentials"]["usernames"][username]["team"]

    st.markdown("###### Your team ")
    st.write(st.session_state["team"])
    authenticator.logout('Logout', 'main')
    st.markdown("⬅️ Select your desired page using the sidebar.")
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
