
import pandas as pd
import streamlit as st
import streamlit_nested_layout

from pandasql import sqldf
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from Stat_Cards import StatCard

st.set_page_config(
    page_title="Defenders",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='collapsed')

add_logo("logo.png", height=210)
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
pysqldf = lambda q: sqldf(q, globals())

df = pd.read_csv('Player.csv')
defender_query = '''SELECT name from df WHERE position ='DF' and ninteys >1 ;'''
names = pysqldf(defender_query).values
name_list = []
for i in names:
    name_list.append(i.tolist())
name_list = [num for sublist in name_list for num in sublist]
st.markdown("<h1 style='text-align: center;color: black;'>Head to Head: United</h1>", unsafe_allow_html=True)
st.write('')
st.write('')
cols = st.columns(2)
with cols[0]:
    st.write('')
    first_choice = st.selectbox(label='Which defender would you like to compare', options = name_list )

with cols[1]:
    second_choice =st.selectbox(label='Who would you like to compare against?', options=name_list)


style_metric_cards(border_left_color='#d92025', border_color='#d92025', box_shadow=True, border_size_px=1, border_radius_px=10)

def get_stats(first_choice, second_choice):
    first_choice_stats = StatCard(player=first_choice,delta = None).general_stats +StatCard(player=first_choice,delta = None).threat_stats+StatCard(player=first_choice,delta = None).upfield_stats
    second_choice_stats = StatCard(player=second_choice,delta = None).general_stats +StatCard(player=second_choice,delta = None).threat_stats+StatCard(player=second_choice,delta = None).upfield_stats
    first_choice_stats[1] = float(first_choice_stats[1][:-1])
    first_choice_stats[2] = float(first_choice_stats[2][:-1])
    second_choice_stats[1] = float(second_choice_stats[1][:-1])
    second_choice_stats[2] = float(second_choice_stats[2][:-1])
    delta_list_card1 = []
    delta_list_card2 = []
    for index, value in enumerate(first_choice_stats):
        delta1 = round(((value - second_choice_stats[index])/(second_choice_stats[index]))*100)
        delta2 = round(((second_choice_stats[index]-value )/(value))*100)
        delta_list_card1.append(delta1)
        delta_list_card2.append(delta2)
    return delta_list_card1, delta_list_card2



deltas = get_stats(first_choice, second_choice)
cols = st.columns(2)
with cols[0]:
   df = StatCard(player=first_choice, delta=deltas[0])
   df.create_card()

with cols[1]:
   df = StatCard(player=second_choice, delta=deltas[1])
   df.create_card()

#retrieving names of defenders who have played more than 90min as less than 90min gives inaccurate results

st.markdown("<h1 style='text-align: center;color: black;'>Defender Roster</h1>", unsafe_allow_html=True)

#page layout
@st.cache_resource()
def roster():
    large_cols = st.columns(2)
    for index, name in enumerate(name_list):
        if index%2 == 0:
            with large_cols[0]:
                df = StatCard(player=name, delta = None)
                df.create_card()
        else:
            with large_cols[1]:
                df = StatCard(player=name, delta = None)
                df.create_card()
roster()