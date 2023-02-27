import pandas as pd
import streamlit as st
import streamlit_nested_layout

from pandasql import sqldf
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from ServingData_Pipeline import PlayerStatFormatting

st.set_page_config(
    page_title="Forwards",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='collapsed')

add_logo("logo.png", height=210)

st.markdown("<h1 style='text-align: center;color: black;'>Forwards</h1>", unsafe_allow_html=True)
style_metric_cards(border_left_color='#d92025', border_color='#d92025', box_shadow=True, border_size_px=1, border_radius_px=10)

pysqldf = lambda q: sqldf(q, globals())

df = pd.read_csv('Player.csv')

#retrieving names of forwards who have played more than 90min as less than 90min gives inaccurate results

forward_query = '''SELECT name from df WHERE position ='FW' AND ninteys >1 ;'''
names = pysqldf(forward_query).values
name_list = []
for i in names:
    name_list.append(i.tolist())
name_list = [num for sublist in name_list for num in sublist]

#foward stat card

class ForwardStatCard:

    def __init__(self,player):
        self.player = player
        if self.player == 'Anthony Martial':
            self.width = 423
        else:
            self.width = 450
        self.image_path = (self.player.split(' '))[-1]
        s = PlayerStatFormatting(player)
        self.number = s.number
        self.general_stats = s.format_general_stats()
        self.involvement_stats = s.get_forward_involvement_stats()
        self.scoring_stats = s.format_goal_scoring_stats()

    def make_card(self):

            with st.expander(label=f'**{self.player}: {self.number}**', expanded=True ):
                tabs = st.tabs(['General', 'Game Involvement', 'Upfield Play' ])
                with tabs[0]:
                    cols = st.columns([4,4,8])
                    with cols[2]:
                        st.image(f'players/{self.image_path}.png', width=self.width,)
                    with cols[0]:
                        st.write('')
                        st.metric(label='AGE', value =self.general_stats[0])
                        st.metric(label='SALARY', value =self.general_stats[1])
                        st.metric(label='EST. MARKET VALUE', value =self.general_stats[2])
                        st.metric(label='TOUCHES/90', value =self.general_stats[3])
                    with cols[1]:
                        st.write('')
                        st.metric(label='PASS ACCURACY', value =str(self.general_stats[4]) + '%')
                        st.metric(label='SHORT PASSES', value =str(self.general_stats[5]) + '%')
                        st.metric(label='MEDIUM PASSES', value =str(self.general_stats[6]) + '%')
                        st.metric(label='LONG PASSES', value =str(self.general_stats[7]) + '%')       
                with tabs[1]:
                    cols = st.columns([4,4,8])
                    with cols[2]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[0]:
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.metric(label='TOUCHES IN 3RD/90', value =self.involvement_stats[0])
                        st.metric(label='TOCUHES IN PEN/90', value =self.involvement_stats[1])
                        st.metric(label='FOULS DRAWN/90', value =self.involvement_stats[2])
                        
                    with cols[1]:
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.metric(label='PASSES TO 3RD/90', value =self.involvement_stats[3])
                        st.metric(label='PROG CARRIES/90', value =self.involvement_stats[4])
                        st.metric(label='PROG PASSES/90', value =self.involvement_stats[5])  

                with tabs[2]:
                    cols = st.columns([4,4,8])
                    with cols[2]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[0]:
                        st.write('')
                        st.metric(label='SHOTS/90', value =self.scoring_stats[0])
                        st.metric(label='ON TARGET/90', value =self.scoring_stats[1])
                        st.metric(label='SHOT ACCURACY', value =str(self.scoring_stats[2]) + '%')
                        st.metric(label='FINISHING ACCURACY', value =str(self.scoring_stats[3]) + '%')     
                    with cols[1]:
                        st.write('')
                        st.metric(label='ASSISTS/90', value =self.scoring_stats[4])
                        st.metric(label='GOALS/90', value =self.scoring_stats[5])
                        st.metric(label='KEY PASSES/90', value =self.scoring_stats[6])
                        st.metric(label='PASSES TO PEN/90', value =self.scoring_stats[7])     

#page layout

large_cols = st.columns(2)
for index, name in enumerate(name_list):
    if index in [0,2,4,6,8]:
        with large_cols[0]:
            df = ForwardStatCard(player=name)
            df.make_card()
    else:
        with large_cols[1]:
            df = ForwardStatCard(player=name)
            df.make_card()