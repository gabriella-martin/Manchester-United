import streamlit as st
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
# streamlit_app.py
import streamlit_nested_layout
import psycopg2
st.set_page_config(
    page_title="Gabriella's Dashboard",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='collapsed')

add_logo("logo.png", height=210)

st.write('# <- CLICK HERE TO SHOW SIDEBAR')

