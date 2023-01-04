import streamlit as st

import api_requests
from helper_funcs.general_funcs import response_to_json
import schemas

st.markdown("# 🏃 Player Stats")
st.write("---")
st.sidebar.markdown("# 🏃 Player Stats")


# Load all players from database
response_players = api_requests.get_all_players()
response_players = response_to_json(response_players)
players = [schemas.Player(**player) for player in response_players]

with st.form("Get Information Of Specific Player"):
    st.write("##### Get Info of Specific Player")
    index = int(st.text_input("Index in players list (8 = ijsbrand)", value=8))
    player = players[index]
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(player)
        response = api_requests.get_player_with_performance(player)

        if 'ERROR' in response.json():
            st.error(response.json())
        else:
            st.write(response)
            test_players = response_to_json(response)
            st.write(test_players)