import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from pandasql import sqldf
import streamlit_nested_layout

st.set_page_config(
    page_title="General",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='auto')

add_logo("logo.png", height=190)

pysqldf = lambda q: sqldf(q, globals())
import plotly.graph_objects as go
from Pipelines.GeneralStats_Pipeline import ClubGeneralStats
df = pd.read_csv('Master.csv')

st.write('# Manchester United General')

clubs = ['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton','Chelsea','Crystal Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester City','Newcastle','Nottingham Forest','Southampton','Tottenham','West Ham','Wolves']

def get_sum_of_points_for_each_club():
    list_of_points = []
    for club in clubs:
        results = ClubGeneralStats(club).get_match_results()
        total_points = sum(results[0])
        list_of_points.append(total_points)
    return list_of_points

list_of_points = get_sum_of_points_for_each_club()
club_points = pd.DataFrame({'Club':clubs, 'Points':list_of_points})
table_standings=f'''SELECT Club from club_points where Club is not 'Manchester United' order by Points desc;'''

table_standings_values = pysqldf(table_standings).values
table_standings = []
for club in table_standings_values:
    table_standings.append(club.tolist())
table_standings = [num for sublist in table_standings for num in sublist]

united_stats= ClubGeneralStats(club='Manchester United')
united_stats = united_stats.create_club_dataframe()

selection = st.selectbox(label='Which team would you like to compare to, options are given in current standing order', options = table_standings)

cols = st.columns(2)
with cols[0]:
    fig = px.line(united_stats, title='Manchester United Form: Goals', y=[ 'Goals Scored', 'Goals Conceeded'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-4,10])
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    opposition_stats = ClubGeneralStats(club=selection)
    opposition_stats = opposition_stats.create_club_dataframe()
    fig = px.line(opposition_stats, title=f'{selection} Form: Goals', y=[ 'Goals Scored', 'Goals Conceeded'], x='Matches Played', color_discrete_sequence =['blue', 'black'])
    fig.update(layout_yaxis_range = [-4,10])
    st.plotly_chart(fig, use_container_width=True)

with cols[0]:
    fig = px.line(united_stats, title='Manchester United Form: Net Goals', y=['Net Goals'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-10,10])
    fig.add_hline(y=0)
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    fig = px.line(opposition_stats, title=f'{selection} Form: Net Goals', y=['Net Goals'], x='Matches Played', color_discrete_sequence =['blue', 'black'])
    fig.update(layout_yaxis_range = [-10,10])
    fig.add_hline(y=0)
    st.plotly_chart(fig, use_container_width=True)


with cols[0]:
    fig = px.line(united_stats, title='Manchester United Form: Points', y=[ 'Points', 'Points Rolling Average'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-2,5])
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    fig = px.line(opposition_stats, title=f'{selection} Form: Points', y=[ 'Points', 'Points Rolling Average'], x='Matches Played', color_discrete_sequence =['blue', 'black'])
    fig.update(layout_yaxis_range = [-2,5])
    st.plotly_chart(fig, use_container_width=True)

with cols[0]:
    club = 'Manchester United'
    query=f'''SELECT name, goals from df where club is '{club}' and goals > 0 order by goals desc ;'''
    player_logs = pysqldf(query).values
    goalscorers = []
    goals = []
    for player_log in player_logs:
        goalscorers.append(player_log[0])
        goals.append(player_log[1])
    dataframe = pd.DataFrame({'Name': goalscorers, 'Goals':goals})
    fig = px.pie(dataframe, title ='Goals by Scorer',values='Goals', labels ='Name', names='Name', color_discrete_sequence=['red', 'black', '#fcf803', '#e6dfd8','#46bde8', '#ad6417', '#232247', '#663b7a'])
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    club = selection
    query=f'''SELECT name, goals from df where club is '{club}' and goals > 0 order by goals desc ;'''
    player_logs = pysqldf(query).values
    goalscorers = []
    goals = []
    for player_log in player_logs:
        goalscorers.append(player_log[0])
        goals.append(player_log[1])
    dataframe = pd.DataFrame({'Name': goalscorers, 'Goals':goals})
    fig = px.pie(dataframe, title ='Goals by Scorer',values='Goals', labels ='Name', names='Name', color_discrete_sequence=['red', 'black', '#fcf803', '#e6dfd8','#46bde8', '#ad6417', '#232247', '#663b7a'])
    st.plotly_chart(fig, use_container_width=True)


selections = st.multiselect(label='Which teams would you like to compare to, options are given in current standing order', options = table_standings)

options= ['Manchester United'] +[selection]+ selections
dict_of_df = {}

for index, club in enumerate(options):
    club_data = ClubGeneralStats(club=club)
    club_data = club_data.create_club_dataframe()
    dict_of_df[options[index]] =  club_data

fig = go.Figure()

for df in dict_of_df:
    fig = fig.add_trace(go.Scatter(x = dict_of_df[df]["Matches Played"],
                                   y = dict_of_df[df]["Points Sum"],
                                   name = df ))
    
for index, value in enumerate(fig.data):
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
    value.line.color = colors[index]
fig.data[0].line.color = "#DA291C"

st.plotly_chart(fig, use_container_width=True)

