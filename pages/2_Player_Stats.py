import pandas as pd
import plotly.express as px
import streamlit as st

import api_requests
import style_config
from helper_funcs.general_funcs import response_to_json
import schemas
from helper_funcs.streamlit_components import insert_page_heading

st.set_page_config(
    page_title=style_config.page_titles,
    page_icon=style_config.page_favicon
)

insert_page_heading("# 🏃 Player Stats", style_config.page_favicon)

st.write("---")
st.sidebar.markdown("# 🏃 Player Stats")

if "team" not in st.session_state:
    st.write("Make sure to login first. Go to the Login page via the sidebar.")
else:
    # Load all players from database
    response_players = api_requests.get_all_players(team=st.session_state["team"])
    response_players = response_to_json(response_players)
    players = [schemas.Player(**player) for player in response_players]

    player = st.selectbox(
        "Van welke speler wil je statistieken zien?",
        options=players,
        format_func=lambda option: option.name,
    )

    response = api_requests.get_player_with_performance(player)
    player_with_performance = response_to_json(response)
    player = schemas.PlayerWithPerformance(**player_with_performance)

    st.markdown("### 🏆️ Presence")
    presence = player.matches_played
    if presence:
        presence_df = pd.DataFrame({
            "match_ids": [match.id for match in presence],
            "Dates": [match.date for match in presence],
            "Presence": [1]*len(presence),
        })
        presence_df.sort_values("Dates", inplace=True)
        presence_df["Presence (cum)"] = presence_df["Presence"].cumsum()
        presence_fig = px.line(
            presence_df,
            x="Dates",
            y="Presence (cum)",
            # title="Presence over time"
        )

        st.plotly_chart(presence_fig)


    st.markdown("### ⚽️ Goals")
    goals = player.goals_scored
    if goals:
        # Get the number of goals scored per match
        individual_goals = [goal.match_id for goal in goals]
        unique_match_ids_w_his_goals = list(set([goal.match_id for goal in goals]))
        num_goals_per_match = {
            match_id: individual_goals.count(match_id)
            for match_id in unique_match_ids_w_his_goals
        }
        num_goals_per_match = dict(sorted(num_goals_per_match.items()))
        # st.write("match_id: num_of_goals")
        # st.write(num_goals_per_match)

        # TODO: Alternatively we could introduce a many-to-many relation between matches
        #  and goals to have the complete match object directly available from a goal object
        # Via the `goal.match_id`, retrieve the `match` object to get the match dates
        response = api_requests.get_all_matches(ids=unique_match_ids_w_his_goals)
        scored_in_matches = response_to_json(response)
        scored_in_matches = [schemas.Match(**match) for match in scored_in_matches]
        dates = [match.date for match in scored_in_matches]

        dates_per_match = {match.id: match.date for match in scored_in_matches}
        dates_per_match = dict(sorted(dates_per_match.items()))
        # st.write("match_id: date")
        # st.write(dates_per_match)

        goals_df = pd.DataFrame({
            "match_ids": dates_per_match.keys(),
            "Dates": dates_per_match.values(),
            "Goals scored": num_goals_per_match.values(),
        })
        goals_df.sort_values("Dates", inplace=True)
        goals_df["Goals scored (cum)"] = goals_df["Goals scored"].cumsum()
        goals_fig = px.line(
            goals_df,
            x="Dates",
            y="Goals scored (cum)",
            # title="Goals scored time"
        )

        st.plotly_chart(goals_fig)

    st.markdown("### 👞 Assists")
    assists = player.assists_given
    if assists:
        # Get the number of assists given per match
        individual_assists = [goal_obj.match_id for goal_obj in assists]
        unique_match_ids_w_his_assists = list(set([goal_obj.match_id for goal_obj in assists]))
        num_assists_per_match = {
            int(match_id): individual_assists.count(match_id)
            for match_id in unique_match_ids_w_his_assists
        }
        num_assists_per_match = dict(sorted(num_assists_per_match.items()))
        # st.write(num_assists_per_match)

        match_ids_w_his_assists = list(set([assist.match_id for assist in assists]))
        # st.write("match_id: num_of_assists")
        # st.write(f"Assists given in matches: {match_ids_w_his_assists}")

        # Via the `goal.match_id`, retrieve the `match` object to get the match dates
        response = api_requests.get_all_matches(ids=match_ids_w_his_assists)
        gave_assist_in_matches = response_to_json(response)
        gave_assist_in_matches = [schemas.Match(**match) for match in gave_assist_in_matches]

        dates_per_match = {int(match.id): match.date for match in gave_assist_in_matches}
        dates_per_match = dict(sorted(dates_per_match.items()))
        # st.write("match_id: date")
        # st.write(dates_per_match)

        assists_df = pd.DataFrame({
            "match_ids": dates_per_match.keys(),
            "Dates": dates_per_match.values(),
            "Assists given": num_assists_per_match.values(),
        })
        assists_df.sort_values("Dates", inplace=True)
        assists_df["Assists given (cum)"] = assists_df["Assists given"].cumsum()
        assists_fig = px.line(
            assists_df,
            x="Dates",
            y="Assists given (cum)",
            # title="Assists over time"
        )

        st.plotly_chart(assists_fig)