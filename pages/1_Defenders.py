
import pandas as pd
import streamlit as st
import streamlit_nested_layout

from pandasql import sqldf
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from ServingData_Pipeline import PlayerStatFormatting

st.set_page_config(
    page_title="Defenders",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state='collapsed')

add_logo("logo.png", height=210)

st.markdown("<h1 style='text-align: center;color: black;'>Defenders</h1>", unsafe_allow_html=True)
style_metric_cards(border_left_color='#d92025', border_color='#d92025', box_shadow=True, border_size_px=1, border_radius_px=10)

pysqldf = lambda q: sqldf(q, globals())

df = pd.read_csv('Player.csv')

#retrieving names of defenders who have played more than 90min as less than 90min gives inaccurate results

defender_query = '''SELECT name from df WHERE position ='DF' and ninteys >1 ;'''
names = pysqldf(defender_query).values
name_list = []
for i in names:
    name_list.append(i.tolist())
name_list = [num for sublist in name_list for num in sublist]

#defender stat card

class DefenderStatCard:
    def __init__(self,player):
        self.player = player
        self.image_path = (self.player.split(' '))[-1]
        s = PlayerStatFormatting(player)
        self.number = s.number
        self.general_stats = s.format_general_stats()
        self.threat_stats = s.format_threat_stats()
        self.upfield_stats = s.get_def_upfield_play_stats()

    def make_card(self):

            with st.expander(label=f'**{self.player}: {self.number}**', expanded=True ):
                tabs = st.tabs(['General', 'Threat-Handling', 'Upfield Play' ])
                with tabs[0]:
                    cols = st.columns([4,4,8])
                    with cols[2]:
                        st.image(f'players/{self.image_path}.png', width=450,)
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
                        st.image(f'players/{self.image_path}.png', width=450)
                    with cols[0]:
                        st.write('')
                        st.metric(label='SHOT BLOCKS/90', value =self.threat_stats[0])
                        st.metric(label='BLOCKS/90', value =self.threat_stats[1])
                        st.metric(label='INTERCEPTIONS/90', value =self.threat_stats[2])
                        st.metric(label='CLEARANCES/90', value =self.threat_stats[3])
                    with cols[1]:
                        st.write('')
                        st.metric(label='TACKLE SUCCESS %', value =str(self.threat_stats[4]) + '%')
                        st.metric(label='TACKLES/90', value =self.threat_stats[5])
                        st.metric(label='TAKEON SUCCESS%', value =str(round(self.threat_stats[6])) + '%' )
                        st.metric(label='FOULS/90', value =self.threat_stats[7])  

                with tabs[2]:
                    cols = st.columns([4,5,8])
                    with cols[2]:
                        st.image(f'players/{self.image_path}.png', width=450)
                    with cols[0]:
                        st.write('')
                        st.metric(label='PROG CARRIES/90', value =self.upfield_stats[0])
                        st.metric(label='PROG PASSES/90', value =self.upfield_stats[1])
                        st.metric(label='PASS TO 3rd/90', value =self.upfield_stats[2])
                        st.metric(label='KEY PASSES/90', value =self.upfield_stats[3])     
                    with cols[1]:
                        st.write('')
                        st.write('')
                        with st.expander('**Progressive Carries**'):
                            st.write("Carries that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any carry into the penalty area. Excludes carries which end in the defending half of the pitch")
                        st.write('')
                        st.write('')
                        st.write('')
                        with st.expander('**Progressive Passes**'):
                            st.write("Completed passes that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any completed pass into the penalty area. Excludes passes from the defending 40% of the pitch")
                        st.write('')
                        st.write('')
                        st.write('')
                        with st.expander('**Passes to Att 1/3rd**'):
                            st.write("Completed passes that enter the 1/3 of the pitch closest to the goal. Not including set pieces")
                        st.write('')
                        st.write('')
                        st.write('')
                        with st.expander('**Key Passes**'):
                            st.write("Passes that directly lead to a shot (assisted shots)")

#page layout

large_cols = st.columns(2)
for index, name in enumerate(name_list):
    if index in [0,2,4,6,8]:
        with large_cols[0]:
            df = DefenderStatCard(player=name)
            df.make_card()
    else:
        with large_cols[1]:
            df = DefenderStatCard(player=name)
            df.make_card()