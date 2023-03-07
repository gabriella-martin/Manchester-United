import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from streamlit_extras.app_logo import add_logo
from pipelines.club_general_pipeline import ClubGeneralStats

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'database-1.c0lrvxe9frij.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = st.secrets['DATABASE_PASSWORD'] 
PORT = 5432
DATABASE = 'football'

#styling & page settings

st.set_page_config(
    page_title="Upcoming",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='auto')

add_logo("resources/logo.png", height=190)

#connecting to database & getting upcoming game

next_match_query = '''SELECT * from fixtures WHERE (home_team = 'Manchester United' or away_team = 'Manchester United') and home_goals is NULL limit 1;'''
next_match = []
with psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, dbname=DATABASE, port=PORT) as conn:
    with conn.cursor() as cur:
        cur.execute(next_match_query)
        records = cur.fetchall()
        for i in records:
            next_match.append(i)
        cur.close()
next_match = [num for sublist in next_match for num in sublist]

#loading the data

if next_match[1] == 'Manchester United':
    opposition = next_match[-1]
if next_match[-1] == 'Manchester United':
    opposition = next_match[1]

united_stats= ClubGeneralStats(club='Manchester United')
united_stats = united_stats.create_club_dataframe()

opposition_stats = ClubGeneralStats(club=opposition)
opposition_stats = opposition_stats.create_club_dataframe()

#LOGO SECTION

st.markdown(f"<h1 style='text-align: center;color: black;'>Manchester United Upcoming</h1>", unsafe_allow_html=True)

st.write('')
st.write('')
st.write('')

cols = st.columns([5,5,5,5,5])

with cols[1]:
    st.image(f'resources/{(next_match[1]).lower()}.png')

with cols[2]:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.markdown(f"<h1 style='text-align: center;color: black;'>vs</h1>", unsafe_allow_html=True)

with cols[3]:
    st.image(f'resources/{(next_match[-1]).lower()}.png')

#LINE GRAPH SECTION

cols = st.columns(2)
with cols[0]:
    fig = px.line(united_stats, title='Manchester United Form: Goals', y=[ 'Goals Scored', 'Goals Conceeded'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-4,10])
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(united_stats, title='Manchester United Form: Net Goals', y=['Net Goals'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-10,10])
    fig.add_hline(y=0)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(united_stats, title='Manchester United Form: Points', y=[ 'Points', 'Points Rolling Average'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-2,5])
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:

    fig = px.line(opposition_stats, title=f'{opposition} Form: Goals', y=[ 'Goals Scored', 'Goals Conceeded'], x='Matches Played', color_discrete_sequence =['blue', 'black'])
    fig.update(layout_yaxis_range = [-4,10])
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(opposition_stats, title=f'{opposition} Form: Net Goals', y=['Net Goals'], x='Matches Played', color_discrete_sequence =['blue', 'black'])
    fig.update(layout_yaxis_range = [-10,10])
    fig.add_hline(y=0)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(opposition_stats, title=f'{opposition} Form: Points', y=[ 'Points', 'Points Rolling Average'], x='Matches Played', color_discrete_sequence =['blue', 'black'])
    fig.update(layout_yaxis_range = [-2,5])
    st.plotly_chart(fig, use_container_width=True)


#PIE CHART OF GOALS

with cols[0]:
    club = 'Manchester United'
    player_logs = []
    query=f'''SELECT name, goals from players where club = '{club}' and goals > 0 order by goals desc ;'''
    with psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, dbname=DATABASE, port=PORT) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            player_logs = cur.fetchall()
        cur.close()
    goalscorers = []
    goals = []
    for player_log in player_logs:
        goalscorers.append(player_log[0])
        goals.append(player_log[1])
    dataframe = pd.DataFrame({'Name': goalscorers, 'Goals':goals})
    fig = px.pie(dataframe, title ='Goals by Scorer',values='Goals', labels ='Name', names='Name', color_discrete_sequence=['red', 'black', '#fcf803', '#e6dfd8','#46bde8', '#ad6417', '#232247', '#663b7a'])
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    club = opposition
    player_logs = []
    query=f'''SELECT name, goals from players where club = '{club}' and goals > 0 order by goals desc ;'''
    with psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, dbname=DATABASE, port=PORT) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            player_logs = cur.fetchall()
        cur.close()
    goalscorers = []
    goals = []
    for player_log in player_logs:
        goalscorers.append(player_log[0])
        goals.append(player_log[1])
    dataframe = pd.DataFrame({'Name': goalscorers, 'Goals':goals})
    fig = px.pie(dataframe, title ='Goals by Scorer',values='Goals', labels ='Name', names='Name', color_discrete_sequence=['red', 'black', '#fcf803', '#e6dfd8','#46bde8', '#ad6417', '#232247', '#663b7a'])
    st.plotly_chart(fig, use_container_width=True)


