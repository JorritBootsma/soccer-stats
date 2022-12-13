import json
import math

import datetime
import streamlit as st

import api_requests
from helper_funcs.general_funcs import response_to_json
import schemas

# ######## These are now loaded from the database #########
# TEAMS_CONFIG_PATH = "configs/teams.json"
# PLAYERS_CONFIG_PATH = "configs/players.json"
# opponents = load_json_from_filepath(TEAMS_CONFIG_PATH)["teams"]
# players = load_json_from_filepath(PLAYERS_CONFIG_PATH)["players"]
#
# with st.form("Get all players"):
#     submitted = st.form_submit_button("Get Players!")
#     if submitted:
#         response = api_requests.get_all_players()
#         st.subheader("Response")
#         if 'ERROR' in response.json():
#             st.error(response.json())
#         else:
#             st.write(response.json())
###########################################################

# Load all players from database
response_players = api_requests.get_all_players()
response_players = response_to_json(response_players)
players = [schemas.Player(**player) for player in response_players]
st.write("Player object example: ", players[0])


# Load all teams from database
response_teams = api_requests.get_all_teams()
response_teams = response_to_json(response_teams)
teams = [schemas.Team(**team) for team in response_teams]
st.write("Club object example: ", teams[0])

if "save_match_to_db" not in st.session_state:
    st.session_state["save_match_to_db"] = ""

st.write("### Wedstrijd informatie")
# Match date & time
date, time = st.columns(2)
game_date = date.date_input("Wedstrijddatum")
game_time = time.time_input("Tijd", value=datetime.time(hour=9, minute=0))
# Match opponent
opponent = st.selectbox("Tegenstander", options=teams, format_func=lambda option: option.club)
# Match result
our_goals, hyphen, their_goals = st.columns(3)
num_of_goals = our_goals.text_input("Goals gemaakt")
hyphen.markdown(
    "<h1 style='text-align: center; color: grey;'>-</h1>", unsafe_allow_html=True
)
num_of_opponent_goals = their_goals.text_input("Goals tegen")

st.write("### Aanwezigheid")
col1, col2, col3 = st.columns(3)
active_players = []
n_in_col1 = math.ceil(len(players) / 3)
n_in_col2 = math.ceil(len(players) / 3)
n_in_col3 = len(players) - n_in_col1 - n_in_col2
player_names = []
for idx, player_obj in enumerate(players):
    name = player_obj.name
    player_names.append(name)

    active_players.append(player_obj)
    if idx <= n_in_col1:
        col1.checkbox(name, value=True, key=f"p_{idx}")
    elif idx <= n_in_col1 + n_in_col2 + 1:
        col2.checkbox(name, value=True, key=f"p_{idx}")
    else:
        col3.checkbox(name, value=True, key=f"p_{idx}")

# Give the user the ability to add players other than the ones defined in the
# `player_names.py` config file
unknown_players = True
counter = 0
while unknown_players:
    if counter == 0:  # Show labels above the first row
        unknown_players = st.text_input(
            "Deden er invallers mee?", key=f"invaller_{counter}"
        )
    else:  # Do not show labels above the next rows
        unknown_players = st.text_input(
            "Deden er invallers mee?",
            key=f"invaller_{counter}",
            label_visibility="collapsed",
        )

    counter += 1

st.write(st.session_state)

# Extract the active players from the session_state using
active_players = [
    players[int(player_idx[2:])]
    for player_idx, active in st.session_state.items()
    if "p_" in player_idx and active
]
other_players = [
    other_player_name
    for other_player_idx, other_player_name in st.session_state.items()
    if "invaller_" in other_player_idx and other_player_name != ""
]

# Add the `invallers` to the list of active players
active_players = active_players + other_players

st.write("### Doelpuntenmakers")
if not num_of_goals:  # Before specifying, the number of scored goals need to be inserted
    st.warning(
        "Selecteer doelpuntenmakers nadat je de eindstand bovenaan hebt ingevoerd."
    )
else:  # When the number of goals are inserted, show this amount of rows to specify the goals
    goal, assist, body_part, in_out_box, penalty = st.columns(5)
    for idx, _ in enumerate(range(int(num_of_goals))):
        if idx == 0:  # Only show labels above the first row
            goal.selectbox(
                "Doelpuntenmaker",
                options=active_players,
                key=f"goal_{idx}",
                format_func=lambda option: option.name
            )
            assist.selectbox(
                "Assist",
                options=["Assistloos"] + active_players,
                key=f"assist_{idx}",
                format_func=lambda option: None if option == "Assistloos" else option.name
            )
            body_part.selectbox(
                "Lichaamsdeel", options=["R", "L", "Hoofd"], key=f"body_part_{idx}"
            )
            in_out_box.selectbox(
                "Binnen of buiten 16m", options=["Binnen", "Buiten"], key=f"box_{idx}"
            )
            penalty.selectbox(
                "Pingel?",
                options=["Ja", "Nee"],
                format_func=lambda option: True if option == "Ja" else False,
                key=f"penalty_{idx}",
            )
        else:  # Do not show labels above the next rows
            goal.selectbox(
                "Doelpuntenmaker",
                options=active_players,
                key=f"goal_{idx}",
                label_visibility="collapsed",
                format_func=lambda option: option.name
            )
            assist.selectbox(
                "Assist",
                options=["Assistloos"] + active_players,
                key=f"assist_{idx}",
                label_visibility="collapsed",
                format_func=lambda option: None if option == "Assistloos" else option.name
            )
            body_part.selectbox(
                "Lichaamsdeel",
                options=["R", "L", "Hoofd"],
                key=f"body_part_{idx}",
                label_visibility="collapsed",
            )
            in_out_box.selectbox(
                "Binnen of buiten 16m",
                options=["Binnen", "Buiten"],
                key=f"box_{idx}",
                label_visibility="collapsed",
            )
            penalty.selectbox(
                "Pingel?",
                options=["Ja", "Nee"],
                key=f"penalty_{idx}",
                label_visibility="collapsed",
            )


st.write("### Panna's")
panna_player, panna_type = st.columns(2)
x = True
y = True
counter = 0
panna_players = []
panna_types = []
while x and y:
    x = panna_player.selectbox(
        "Pannagever", [""] + active_players, key=f"panna_gever_{counter}"
    )
    y = panna_type.selectbox(
        "Panna type",
        [""] + ["Zakelijk", "Vies", "Murderous"],
        key=f"panna_type_{counter}",
    )
    counter += 1
    panna_players.append(panna_player)
    panna_types.append(panna_type)

st.write("### Penalties gestopt")
penalties_boolean = st.checkbox("Heeft onze keeper penalties gestopt?")
if penalties_boolean:
    penalties_stopped = st.text_input("Vul hier het aantal in")
else:
    penalties_stopped = None

st.write("### Derde helft")
third_half = st.multiselect(
    "Wie hebben de deur op slot gedaan bij de club?", active_players
)

st.write("---")

# Button to persist the information in the database
store_button = st.button(
    "Write to database!",
    on_click=api_requests.send_to_database,
    args=[st.session_state],
)

if store_button:
    st.warning(st.session_state["save_match_to_db"])

with st.form("Create Player"):
    name = st.text_input("Player name")
    birth_date = st.text_input("Birth date (in yyyy-mm-dd)")
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = api_requests.create_player(name, birth_date)
        st.subheader("Response")
        if 'ERROR' in response.json():
            st.error(response.json())
        else:
            st.write(response.json())


with st.form("Create Team"):
    name = st.text_input("Team name")
    submitted = st.form_submit_button("Submit Team")
    if submitted:
        response = api_requests.create_team(name)
        st.subheader("Response")
        if 'ERROR' in response.json():
            st.error(response.json())
        else:
            st.write(response.json())


with st.form("Create Card"):
    name = st.text_input("Card type")
    submitted = st.form_submit_button("Submit Card")
    if submitted:
        response = api_requests.create_card(name)
        st.subheader("Response")
        if 'ERROR' in response.json():
            st.error(response.json())
        else:
            st.write(response.json())


with st.form("Create Goal"):
    goal_scorer = st.text_input("Goal scorer")
    assist_giver = st.text_input("Assist giver")
    body_part = st.selectbox("Body part", options=["Left foot", "Right foot", "Header"])
    half = st.selectbox("Half", options=['First half', 'Second half'])
    submitted = st.form_submit_button("Submit Goal")
    if submitted:
        response = api_requests.create_goal(goal_scorer, assist_giver, body_part, half)
        st.subheader("Response")
        if 'ERROR' in response.json():
            st.error(response.json())
        else:
            st.write(response.json())


with st.form("Create Match"):
    match_date = st.text_input("Date")
    season = st.selectbox("Season", options=["2021/2022", "2022/2023"])
    home_team = st.selectbox("Home team", options=["A", "B", "C"])
    away_team = st.selectbox("Away team", options=['A', 'B', "C"])
    their_goals = st.text_input("Their goals")
    players_present = st.multiselect("Players", options=["Anna", "Bob", "Charlotte"])
    submitted = st.form_submit_button("Submit Match")
    if submitted:
        # response = api_requests.create_match(name)
        # st.subheader("Response")
        # if 'ERROR' in response.json():
        #     st.error(response.json())
        # else:
        #     st.write(response.json())
        pass


st.write("---")
st.write("To **delete** all data and re-initialize the tables: type 'reset all tables' in the textbox")
reset_all_tables = st.text_input(
    "Reset Tables",
)
if reset_all_tables == "reset all tables":
    api_requests.initialize_tables()
    st.error("All tables are deleted and re-created using `initial_load.py`")
