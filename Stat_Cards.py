import streamlit as st
from Pipelines.ServingData_Pipeline import PlayerStatFormatting
from Pipelines.AveragePlayer_Pipeline import ClubStatFormatting
class StatCard:

    def __init__(self,position,player=None,club=None,delta=None):
        self.club = club
        self.player = player
        self.position = position
        self.delta = delta
        #comparison cards with deltas are larger so make picture also large
        if self.delta != None:
            self.width = 425
        else:
            self.width = 335
        if self.club != None:
            self.image_path=((self.club).lower())
            self.player_stats = ClubStatFormatting(club=self.club, position=self.position)
        else:
            self.image_path = ((self.player.split(' '))[-1]).lower()
            self.player_stats = PlayerStatFormatting(player)
            self.number = self.player_stats.number
        
        self.general_stats = self.player_stats.format_general_stats()
        if self.position == 'DF':
            self.threat_stats = self.player_stats.format_threat_stats()
            self.def_upfield_stats = self.player_stats.get_def_upfield_play_stats()
        elif self.position ==  'MF':
            self.threat_stats = self.player_stats.format_threat_stats()
            self.upfield_stats = self.player_stats.get_upfield_play_stats()
        elif self.position == 'FW':
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
        cols = st.columns([8,4.5,4.5])
        with cols[0]:
            st.image(f'resources/{self.image_path}.png', width=self.width,)
        with cols[1]:
            st.write('')
            for i in range(1,3):
                if self.general_stats[i] > 1000000:
                    self.general_stats[i]  = str(round(((self.general_stats[i] ))/1000000,1)) +'m'
                elif self.general_stats[i]> 10000:
                    self.general_stats[i] = str(round(((self.general_stats[i]))/1000)) + 'k'

            st.metric(label='age', value =round(self.general_stats[0]), delta=self.get_deltas(0))
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
        cols = st.columns([8,4.5,4.5])
        with cols[0]:
            st.image(f'resources/{self.image_path}.png', width=self.width)
        with cols[1]:
            st.write('')
            st.metric(label='shot-blocks/90', value =self.threat_stats[0], delta=self.get_deltas(8))
            st.metric(label='blocks/90', value =self.threat_stats[1], delta=self.get_deltas(9))
            st.metric(label='interceptions/90', value =self.threat_stats[2], delta=self.get_deltas(10))
            st.metric(label='clearances/90', value =self.threat_stats[3], delta=self.get_deltas(11))
        with cols[2]:
            st.write('')
            st.metric(label='tackles/90', value =self.threat_stats[4], delta=self.get_deltas(12))
            st.metric(label='tackle success', value =str(self.threat_stats[5]) + '%', delta=self.get_deltas(13))
            try:
                st.metric(label='takeon success', value =str(round(self.threat_stats[6])) + '%', delta=self.get_deltas(14) )
            except TypeError:
                st.metric(label='takeon success', value ='NA' + '%', delta=self.get_deltas(14) )
            st.metric(label='fouls/90', value =self.threat_stats[7], delta=self.get_deltas(15))  
        return cols
    
    def get_def_upfield_stats(self):
        cols = st.columns([8,4.5,4.5])
        with cols[0]:
            st.image(f'resources/{self.image_path}.png', width=self.width)
        with cols[2]:
            st.write('')
            st.metric(label='prog carries/90', value =self.def_upfield_stats[0], delta=self.get_deltas(16))
            st.metric(label='prog passes/90', value =self.def_upfield_stats[1], delta=self.get_deltas(17))
            st.metric(label='pass to 3rd/90', value =self.def_upfield_stats[2], delta=self.get_deltas(18))
            st.metric(label='key passes/90', value =self.def_upfield_stats[3], delta=self.get_deltas(19))
        return cols
    
    def get_upfield_stats(self):
        cols = st.columns([8,4.5,4.5])
        with cols[0]:
            st.image(f'resources/{self.image_path}.png', width=self.width)
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
        cols = st.columns([8,4.5,4.5])
        with cols[0]:
            st.image(f'resources/{self.image_path}.png', width=self.width)
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
        cols = st.columns([8,4.5,4.5])
        with cols[0]:
            st.image(f'resources/{self.image_path}.png', width=self.width)
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
        if self.club != None:
            expander = st.expander(label=f'**{self.club}: {self.position} Average**', expanded=True )
        else:
            expander = st.expander(label=f'**{self.player}: {int(self.number)}**', expanded=True )
        if self.position == 'DF':
            with expander:
                tabs = st.tabs(DF_tabs)
                with tabs[0]:
                    self.get_general_stats()
                with tabs[1]:
                    self.get_threat_handling_stats()
                with tabs[2]:
                    self.get_def_upfield_stats()
        elif self.position ==  'MF':
            with expander:
                tabs = st.tabs(MF_tabs)
                with tabs[0]:
                    self.get_general_stats()
                with tabs[1]:
                    self.get_threat_handling_stats()
                with tabs[2]:
                    self.get_upfield_stats()
        elif self.position == 'FW':
            with expander:
                tabs = st.tabs(FW_tabs)
                with tabs[0]:
                    self.get_general_stats()
                with tabs[1]:
                    self.get_involvement_stats()
                with tabs[2]:
                    self.get_scoring_stats()
        return expander



def get_deltas(first_choice_stats, second_choice_stats):

    delta_list_card1 = []
    delta_list_card2 = []
    for index, value in enumerate(first_choice_stats):
        if second_choice_stats[index] != 0:
            try:
                delta1 = round(((value - second_choice_stats[index])/(second_choice_stats[index]))*100)
            except TypeError:
                delta1 = 'NA'
        else: 
            delta1 = 'NA'
        delta_list_card1.append(delta1)
        if value != 0:
            try:
                delta2 = round(((second_choice_stats[index]-value )/(value))*100)
            except TypeError:
                delta2 = 'NA'
        else: 
            delta2 = 'NA'            
        delta_list_card2.append(delta2)
    return delta_list_card1, delta_list_card2
