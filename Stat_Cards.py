import streamlit as st
from Pipelines.ServingData_Pipeline import PlayerStatFormatting

class StatCard:

    def __init__(self,player,delta=None):
        self.player = player
        self.delta = delta

        #comparison cards with deltas are larger so make picture also large

        if self.delta != None:
            self.width = 425
        else:
            self.width = 335

        self.image_path = ((self.player.split(' '))[-1]).lower()
        self.player_stats = PlayerStatFormatting(player)
        self.number = self.player_stats.number
        self.player_position = self.player_stats.position
        self.general_stats = self.player_stats.format_general_stats()
        if self.player_position == 'DF':
            self.threat_stats = self.player_stats.format_threat_stats()
            self.upfield_stats = self.player_stats.get_def_upfield_play_stats()
        elif self.player_position ==  'MF':
            self.threat_stats = self.player_stats.format_threat_stats()
            self.upfield_stats = self.player_stats.get_upfield_play_stats()
        elif self.player_position == 'FW':
            self.involvement_stats = self.player_stats.get_forward_involvement_stats()
            self.scoring_stats = self.player_stats.format_goal_scoring_stats()

    def get_deltas(self, number):
        if self.delta != None:
            delta = str(self.delta[number]) + '%'
        else:
            #if not comparing then setting delta=None will remove deltas
            delta = None
        return delta

    def get_general_stats(self):
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

        return cols

    def get_threat_handling_stats(self):
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
        return cols
    
    def get_def_upfield_stats(self):
        cols = st.columns([8,5,5])
        with cols[0]:
            st.image(f'players/{self.image_path}.png', width=self.width)
        with cols[2]:
            st.write('')
            st.metric(label='prog carries/90', value =self.upfield_stats[0], delta=self.get_deltas(16))
            st.metric(label='prog passes/90', value =self.upfield_stats[1], delta=self.get_deltas(17))
            st.metric(label='pass to 3rd/90', value =self.upfield_stats[2], delta=self.get_deltas(18))
            st.metric(label='key passes/90', value =self.upfield_stats[3], delta=self.get_deltas(19))
        return cols
    
    def get_upfield_stats(self):
        cols = st.columns([8,5,5])
        with cols[0]:
            st.image(f'players/{self.image_path}.png', width=self.width)
        with cols[1]:
            st.write('')
            st.metric(label='shots/90', value =self.upfield_stats[0], delta =self.get_deltas(16))
            st.metric(label='on target/90', value =self.upfield_stats[1], delta =self.get_deltas(17))
            st.metric(label='assists/90', value =self.upfield_stats[2], delta =self.get_deltas(18))
            st.metric(label='goals/90', value =self.upfield_stats[3], delta =self.get_deltas(19))     
        with cols[2]:
            st.write('')
            st.metric(label='pass to pen/90', value =self.upfield_stats[4], delta =self.get_deltas(20))
            st.metric(label='prog passes/90', value =self.upfield_stats[5], delta =self.get_deltas(21))
            st.metric(label='prog carries/90', value =self.upfield_stats[6], delta =self.get_deltas(22))
            st.metric(label='key passes/90', value =self.upfield_stats[7], delta =self.get_deltas(23)) 
        return cols

    def get_involvement_stats(self):
        cols = st.columns([8,5,5])
        with cols[0]:
            st.image(f'players/{self.image_path}.png', width=self.width)
        with cols[1]:
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')

            st.metric(label='touches in 3rd/90', value =self.involvement_stats[0], delta =self.get_deltas(8))
            st.metric(label='touches in pen/90', value =self.involvement_stats[1], delta =self.get_deltas(9))
            st.metric(label='fouls drawn/90', value =self.involvement_stats[2], delta =self.get_deltas(10))
        
        with cols[2]:
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.metric(label='passes to 3rd/90', value =self.involvement_stats[3], delta =self.get_deltas(11))
            st.metric(label='prog carries/90', value =self.involvement_stats[4], delta =self.get_deltas(12))
            st.metric(label='prog passes/90', value =self.involvement_stats[5], delta =self.get_deltas(13)) 
        return cols
    
    def get_scoring_stats(self):
        cols = st.columns([8,5,5])
        with cols[0]:
            st.image(f'players/{self.image_path}.png', width=self.width)
        with cols[1]:
            st.write('')
            st.metric(label='shots/90', value =self.scoring_stats[0], delta =self.get_deltas(14))
            st.metric(label='on target/90', value =self.scoring_stats[1], delta =self.get_deltas(15))
            st.metric(label='shot accuracy', value =str(self.scoring_stats[2]) + '%', delta =self.get_deltas(16))
            st.metric(label='finishing accuracy', value =str(self.scoring_stats[3]) + '%', delta =self.get_deltas(17))     
        with cols[2]:
            st.write('')
            st.metric(label='assists/90', value =self.scoring_stats[4], delta =self.get_deltas(18))
            st.metric(label='goals/90', value =self.scoring_stats[5], delta =self.get_deltas(19))
            st.metric(label='key passes/90', value =self.scoring_stats[6], delta =self.get_deltas(20))
            st.metric(label='passes to pen/90', value =self.scoring_stats[7], delta =self.get_deltas(21))     
        return cols

    def create_card(self):

        DF_tabs = ['General', 'Threat-Handling', 'Upfield Play']
        MF_tabs = ['General', 'Threat-Handling', 'Upfield Play']
        FW_tabs = ['General', 'Game-Involvement', 'Goal-Involvement']
        expander = st.expander(label=f'**{self.player}: {self.number}**', expanded=True )
        if self.player_position == 'DF':
            with expander:
                tabs = st.tabs(DF_tabs)
                with tabs[0]:
                    self.get_general_stats()
                with tabs[1]:
                    self.get_threat_handling_stats()
                with tabs[2]:
                    self.get_def_upfield_stats()
        elif self.player_position ==  'MF':
            with expander:
                tabs = st.tabs(MF_tabs)
                with tabs[0]:
                    self.get_general_stats()
                with tabs[1]:
                    self.get_threat_handling_stats()
                with tabs[2]:
                    self.get_upfield_stats()
        elif self.player_position == 'FW':
            with expander:
                tabs = st.tabs(FW_tabs)
                with tabs[0]:
                    self.get_general_stats()
                with tabs[1]:
                    self.get_involvement_stats()
                with tabs[2]:
                    self.get_scoring_stats()
        return expander
