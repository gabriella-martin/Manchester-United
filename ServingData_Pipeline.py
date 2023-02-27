import pandas as pd
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

df = pd.read_csv('Player.csv')



class PlayerStatFormatting:
    
    def __init__(self, player):
        self.player = player
        ninentys_played_query = f"""SELECT ninteys from df WHERE name = '{self.player}'  ;"""
        position_query = f"""SELECT position from df WHERE name = '{self.player}';"""
        number_query =  f"""SELECT number from df WHERE name = '{self.player}'  ;"""
        self.number = ((pysqldf(number_query)).values)[0][0]
        self.ninetys = ((pysqldf(ninentys_played_query)).values)[0][0]
        self.position = ((pysqldf(position_query)).values)[0][0]

    def get_general_stats(self):
        general_stat_list = ['age', 'salary', 'estimated_market_value', 'touches', 'passes_com','passes_com_s','passes_com_m','passes_com_l']
        player_general_stats = []
        for i in general_stat_list:
            q = f"""SELECT {i}
                FROM df WHERE name = '{self.player}'
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
            #formatting salary and market value to human readable
            try:
                if value > 1000000:
                    player_general_stats[index] = str(round(((value))/1000000,1)) +'m'
                elif value> 10000:
                    player_general_stats[index] = str(round(((value))/1000)) + 'k'
            except TypeError:
                pass

        return player_general_stats
    
    def get_threat_handling_stats(self):
        threat_stats = ['shot_blocks', 'blocks', 'interceptions', 'clearances', 'total_tackles', 'successful_tackles','sucessful_takeons', 'fouls_committed' ]
        player_threat_stats = []
        for i in threat_stats:
            q = f"""SELECT {i}
                FROM df WHERE name = '{self.player}'
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
                elif index in range(0,4) or index == 7:
                    player_threat_stats[index] = round(value/self.ninetys,1)
            except TypeError:
                pass
        try:
            player_threat_stats[5] = round(player_threat_stats[5]/self.ninetys,1)
        except TypeError:
            player_threat_stats[5] = 'NA'
        return player_threat_stats   


    def get_def_upfield_play_stats(self):
        upfield_stats = ['progressive_carries', 'progressive_passes', 'passes_into_third', 'key_passes' ]
        player_upfield_stats = []
        for i in upfield_stats:
            q = f"""SELECT {i}
                FROM df WHERE name = '{self.player}'
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
            q = f"""SELECT {i}
                FROM df WHERE name = '{self.player}'
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
            q = f"""SELECT {i}
                FROM df WHERE name = '{self.player}'
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
            q = f"""SELECT {i}
                FROM df WHERE name = '{self.player}'
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
    
