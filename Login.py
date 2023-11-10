import yaml
from yaml.loader import SafeLoader

import streamlit as st
import streamlit_authenticator as stauth

import api_requests
import style_config
from helper_funcs.general_funcs import response_to_json
from helper_funcs.streamlit_components import insert_page_heading
import schemas

st.set_page_config(
    page_title=style_config.page_titles, page_icon=style_config.page_favicon
)

insert_page_heading("# Welcome to Soccer Buddy", style_config.page_favicon)

# st.sidebar.markdown("# 🏟️ Main page")
st.sidebar.image(style_config.page_favicon)

st.write("---")
st.markdown("Your Soccer Buddy. _The_ place the organise your soccer stats.")

# Load credentials from file
with open("configs/users.yaml") as file:
    users = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    users["credentials"],
    users["cookie"]["name"],
    users["cookie"]["key"],
    users["cookie"]["expiry_days"],
    users["preauthorized"],
)

# Hardcode Logout when wrong user logged in
# authenticator.logout("Logout_", "main")

name, authentication_status, username = authenticator.login("Login", "main")
if authentication_status:
    team_name = users["credentials"]["usernames"][username]["team"]

    response_teams = api_requests.get_all_teams()
    response_teams = response_to_json(response_teams)
    teams = [schemas.Team(**team) for team in response_teams]

    st.session_state["team"] = [
        schemas.Team(**team)
        for team in response_teams
        if schemas.Team(**team).club == team_name
    ]
    if st.session_state["team"]:
        st.session_state["team"] = st.session_state["team"][0]
    else:
        st.write("No team found for this user.")

    st.markdown(f"###### Welcome:  {username.capitalize()}")
    st.markdown(f"###### Your team: {st.session_state['team'].club}")
    st.markdown("⬅️ Select your desired page using the sidebar.")
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    empty_col, logout_col = st.columns([10, 2])
    with logout_col:
        authenticator.logout("Logout", "main")
