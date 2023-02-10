import streamlit as st


def insert_page_heading(title, image_path):
    title_col, logo_col = st.columns([10, 1.2])
    title_col.markdown(title)
    logo_col.image(image_path)
    cols = title_col, logo_col
    return cols
