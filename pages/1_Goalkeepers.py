import psycopg2
import streamlit as st
import streamlit_nested_layout
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from stat_cards import StatCard, get_deltas

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'database-1.c0lrvxe9frij.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = st.secrets['DATABASE_PASSWORD'] 
PORT = 5432
DATABASE = 'football'

#styling & page settings

st.set_page_config(
    page_title="Goalkeepers",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='collapsed')

add_logo("resources/logo.png", height=210)

with open('resources/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

style_metric_cards(border_left_color='#d92025', border_color='#d92025', box_shadow=True, border_size_px=1, border_radius_px=10)

#connecting to database & getting goalkeeper names

name_list = []

with psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, dbname=DATABASE, port=PORT) as conn:
    with conn.cursor() as cur:
        cur.execute('''SELECT name from players WHERE position ='GK' AND ninteys >1 AND club ='Manchester United';''')
        records = cur.fetchall()
        for i in records:
            name_list.append(i)
        
name_list = [num for sublist in name_list for num in sublist]
conn.close()
 
clubs = ['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton','Chelsea','Crystal Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester City','Newcastle','Nottingham Forest','Southampton','Tottenham','West Ham','Wolves']

#PREMIER LEAGUE HEAD TO HEAD

st.markdown("<h1 style='text-align: center;color: black;'>Head to Head: Premier League</h1>", unsafe_allow_html=True)
st.write('')
st.write('')
st.write('')

cols = st.columns(2)
with cols[0]:
    first_choice = st.selectbox(label='Which goalkeeper would you like to compare', options = name_list , key=23 )
with cols[1]:
    second_choice =st.selectbox(label='Which team would you like to compare against?', options=clubs)

@st.cache_data
def league_comparison(first_choice, second_choice):
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

league_comparison(first_choice, second_choice)