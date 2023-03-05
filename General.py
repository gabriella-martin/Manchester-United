import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo

from pandasql import sqldf
import streamlit_nested_layout
import psycopg2
st.set_page_config(
    page_title="Gabriella's Dashboard",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='auto')

add_logo("logo.png", height=190)

pysqldf = lambda q: sqldf(q, globals())

from Pipelines.GeneralStats_Pipeline import ClubGeneralStats

#getting names of united forwards who have played more than a total of 90 minutes on pitch
#making a list of these and unnesting that list for easy access 
st.write('# Manchester United General')

clubs = ['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton','Chelsea','Crystal Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester City','Newcastle','Nottingham Forest','Southampton','Tottenham','West Ham','Wolves']

club = 'Tottenham'
df = pd.read_csv('Fixtures.csv')
club_query = f'''SELECT * from df WHERE (home_team ='{club}' or away_team = '{club}') and home_score is NULL order by Date Asc ;'''
match_logs = pysqldf(club_query).values
match_results = []
for match in match_logs:
    match_results.append(match.tolist())
match_results = [num for sublist in match_results for num in sublist]


a = ClubGeneralStats(club='Manchester United')
ya = a.create_club_dataframe()

ee = a.split_matches_from_match_results()

for match in ee:
    if match[1] == 'Manchester United':
        goals_against = match[-2]
    if match[-1] == 'Manchester United':
        goals_against = match[2]

cols = st.columns(2)
with cols[0]:
    fig = px.line(ya, title='Manchester United Form: Goals', y=[ 'Goals Scored', 'Goals Conceeded'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-4,10])
    st.plotly_chart(fig, use_container_width=True)

# who scored for us, their position
# who scores most against us





with cols[1]:
    fig = px.line(ya, title='Manchester United Form: Points', y=[ 'Points', 'Points Cumulative Moving Average'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-2,5])
    st.plotly_chart(fig, use_container_width=True)
def get_sum_of_points_for_each_club():
    list_of_points = []
    for club in clubs:
        results = ClubGeneralStats(club).get_match_results()
        total_points = sum(results[0])
        list_of_points.append(total_points)
    return list_of_points
list_of_points = get_sum_of_points_for_each_club()

club_points = pd.DataFrame({'Club':clubs, 'Points':list_of_points})



top_5_query=f'''SELECT Club from club_points where Club is not 'Manchester United' order by Points desc ;'''

match_logs = pysqldf(top_5_query).values
match_results = []
for match in match_logs:
    match_results.append(match.tolist())
match_results = [num for sublist in match_results for num in sublist]

with cols[0]:
    selections = st.multiselect(label='Which teams would you like to compare to, options are given in current standing order', options = match_results)

match_results = ['Manchester United'] + selections
dict_of_df = {}
import plotly.graph_objects as go
for index, top_club in enumerate(match_results):
    a = ClubGeneralStats(club=top_club)
    ya = a.create_club_dataframe()
    dict_of_df[match_results[index]] =  ya

fig = go.Figure()

for df in dict_of_df:
    fig = fig.add_trace(go.Scatter(x = dict_of_df[df]["Matches Played"],
                                   y = dict_of_df[df]["Points Sum"],
                                   name = df ))
fig.data[0].line.color = "#DA291C"
with cols[0]:
    st.plotly_chart(fig, use_container_width=True)
with cols[1]:
    fig = px.line(ya, title='Manchester United Form: Goals', y=[ 'Net Goals'], x='Matches Played', color_discrete_sequence =['red', 'black'])
    fig.update(layout_yaxis_range = [-4,6])
    st.plotly_chart(fig, use_container_width=True)