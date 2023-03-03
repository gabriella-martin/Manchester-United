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
        for index, value in enumerate(self.match_results,1):
            match.append(value)
            if index % 5 == 0 or index == len(self.match_results):
                matches.append(match)
                match = []
        return matches
    
    def create_dataframe(self):
        point_list = []
        goals_scored = []
        goals_conceeded = []
        opponents = []
        matches = self.split_matches_from_match_results()
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
            elif (match[1] == self.club  and match[2] == match[3]) or (match[-1]== self.club and match[2] == match[3]):
                point_list.append(1)
                goals_scored.append(match[2])
                goals_conceeded.append(match[2])
                if match[1] == self.club:
                    opponents.append(match[-1])
                else:
                    opponents.append(match[1])
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
        net_goals = []
        matches_played =[]
        
        number_of_matches = len(matches)

        for i in range(0, number_of_matches):
            matches_played.append(i)

        for item1, item2 in zip(goals_scored, goals_conceeded):
            net_goals.append(item1-item2)

        df = pd.DataFrame({'Matches Played': matches_played ,'Points':point_list, 'Goals Scored': goals_scored, 'Goals Conceeded': goals_conceeded, 'Net Goals': net_goals})
        df['Points Sum'] = df['Points'].cumsum()
        df['Points CMA'] =df['Points'].expanding(1).mean()
        df['Goals Scored CMA'] =df['Goals Scored'].expanding(1).mean()
        df['Goals Conceeded CMA'] =df['Goals Conceeded'].expanding(1).mean()
        df['Net Goals CMA'] =df['Net Goals'].expanding(1).mean()
        return df