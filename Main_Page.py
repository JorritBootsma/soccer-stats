import streamlit as st

import api_requests
from helper_funcs.general_funcs import response_to_json
import schemas

st.markdown("# Main page 🏟️")
st.sidebar.markdown("# Main page 🏟️")

st.markdown(
    """
    Welcome to the Soccer Stats application. Select your desired page using the sidebar.
    """
)

response_teams = api_requests.get_all_teams()
response_teams = response_to_json(response_teams)
teams = [schemas.Team(**team) for team in response_teams]
OUR_TEAM = [team for team in teams if team.club == "WV-HEDW Zon. 9"][0]

st.write(" ")
st.write(" ")
st.write(" ")

st.markdown("###### Your team ")
st.write(OUR_TEAM)
st.write("⬆️ This will be taken from login details and should be available throughout the application")