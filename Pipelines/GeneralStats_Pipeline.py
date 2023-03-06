import pandas as pd
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
df = pd.read_csv('Fixtures.csv')
import streamlit as st
class ClubGeneralStats:
    def __init__(self, club):
        self.club = club
        club_query = f'''SELECT * from df WHERE (home_team ='{self.club}' or away_team = '{self.club}') and home_score is not NULL order by Date Asc ;'''
        match_logs = pysqldf(club_query).values
        match_results = []
        for match in match_logs:
            match_results.append(match.tolist())
        self.match_results = [num for sublist in match_results for num in sublist]

    def split_matches_from_match_results(self):
        match = []
        matches = []

        #self.match_results is one long list of match data, each match has 5 datapoints, so split the list into 
        #lists of size 5

        for index, value in enumerate(self.match_results,1):
            match.append(value)
            if index % 5 == 0 or index == len(self.match_results):
                matches.append(match)
                match = []
        return matches
    
    def get_match_results(self):
        
        matches = self.split_matches_from_match_results()
        #each match is of the following format; date, home team, home goals, away goals & away team

        point_list = []
        goals_scored = []
        goals_conceeded = []
        opponents = []
       
        for match in matches:
            
            # home wins
            if match[1] == self.club and match[2] > match[3]:
                point_list.append(3)
                goals_scored.append(match[2])
                goals_conceeded.append(match[-2])
                opponents.append(match[-1])

            # away wins
            elif match[-1]== self.club and match[3] > match[2]:
                point_list.append(3)
                goals_scored.append(match[-2])
                goals_conceeded.append(match[2])
                opponents.append(match[1])

            # draws     
            elif (match[1] == self.club  and match[2] == match[3]) or (match[-1]== self.club and match[2] == match[3]):
                point_list.append(1)
                goals_scored.append(match[2])
                goals_conceeded.append(match[2])
                if match[1] == self.club:
                    opponents.append(match[-1])
                else:
                    opponents.append(match[1])

            # losses
            else:
                point_list.append(0)
                if match[1] == self.club:
                        goals_scored.append(match[2])
                        goals_conceeded.append(match[-2])
                        opponents.append(match[-1])
                else:
                    goals_scored.append(match[-2])
                    goals_conceeded.append(match[2])
                    opponents.append(match[1])
        return point_list, goals_scored, goals_conceeded, opponents
    
    def get_net_goals(self):

        net_goals = []
        point_list, goals_scored, goals_conceeded, opponents = self.get_match_results()
        for item1, item2 in zip(goals_scored, goals_conceeded):
            net_goals.append(item1-item2)

        return  point_list, goals_scored, goals_conceeded, opponents, net_goals
    
    def get_matches_played(self):

        #create a list of number of matches played at that given point to use as x axis

        point_list, goals_scored, goals_conceeded, opponents, net_goals = self.get_net_goals()
        matches_played =[]
        number_of_matches = len(point_list)

        for i in range(0, number_of_matches):
            matches_played.append(i)

        return matches_played, point_list, goals_scored, goals_conceeded, opponents, net_goals

    def create_club_dataframe(self):
        matches_played, point_list, goals_scored, goals_conceeded, opponents, net_goals = self.get_matches_played()
        df = pd.DataFrame({'Matches Played': matches_played ,'Points':point_list, 'Goals Scored': goals_scored, 'Goals Conceeded': goals_conceeded, 'Net Goals': net_goals, 'Opponents':opponents})
        df['Points Sum'] = df['Points'].cumsum()
        df['Points Rolling Average'] =df['Points'].expanding(1).mean()
        df['Goals Scored CMA'] =df['Goals Scored'].expanding(1).mean()
        df['Goals Conceeded CMA'] =df['Goals Conceeded'].expanding(1).mean()
        df['Net Goals CMA'] =df['Net Goals'].expanding(1).mean()
        return df
    
clubs = ['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton','Chelsea','Crystal Palace','Everton','Fulham','Leeds','Leicester','Liverpool','Manchester City','Manchester United','Newcastle','Nottingham Forest','Southampton','Tottenham','West Ham','Wolves']


def get_sum_of_points_for_each_club():
    list_of_points = []
    for club in clubs:
        results = ClubGeneralStats(club).get_match_results()
        total_points = sum(results[0])
        list_of_points.append(total_points)
    return list_of_points


list_of_points = get_sum_of_points_for_each_club()

club_points = pd.DataFrame({'Club':clubs, 'Points':list_of_points})


top_5_query=f'''SELECT Club from club_points where Club is not 'Manchester United' order by Points desc limit 5 ;'''

match_logs = pysqldf(top_5_query).values
match_results = []
for match in match_logs:
    match_results.append(match.tolist())
match_results = [num for sublist in match_results for num in sublist]


