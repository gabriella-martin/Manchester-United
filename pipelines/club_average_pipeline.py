'''from decouple import config
from sqlalchemy import create_engine

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'database-1.c0lrvxe9frij.eu-west-2.rds.amazonaws.com' # Change it to your AWS endpoint
USER = 'postgres'
PASSWORD = config('DATABASE_PASSWORD')
PORT = 5432
DATABASE = 'football'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")

print(engine.table_names())
'''
import pandas as pd
from pandasql import sqldf
import streamlit as st
pysqldf = lambda q: sqldf(q, globals())

df = pd.read_csv('Master.csv',index_col=0)

class ClubStatFormatting:
    
    def __init__(self, club, position):
        self.club = club
        self.position = position
        ninentys_played_query = f"""SELECT SUM(ninteys) from df WHERE club = '{self.club}' AND ninteys >1  and position='{self.position}';"""
        self.ninetys = ((pysqldf(ninentys_played_query)).values)[0][0]



    def get_general_stats(self):
        general_stat_list = ['age', 'salary', 'estimated_market_value', 'touches', 'passes_com','passes_com_s','passes_com_m','passes_com_l']
        index_of_stats_to_be_summed = [3]
        player_general_stats = []
        for index, value in enumerate(general_stat_list):
            if index in index_of_stats_to_be_summed:
             q = f"""SELECT sum({value})
                    FROM df WHERE club = '{self.club}' and position = '{self.position}'
                    ;"""
            else:
                q = f"""SELECT avg({value})
                    FROM df WHERE club = '{self.club}' and position = '{self.position}'
                    ;"""
            general_stat_values = (pysqldf(q)).values
            for i in general_stat_values:
                player_general_stats.append(i.tolist())
        player_general_stats = [num for sublist in player_general_stats for num in sublist]

        return player_general_stats

    def format_general_stats(self):
        player_general_stats = self.get_general_stats()
        for index, value in enumerate(player_general_stats):
            #touches per 90 min
            if index == 3:
                player_general_stats[index] = round(value/self.ninetys)

        return player_general_stats
    
    def get_threat_handling_stats(self):
        threat_stats = ['shot_blocks', 'blocks', 'interceptions', 'clearances', 'total_tackles', 'successful_tackles','sucessful_takeons', 'fouls_committed' ]
        index_of_stats_to_be_averaged = [6]
        player_threat_stats = []
        for index, value in enumerate(threat_stats):
            if index in index_of_stats_to_be_averaged:
                q = f"""SELECT AVG({value})
                FROM df WHERE club = '{self.club}' and position = '{self.position}'
                ;"""
            else:
                q = f"""SELECT SUM({value})
                    FROM df WHERE club = '{self.club}' and position = '{self.position}'
                    ;"""
            threat_stat_values = (pysqldf(q)).values
            for i in threat_stat_values:
                player_threat_stats.append(i.tolist())
        player_threat_stats = [num for sublist in player_threat_stats for num in sublist]

        return player_threat_stats


    def format_threat_stats(self):
        player_threat_stats = self.get_threat_handling_stats()
        try:
            tackle_success = round((player_threat_stats[5]/player_threat_stats[4])*100)
        except ZeroDivisionError:
            tackle_success = 'NA'
        for index, value in enumerate(player_threat_stats):
            try:    
                # change successful tackle count to a % of tackles successful
                if index == 5:
                    player_threat_stats[index] = tackle_success
                    
                elif index in range(0,5) or index == 7:
                    player_threat_stats[index] = round(value/self.ninetys,1)
            except TypeError:
                pass
        
        return player_threat_stats   


    def get_def_upfield_play_stats(self):
        upfield_stats = ['progressive_carries', 'progressive_passes', 'passes_into_third', 'key_passes' ]
        player_upfield_stats = []
        for i in upfield_stats:
            q = f"""SELECT SUM({i})
                FROM df WHERE club = '{self.club}' and position = '{self.position}'
                ;"""
            threat_stat_values = (pysqldf(q)).values
            for i in threat_stat_values:
                player_upfield_stats.append(i.tolist())
        player_upfield_stats = [num for sublist in player_upfield_stats for num in sublist]
        player_upfield_stats = [round(x/self.ninetys,1) for x in player_upfield_stats]

        return player_upfield_stats
    
    def get_upfield_play_stats(self):
        upfield_stats = ['shots', 'shots_on_target', 'assists', 'goals', 'progressive_carries', 'progressive_passes', 'key_passes','passes_into_pen' ]
        player_upfield_stats = []
        for i in upfield_stats:
            q = f"""SELECT SUM({i})
                FROM df WHERE club = '{self.club}'
                ;"""
            threat_stat_values = (pysqldf(q)).values
            for i in threat_stat_values:
                player_upfield_stats.append(i.tolist())
        player_upfield_stats = [num for sublist in player_upfield_stats for num in sublist]
        player_upfield_stats = [round(x/self.ninetys,1) for x in player_upfield_stats]

        return player_upfield_stats

    def get_forward_involvement_stats(self):
        forward_involvement_stats = ['touches_att_third', 'touches_att_pen', 'fouls_drawn', 'passes_into_third', 'progressive_carries', 'progressive_passes']
        player_involvement_stats = []
        for i in forward_involvement_stats:
            q = f"""SELECT SUM({i})
                FROM df WHERE club = '{self.club}' and position = '{self.position}'
                ;"""
            involvement_stat_values = (pysqldf(q)).values
            for i in involvement_stat_values:
                player_involvement_stats.append(i.tolist())
        player_involvement_stats = [num for sublist in player_involvement_stats for num in sublist]
        player_involvement_stats = [round(x/self.ninetys,1) for x in player_involvement_stats]
        
        return player_involvement_stats

    def get_goal_scoring_stats(self):
        goal_scoring_stats = ['shots', 'shots_on_target', 'assists', 'goals', 'key_passes', 'passes_into_pen']
        player_scoring_stats = []
        for i in goal_scoring_stats:
            q = f"""SELECT SUM({i})
                FROM df WHERE club = '{self.club}' and position = '{self.position}'
                ;"""
            scoring_stat_values = (pysqldf(q)).values
            for i in scoring_stat_values:
                player_scoring_stats.append(i.tolist())
        player_scoring_stats = [num for sublist in player_scoring_stats for num in sublist]

        return player_scoring_stats
    
    def format_goal_scoring_stats(self):
        player_scoring_stats = self.get_goal_scoring_stats()
        shot_accuracy = round((player_scoring_stats[1]/player_scoring_stats[0])*100)
        finishing_accuracy = round((player_scoring_stats[3]/player_scoring_stats[1])*100)
        player_scoring_stats = [round(x/self.ninetys,1) for x in player_scoring_stats]
        player_scoring_stats.insert(2, shot_accuracy)
        player_scoring_stats.insert(3, finishing_accuracy)
        return player_scoring_stats
    
    def get_goalkeeping_stats(self):
        goalkeeper_stats = ['goals_conceeded', 'shots_on_target_against', 'saves', 'clean_sheets']
        player_goalkeeping_stats = []
        for i in goalkeeper_stats:
            q = f"""SELECT SUM({i})
                FROM df WHERE club = '{self.club}'
                ;"""
            goalkeeping_stat_values = (pysqldf(q)).values
            for i in goalkeeping_stat_values:
                player_goalkeeping_stats.append(i.tolist())
        player_goalkeeping_stats = [num for sublist in player_goalkeeping_stats for num in sublist]
        
        return player_goalkeeping_stats
    
    def format_goalkeeping_stats(self):
        player_goalkeeping_stats = self.get_goalkeeping_stats()
        save_percentage = round((player_goalkeeping_stats[2]/player_goalkeeping_stats[1])*100)
        clean_sheets_percentage = round((player_goalkeeping_stats[3]/self.ninetys)*100)
        goals_conceeded_per_90 =round((player_goalkeeping_stats[0]/self.ninetys),2)
        saves_per_90 = round((player_goalkeeping_stats[2]/self.ninetys),1)
        player_goalkeeping_stats = []
        player_goalkeeping_stats.append(save_percentage)
        player_goalkeeping_stats.append(goals_conceeded_per_90)
        player_goalkeeping_stats.append(clean_sheets_percentage)
        player_goalkeeping_stats.append(saves_per_90)
        return player_goalkeeping_stats
        

