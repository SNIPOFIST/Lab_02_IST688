# main.py
import streamlit as st

pages=[
    st.Page("lab_01.py", title = "Lab - 01"),
    st.Page("lab_02.py", title= " Lab - 02")
]

pg = st.navigation(pages)
pg.run()

st.sidebar.title("Summary Options")