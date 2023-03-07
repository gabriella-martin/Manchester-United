import pandas as pd
import psycopg2
import streamlit as st

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'database-1.c0lrvxe9frij.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = st.secrets['DATABASE_PASSWORD'] 
PORT = 5432
DATABASE = 'football'

class ClubGeneralStats:
    def __init__(self, club):
        self.club = club
        club_query = f'''SELECT * from fixtures WHERE (home_team ='{self.club}' or away_team = '{self.club}') and home_goals is not NULL order by Date Asc ;'''
        match_results = []
        with psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, dbname=DATABASE, port=PORT) as conn:
            with conn.cursor() as cur:
                cur.execute(club_query)
                records = cur.fetchall()
                for i in records:
                    match_results.append(i)
                    
        self.match_results = match_results

    
    def get_match_results(self):
        
        #each match is of the following format; date, home team, home goals, away goals & away team

        point_list = []
        goals_scored = []
        goals_conceeded = []
        opponents = []
       
        for match in self.match_results:
            
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



