import locale

import streamlit as st

import api_requests
from helper_funcs.general_funcs import response_to_json
import schemas
from Main_Page import OUR_TEAM
locale.setlocale(locale.LC_ALL, "nl_NL")

st.markdown("# ⛳️ Matches")
st.write("---")
st.sidebar.markdown("# ⛳️ Matches")
st.sidebar.markdown("---")

response_matches = api_requests.get_all_matches()
response_matches = response_to_json(response_matches)
# st.write(response_matches)
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


for match in matches:
    st.sidebar.markdown(f"##### {match.date.strftime('%a %-d %b. %Y')}")
    st.write(match.date.strftime("%a %-d %b. %Y"))
    # st.write(f"{match.date}")
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


# import locale, time
# time.strftime("%B") 'August'
# locale.getlocale() (None, None)
# locale.setlocale(locale.LC_ALL, "") 'nl_NL'
# locale.getlocale() ('nl_NL', 'ISO8859-1')
# time.strftime("%B") 'augustus'
#
# time.strptime("10 augustus 2005 om 17:26", "%d %B %Y om %H:%M")