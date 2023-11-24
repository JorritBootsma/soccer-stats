import locale

import streamlit as st

import api_requests
import style_config
from helper_funcs.general_funcs import response_to_json
import schemas
from helper_funcs.streamlit_components import insert_page_heading

locale.setlocale(locale.LC_ALL, "nl_NL")

st.set_page_config(
    page_title=style_config.page_titles,
    page_icon=style_config.page_favicon
)

insert_page_heading("# ⛳️ Matches", style_config.page_favicon)
st.write("---")
st.sidebar.markdown("# ⛳️ Matches")
st.sidebar.markdown("---")

if "team" not in st.session_state:
    st.write("Make sure to login first. Go to the Login page via the sidebar.")
else:

    st.write("bla")
    response_matches = api_requests.get_all_matches()
    response_matches = response_to_json(response_matches)
    st.write(response_matches)
    matches = [schemas.Match(**match) for match in response_matches]

    st.markdown(
        """
        <style>
            div[data-testid="column"]:nth-of-type(1)
            {
            } 
    
            div[data-testid="column"]:nth-of-type(2)
            {
                text-align: end;
            } 
            
            div[data-testid="column"]:nth-of-type(3)
            {
                text-align: center;
            } 
            
            div[data-testid="column"]:nth-of-type(4)
            {
                text-align: center;
            }     
            
            div[data-testid="column"]:nth-of-type(4)
            {
                text-align: left;
            }
            
            # div.row-widget.stCheckbox
            # {
            #     # border: 3px solid green;
            #     float: right;
            # }
            # 
            # label.st-bc.st-b3.st-bd.st-be.st-bf.st-as.st-ar.st-bg.st-bh:nth-of-type(1)
            # {
            #     # border: 3px solid red;
            #     float: right;
            # }
        </style>
        """, unsafe_allow_html=True
    )

    OUR_TEAM = st.session_state["team"]

    for match in matches:
        st.sidebar.markdown(f"##### {match.date.strftime('%a %-d %b. %Y')}")
        st.write(match.date.strftime("%a %-d %b. %Y"))
        date, home_team, score, away_team = st.columns([1, 2.5, .5, 4])
        home_team.markdown(f"###### {match.home_team.club}")
        if OUR_TEAM == match.home_team:
            score.markdown(f"###### {len(match.our_goals)} - {match.their_goals}")
        elif OUR_TEAM == match.away_team:
            score.markdown(f"###### {match.their_goals} - {len(match.our_goals)}")
        else:
            raise ValueError(
                f"This match does not contain {OUR_TEAM} as home_team ({match.home_team}) "
                f"or away_team ({match.away_team})")

        away_team.markdown(f"###### {match.away_team.club}")

        space_col, checkbox_col = st.columns([4, 1])
        goals_checkbox = checkbox_col.checkbox("See goals", key=f"goals_{match.id}")
        if goals_checkbox:
            for goal in match.our_goals:
                st.write(goal)

        presence_checkbox = checkbox_col.checkbox("See presence", key=f"presence_{match.id}")
        if presence_checkbox:
            for player in match.players_present:
                st.write(player)

        st.write("---")
