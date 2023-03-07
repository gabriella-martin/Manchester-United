import psycopg2
import streamlit as st

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'database-1.c0lrvxe9frij.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = st.secrets['DATABASE_PASSWORD'] 
PORT = 5432
DATABASE = 'football'

class PlayerStatFormatting:
    
    def __init__(self, player,):
        self.player = player
        ninentys_played_query = f"""SELECT ninteys from players WHERE name = '{self.player}'  ;"""
        position_query = f"""SELECT position from players WHERE name = '{self.player}';"""
        number_query =  f"""SELECT number from players WHERE name = '{self.player}'  ;"""
        with psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, dbname=DATABASE, port=PORT) as conn:
            self.conn = conn
        with self.conn.cursor() as cur:
            cur.execute(ninentys_played_query)
            self.ninetys = (cur.fetchall())[0][0]
            cur.execute(position_query)
            self.position = (cur.fetchall())[0][0]
            cur.execute(number_query)
            self.number = (cur.fetchall())[0][0]
            cur.close()

    def get_general_stats(self):
        general_stat_list = ['age', 'salary', 'estimated_market_value', 'touches', 'passes_com','passes_com_s','passes_com_m','passes_com_l']
        player_general_stats = []
        with self.conn.cursor() as cur:
            for i in general_stat_list:
                q = f"""SELECT {i}
                    FROM players WHERE name = '{self.player}'
                    ;"""
                cur.execute(q)
                records = cur.fetchall()    
                for i in records:
                    i = i[0]
                    i = float(i)
                    player_general_stats.append(i)
            cur.close()  
        
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
        player_threat_stats = []
        with self.conn.cursor() as cur:
            for i in threat_stats:
                q = f"""SELECT {i}
                    FROM players WHERE name = '{self.player}'
                    ;"""
                cur.execute(q)
                records = cur.fetchall()    
                for i in records:
                    i = i[0]
                    i = float(i)
                    player_threat_stats.append(i)
            cur.close()         

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
        with self.conn.cursor() as cur:
            for i in upfield_stats:
                q = f"""SELECT {i}
                    FROM players WHERE name = '{self.player}'
                    ;"""
                cur.execute(q)
                records = cur.fetchall()    
                for i in records:
                    i = i[0]
                    i = float(i)
                    player_upfield_stats.append(i)
            cur.close()      
        player_upfield_stats = [round(x/self.ninetys,1) for x in player_upfield_stats]

        return player_upfield_stats
    
    def get_upfield_play_stats(self):
        upfield_stats = ['shots', 'shots_on_target', 'assists', 'goals', 'progressive_carries', 'progressive_passes', 'key_passes','passes_into_pen' ]
        player_upfield_stats = []
        with self.conn.cursor() as cur:
            for i in upfield_stats:
                q = f"""SELECT {i}
                    FROM players WHERE name = '{self.player}'
                    ;"""
                cur.execute(q)
                records = cur.fetchall()
                for i in records:
                    i = i[0]
                    i = float(i)
                    player_upfield_stats.append(i)
            cur.close()

        player_upfield_stats = [round(x/self.ninetys,1) for x in player_upfield_stats]
        return player_upfield_stats

    def get_forward_involvement_stats(self):
        forward_involvement_stats = ['touches_att_third', 'touches_att_pen', 'fouls_drawn', 'passes_into_third', 'progressive_carries', 'progressive_passes']
        player_involvement_stats = []
        with self.conn.cursor() as cur:
            for i in forward_involvement_stats:
                q = f"""SELECT {i}
                    FROM players WHERE name = '{self.player}'
                    ;"""
                cur.execute(q)
                records = cur.fetchall()
                for i in records:
                    i = i[0]
                    i = float(i)
                    player_involvement_stats.append(i)
            cur.close()
        player_involvement_stats = [round(x/self.ninetys,1) for x in player_involvement_stats]
        return player_involvement_stats

    def get_goal_scoring_stats(self):
        goal_scoring_stats = ['shots', 'shots_on_target', 'assists', 'goals', 'key_passes', 'passes_into_pen']
        player_scoring_stats = []
        with self.conn.cursor() as cur:
            for i in goal_scoring_stats:
                q = f"""SELECT {i}
                    FROM players WHERE name = '{self.player}'
                    ;"""
                cur.execute(q)
                records = cur.fetchall()
                for i in records:
                    i = i[0]
                    i = float(i)
                    player_scoring_stats.append(i)
            cur.close()  



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
        with self.conn.cursor() as cur:
            for i in goalkeeper_stats:
                q = f"""SELECT {i}
                    FROM players WHERE name = '{self.player}'
                    ;"""
                cur.execute(q)
                records = cur.fetchall()
                for i in records:
                    i = i[0]
                    i = float(i)
                    player_goalkeeping_stats.append(i)
            cur.close()
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
            

            
    