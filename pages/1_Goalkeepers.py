import pandas as pd
import streamlit as st
import streamlit_nested_layout
from pandasql import sqldf
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from Stat_Cards import StatCard, get_deltas

#styling & page settings

st.set_page_config(
    page_title="Goalkeepers",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='collapsed')
add_logo("logo.png", height=210)
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
style_metric_cards(border_left_color='#d92025', border_color='#d92025', box_shadow=True, border_size_px=1, border_radius_px=10)

#function to return sql queries from pandas dataframe

pysqldf = lambda q: sqldf(q, globals())

@st.cache_data
def load_database():
    GK = pd.read_csv('Master.csv')
    return GK

GK = load_database()


#getting names of united forwards who have played more than a total of 90 minutes on pitch
#making a list of these and unnesting that list for easy access 

forward_query = '''SELECT name from GK WHERE position ='GK' AND ninteys >1 AND club ='Manchester United';'''
names = pysqldf(forward_query).values
name_list = []
for i in names:
    name_list.append(i.tolist())
name_list = [num for sublist in name_list for num in sublist]

clubs = ['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton','Chelsea','Crystal Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester City','Newcastle','Nottingham Forest','Southampton','Tottenham','West Ham','Wolves']

#PREMIER LEAGUE HEAD TO HEAD

st.markdown("<h1 style='text-align: center;color: black;'>Head to Head: Premier League</h1>", unsafe_allow_html=True)
st.write('')

cols = st.columns(2)
with cols[0]:
    first_choice = st.selectbox(label='Which goalkeeper would you like to compare', options = name_list , key=23 )
with cols[1]:
    second_choice =st.selectbox(label='Which team would you like to compare against?', options=clubs)


if first_choice == 'Manchester United':
    first_choice_stats = StatCard(club=first_choice,position ='GK',delta = None).general_stats + StatCard(club=first_choice,position ='GK',delta = None).goalkeeping_stats 
else:
    first_choice_stats = StatCard(player=first_choice,position ='GK',delta = None).general_stats + StatCard(player=first_choice,position ='GK',delta = None).goalkeeping_stats 
second_choice_stats = StatCard(club=second_choice,position ='GK',delta = None).general_stats + StatCard(club=second_choice,position ='GK',delta = None).goalkeeping_stats 

deltas = get_deltas(first_choice_stats, second_choice_stats)

cols = st.columns(2)
with cols[0]:
    if first_choice == 'Manchester United':
        data = StatCard(club=first_choice, position='GK', delta=deltas[0])
        data.create_card()
    else:
            data = StatCard(player=first_choice, position ='GK',delta=deltas[0])
            data.create_card()
    with cols[1]:
        data = StatCard(club=second_choice, position ='GK',delta=deltas[1])
        data.create_card()