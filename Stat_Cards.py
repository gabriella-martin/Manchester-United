import streamlit as st
from Pipelines.ServingData_Pipeline import PlayerStatFormatting

class DefenderStatCard:
    def __init__(self,player,delta=None):
        self.player = player
        self.delta = delta
        if self.delta != None:
            self.width = 425
        else:
            self.width = 335
        self.image_path = ((self.player.split(' '))[-1]).lower()
        s = PlayerStatFormatting(player)
        self.number = s.number
        self.general_stats = s.format_general_stats()
        self.threat_stats = s.format_threat_stats()
        self.upfield_stats = s.get_def_upfield_play_stats()

    def get_deltas(self, number):
        if self.delta != None:
            delta = str(self.delta[number]) + '%'
        else:
            delta = None
        return delta

    def make_card(self):

            with st.expander(label=f'**{self.player}: {self.number}**', expanded=True ):
                tabs = st.tabs(['General', 'Threat-Handling', 'Upfield Play' ])
                with tabs[0]:
                    cols = st.columns([8,5,5])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width,)
                    with cols[1]:
                        st.write('')
                        st.metric(label='age', value =self.general_stats[0], delta=self.get_deltas(0))
                        st.metric(label='salary', value =self.general_stats[1], delta=self.get_deltas(1))
                        st.metric(label='value', value =self.general_stats[2], delta=self.get_deltas(2))
                        st.metric(label='touches/90', value =self.general_stats[3], delta=self.get_deltas(3))
                    with cols[2]:
                        st.write('')
                        st.metric(label='pass accuracy', value =str(round(self.general_stats[4])) + '%', delta=self.get_deltas(4))
                        st.metric(label='short passes', value =str(round(self.general_stats[5])) + '%', delta=self.get_deltas(5))
                        st.metric(label='medium passes', value =str(round(self.general_stats[6])) + '%', delta=self.get_deltas(6))
                        st.metric(label='long passes', value =str(round(self.general_stats[7])) + '%', delta=self.get_deltas(7))        
                with tabs[1]:
                    cols = st.columns([8,5,5])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[1]:
                        st.write('')
                        st.metric(label='shot-blocks/90', value =self.threat_stats[0], delta=self.get_deltas(8))
                        st.metric(label='blocks/90', value =self.threat_stats[1], delta=self.get_deltas(9))
                        st.metric(label='interceptions/90', value =self.threat_stats[2], delta=self.get_deltas(10))
                        st.metric(label='clearances/90', value =self.threat_stats[3], delta=self.get_deltas(11))
                    with cols[2]:
                        st.write('')
                        st.metric(label='tackle success', value =str(self.threat_stats[4]) + '%', delta=self.get_deltas(12))
                        st.metric(label='tackle/90', value =self.threat_stats[5], delta=self.get_deltas(13))
                        st.metric(label='takeon success', value =str(round(self.threat_stats[6])) + '%', delta=self.get_deltas(14) )
                        st.metric(label='fouls/90', value =self.threat_stats[7], delta=self.get_deltas(15))  

                with tabs[2]:
                    cols = st.columns([8,5,5])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[2]:
                        st.write('')
                        st.metric(label='prog carries/90', value =self.upfield_stats[0], delta=self.get_deltas(16))
                        st.metric(label='prog passes/90', value =self.upfield_stats[1], delta=self.get_deltas(17))
                        st.metric(label='pass to 3rd/90', value =self.upfield_stats[2], delta=self.get_deltas(18))
                        st.metric(label='key passes/90', value =self.upfield_stats[3], delta=self.get_deltas(19))     
class MidfielderStatCard:

    def __init__(self,player, delta=None):
        self.player = player
        self.delta = delta
        if self.delta != None:
            self.width = 425
        else:
            self.width = 335
        self.image_path = ((self.player.split(' '))[-1]).lower()
        s = PlayerStatFormatting(player)
        self.minutes_played = round((s.ninetys)*90)
        self.number = s.number
        self.general_stats = s.format_general_stats()
        self.threat_stats = s.format_threat_stats()
        self.upfield_stats = s.get_upfield_play_stats()
    def get_deltas(self, number):
        if self.delta != None:
            delta = str(self.delta[number]) + '%'
        else:
            delta = None
        return delta
    def make_card(self):

            with st.expander(label=f'**{self.player}: {self.number}**', expanded=True ):
                tabs = st.tabs(['General', 'Threat-Handling', 'Upfield Play' ])
                with tabs[0]:
                    cols = st.columns([8,4,4])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width,)
                    with cols[1]:
                        st.write('')
                        st.metric(label='AGE', value =self.general_stats[0], delta =self.get_deltas(0))
                        st.metric(label='SALARY', value =self.general_stats[1], delta =self.get_deltas(1))
                        st.metric(label='MARKET VALUE', value =self.general_stats[2], delta =self.get_deltas(2))
                        st.metric(label='TOUCHES/90', value =self.general_stats[3], delta =self.get_deltas(3))
                    with cols[2]:
                        st.write('')
                        st.metric(label='PASS ACCURACY', value =str(round(self.general_stats[4])) + '%', delta =self.get_deltas(4))
                        st.metric(label='SHORT PASSES', value =str(round(self.general_stats[5])) + '%', delta =self.get_deltas(5))
                        st.metric(label='MEDIUM PASSES', value =str(round(self.general_stats[6])) + '%', delta =self.get_deltas(6))
                        st.metric(label='LONG PASSES', value =str(round(self.general_stats[7])) + '%', delta =self.get_deltas(7))       
                with tabs[1]:
                    cols = st.columns([8,4,4])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[1]:
                        st.write('')
                        st.metric(label='SHOT BLOCKS/90', value =self.threat_stats[0], delta =self.get_deltas(8))
                        st.metric(label='BLOCKS/90', value =self.threat_stats[1], delta =self.get_deltas(9))
                        st.metric(label='INTERCEPTIONS/90', value =self.threat_stats[2], delta =self.get_deltas(10))
                        st.metric(label='CLEARANCES/90', value =self.threat_stats[3], delta =self.get_deltas(11))
                    with cols[2]:
                        st.write('')
                        st.metric(label='TACKLE SUCCESS %', value =str(self.threat_stats[4]) + '%', delta =self.get_deltas(12))
                        st.metric(label='TACKLES/90', value =self.threat_stats[5], delta =self.get_deltas(13))
                        try:
                            st.metric(label='TAKEON SUCCESS%', value =str(round(self.threat_stats[6])) + '%' , delta =self.get_deltas(14))
                        except TypeError:
                            st.metric(label='TAKEON SUCCESS%', value ='NA' , delta =None)
                        st.metric(label='FOULS/90', value =self.threat_stats[7], delta =self.get_deltas(15))  

                with tabs[2]:
                    cols = st.columns([8,4,4])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[1]:
                        st.write('')
                        st.metric(label='SHOTS/90', value =self.upfield_stats[0], delta =self.get_deltas(16))
                        st.metric(label='SHOTS ON TARGET/90', value =self.upfield_stats[1], delta =self.get_deltas(17))
                        st.metric(label='ASSISTS/90', value =self.upfield_stats[2], delta =self.get_deltas(18))
                        st.metric(label='GOALS/90', value =self.upfield_stats[3], delta =self.get_deltas(19))     
                    with cols[2]:
                        st.write('')
                        st.metric(label='PASS into PEN/90', value =self.upfield_stats[4], delta =self.get_deltas(20))
                        st.metric(label='PROG PASSES/90', value =self.upfield_stats[5], delta =self.get_deltas(21))
                        st.metric(label='PROG CARRIES/90', value =self.upfield_stats[6], delta =self.get_deltas(22))
                        st.metric(label='KEY PASSES/90', value =self.upfield_stats[7], delta =self.get_deltas(23))     

class ForwardStatCard:

    def __init__(self,player, delta=None):
        self.player = player
        self.delta = delta
        if self.delta != None:
            self.width = 425
        else:
            self.width = 335
        self.image_path = ((self.player.split(' '))[-1]).lower()
        s = PlayerStatFormatting(player)
        self.number = s.number
        self.general_stats = s.format_general_stats()
        self.involvement_stats = s.get_forward_involvement_stats()
        self.scoring_stats = s.format_goal_scoring_stats()
    def get_deltas(self, number):
        if self.delta != None:
            delta = str(self.delta[number]) + '%'
        else:
            delta = None
        return delta
    def make_card(self):

            with st.expander(label=f'**{self.player}: {self.number}**', expanded=True ):
                tabs = st.tabs(['General', 'Game Involvement', 'Upfield Play' ])
                with tabs[0]:
                    cols = st.columns([8,4,4])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[1]:
                        st.write('')
                        st.metric(label='AGE', value =self.general_stats[0], delta =self.get_deltas(0))
                        st.metric(label='SALARY', value =self.general_stats[1], delta =self.get_deltas(1))
                        st.metric(label='MARKET VALUE', value =self.general_stats[2], delta =self.get_deltas(2))
                        st.metric(label='TOUCHES/90', value =self.general_stats[3], delta =self.get_deltas(3))
                    with cols[2]:
                        st.write('')
                        st.metric(label='PASS ACCURACY', value =str(round(self.general_stats[4])) + '%', delta =self.get_deltas(4))
                        st.metric(label='SHORT PASSES', value =str(round(self.general_stats[5])) + '%', delta =self.get_deltas(5))
                        st.metric(label='MEDIUM PASSES', value =str(round(self.general_stats[6])) + '%', delta =self.get_deltas(6))
                        st.metric(label='LONG PASSES', value =str(round(self.general_stats[7])) + '%', delta =self.get_deltas(7))        
                with tabs[1]:
                    cols = st.columns([8,4,4])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[1]:
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.metric(label='TOUCHES IN 3RD/90', value =self.involvement_stats[0], delta =self.get_deltas(8))
                        st.metric(label='TOCUHES IN PEN/90', value =self.involvement_stats[1], delta =self.get_deltas(9))
                        st.metric(label='FOULS DRAWN/90', value =self.involvement_stats[2], delta =self.get_deltas(10))
                        
                    with cols[2]:
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.write('')
                        st.metric(label='PASSES TO 3RD/90', value =self.involvement_stats[3], delta =self.get_deltas(11))
                        st.metric(label='PROG CARRIES/90', value =self.involvement_stats[4], delta =self.get_deltas(12))
                        st.metric(label='PROG PASSES/90', value =self.involvement_stats[5], delta =self.get_deltas(13))  

                with tabs[2]:
                    cols = st.columns([8,4,4])
                    with cols[0]:
                        st.image(f'players/{self.image_path}.png', width=self.width)
                    with cols[1]:
                        st.write('')
                        st.metric(label='SHOTS/90', value =self.scoring_stats[0], delta =self.get_deltas(14))
                        st.metric(label='ON TARGET/90', value =self.scoring_stats[1], delta =self.get_deltas(15))
                        st.metric(label='SHOT ACCURACY', value =str(self.scoring_stats[2]) + '%', delta =self.get_deltas(16))
                        st.metric(label='FINISHING ACCURACY', value =str(self.scoring_stats[3]) + '%', delta =self.get_deltas(17))     
                    with cols[2]:
                        st.write('')
                        st.metric(label='ASSISTS/90', value =self.scoring_stats[4], delta =self.get_deltas(18))
                        st.metric(label='GOALS/90', value =self.scoring_stats[5], delta =self.get_deltas(19))
                        st.metric(label='KEY PASSES/90', value =self.scoring_stats[6], delta =self.get_deltas(20))
                        st.metric(label='PASSES TO PEN/90', value =self.scoring_stats[7], delta =self.get_deltas(21))     
