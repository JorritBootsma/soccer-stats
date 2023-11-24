import streamlit as st

import style_config
from helper_funcs.streamlit_components import insert_page_heading

st.set_page_config(
    page_title=style_config.page_titles,
    page_icon=style_config.page_favicon
)

insert_page_heading("# 🏆 Team Stats", style_config.page_favicon)
st.write("---")

if "team" not in st.session_state:
    st.write("Make sure to login first. Go to the Login page via the sidebar.")
else:
    st.write(st.session_state["team"])
    st.sidebar.markdown("# 🏆️ Team Stats")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏆️ Presence")
    st.sidebar.markdown("### ⚽️ Goals")
    st.sidebar.markdown("### 👞 Assists")

    st.header(" 🏆️ Presence")


    st.header(" ⚽️ Goals")


    st.header(" 👞 Assists")
