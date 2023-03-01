import pandas as pd
import requests 
from bs4 import BeautifulSoup 

# PLAYER FOOTBALL STATS

# run this after each game for up-to-date results
from unidecode import unidecode
urls = {'Manchester-United':['https://fbref.com/en/squads/19538871/Manchester-United-Stats', 'https://salarysport.com/football/premier-league/manchester-united-f.c./', 'https://www.footballtransfers.com/en/teams/uk/man-utd', 'https://www.premierleague.com/clubs/12/Manchester-United/squad'],
'Manchester-City': ['https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats', 'https://salarysport.com/football/premier-league/manchester-city-f.c./', 'https://www.footballtransfers.com/en/teams/uk/man-city', 'https://www.premierleague.com/clubs/11/Manchester-City/squad'], 'Arsenal': [
    'https://fbref.com/en/squads/18bb7c10/Arsenal-Stats', 'https://salarysport.com/football/premier-league/arsenal-f.c./', 'https://www.footballtransfers.com/en/teams/uk/arsenal', 'https://www.premierleague.com/clubs/1/Arsenal/squad'], 
    'Tottenham': ['https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats','https://salarysport.com/football/premier-league/tottenham-hotspur-f.c./','https://www.footballtransfers.com/en/teams/uk/tottenham', 'https://www.premierleague.com/clubs/21/Tottenham-Hotspur/squad'],
     'Newcastle': ['https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats', 'https://salarysport.com/football/premier-league/newcastle-united-f.c./', 'https://www.footballtransfers.com/en/teams/uk/newcastle-utd', 'https://www.premierleague.com/clubs/23/Newcastle-United/squad'],
      'Fulham' : ['https://fbref.com/en/squads/fd962109/Fulham-Stats','https://salarysport.com/football/premier-league/newcastle-united-f.c./','https://www.footballtransfers.com/en/teams/uk/newcastle-utd','https://www.premierleague.com/clubs/34/Fulham/squad'] }

data_type = ['Data', 'Salary', 'Market-Value', 'Number']
'''
for key, value in urls.items():
    for index, url in enumerate(value):
        response = requests.get(url)
        with open (f'{key}-{data_type[index]}', 'wb') as p:
            p.write(response.content)'''

clubs = ['Manchester-United', 'Manchester-City', 'Arsenal', 'Tottenham', 'Newcastle', 'Fulham']

class BrefParser:
    
    def __init__(self, club):
        self.club = club
        with open(f'{self.club}-Data', 'rb') as pd:
            self.soup = BeautifulSoup(pd.read(), 'html.parser')
            
    def standard_stats_table(self):
        list_of_player_stats = []
        table_body = self.soup.find("div", { "id" : "all_stats_standard" })
        rows = table_body.find_all("tr")
        # first two rows are not data 
        for i in rows[2:-2]:

            player = []
            # only want players who have actually played
            matches_played = (i.find('td', {'data-stat':'games'})).text
            if matches_played == '0':
                continue
            name = i.a.text
            name = unidecode(name)
            nationality = ((i.find('td', {'data-stat':'nationality'})).text)[-3:]
            position = (i.find('td', {'data-stat':'position'})).text
            if len(position) > 2:
                position = position[:2]
            age = ((i.find('td', {'data-stat':'age'})).text)[:2]
            starts = (i.find('td', {'data-stat':'games_starts'})).text
            minutes = (i.find('td', {'data-stat':'minutes'})).text
            minutes = int(minutes.replace(',',''))
            ninetys = ((i.find('td', {'data-stat':'minutes_90s'})).text)
            goals = (i.find('td', {'data-stat':'goals'})).text
            assists = (i.find('td', {'data-stat':'assists'})).text
            cards_yellow = (i.find('td', {'data-stat':'cards_yellow'})).text
            cards_red = (i.find('td', {'data-stat':'cards_red'})).text
            progressive_carries = (i.find('td', {'data-stat':'progressive_carries'})).text
            progressive_passes = (i.find('td', {'data-stat':'progressive_passes'})).text
            player_list = [name, nationality, position, age, matches_played, starts, minutes, ninetys,  goals, assists, cards_yellow, cards_red, progressive_carries, progressive_passes]
            for stat in player_list:
                player.append(stat)


            list_of_player_stats.append(player)
        return(list_of_player_stats)

    def goalkeeper_stats_table(self):
        list_of_player_stats = self.standard_stats_table()            
        table_body = self.soup.find("div", { "id" : "div_stats_keeper_9" })
        rows = table_body.find_all("tr")
        for i in rows[2:-2]:

            for player in list_of_player_stats:
                name = i.a.text
                if name in player[0]:
                    goals_conceeded = (i.find('td', {'data-stat':'gk_goals_against'})).text
                    shots_on_target_against = (i.find('td', {'data-stat':'gk_shots_on_target_against'})).text
                    saves = (i.find('td', {'data-stat':'gk_saves'})).text
                    clean_sheets = (i.find('td', {'data-stat':'gk_clean_sheets'})).text
                    goal_keeping = goals_conceeded, shots_on_target_against, saves, clean_sheets
                    for stat in goal_keeping:
                        player.append(stat)

        # filing non goalkeeper statistics with null
        for player in list_of_player_stats:
            if len(player) == 14:
                for i in range(0,4):
                    player.append('NULL')

        return list_of_player_stats

    def shooting_stats_table(self):
        list_of_player_stats = self.goalkeeper_stats_table()       

        table_body = self.soup.find("div", { "id" : "div_stats_shooting_9" })
        rows = table_body.find_all("tr")    

        for index, value in enumerate(rows[2:-2]):
            
                shots = (value.find('td', {'data-stat':'shots'})).text
                shots_on_target = (value.find('td', {'data-stat':'shots_on_target'})).text
                list_of_player_stats[index].append(shots)
                list_of_player_stats[index].append(shots_on_target)
        return list_of_player_stats
        
    def passing_stats_table(self):

        list_of_player_stats = self.shooting_stats_table()
        table_body = self.soup.find("div", { "id" : "div_stats_passing_9" })
        rows = table_body.find_all("tr")    

        for index, value in enumerate(rows[2:-2]):

                passes_com = (value.find('td', {'data-stat':'passes_pct'})).text
                passes_com_short = (value.find('td', {'data-stat':'passes_pct_short'})).text
                passes_com_medium = (value.find('td', {'data-stat':'passes_pct_medium'})).text
                passes_com_long = (value.find('td', {'data-stat':'passes_pct_long'})).text
                key_passes = (value.find('td', {'data-stat':'assisted_shots'})).text
                passes_into_third = (value.find('td', {'data-stat':'passes_into_final_third'})).text
                passes_into_pen = (value.find('td', {'data-stat':'passes_into_penalty_area'})).text
                passing_stats = [passes_com, passes_com_short, passes_com_medium, passes_com_long, key_passes, passes_into_third, passes_into_pen]
                for stat in passing_stats:
                    list_of_player_stats[index].append(stat)
        return list_of_player_stats

    def possession_stats_table(self):
        list_of_player_stats = self.passing_stats_table()
        table_body = self.soup.find("div", { "id" : "div_stats_possession_9" })
        rows = table_body.find_all("tr")    

        for index, value in enumerate(rows[2:-2]):

                touches = (value.find('td', {'data-stat':'touches'})).text
                touches_def_pen = (value.find('td', {'data-stat':'touches_def_pen_area'})).text
                touches_def_third = (value.find('td', {'data-stat':'touches_def_3rd'})).text
                touches_mid_third = (value.find('td', {'data-stat':'touches_mid_3rd'})).text
                touches_att_third = (value.find('td', {'data-stat':'touches_att_3rd'})).text
                touches_att_pen = (value.find('td', {'data-stat':'touches_att_pen_area'})).text
                sucessful_takeons = (value.find('td', {'data-stat':'take_ons_won_pct'})).text
                possesion_stats = [touches, touches_def_pen, touches_def_third, touches_mid_third, touches_att_third, touches_att_pen, sucessful_takeons]
                for stat in possesion_stats:
                    list_of_player_stats[index].append(stat)
        return list_of_player_stats

    def misc_stats_table(self):
        list_of_player_stats = self.possession_stats_table()
        table_body = self.soup.find("div", { "id" : "div_stats_misc_9" })
        rows = table_body.find_all("tr")    

        for index, value in enumerate(rows[2:-2]):
                aerial_duels_won = (value.find('td', {'data-stat':'aerials_won_pct'})).text
                fouls_committed = (value.find('td', {'data-stat':'fouls'})).text
                fouls_drawns = (value.find('td', {'data-stat':'fouled'})).text
                list_of_player_stats[index].append(aerial_duels_won)
                list_of_player_stats[index].append(fouls_committed)
                list_of_player_stats[index].append(fouls_drawns)
        return list_of_player_stats

    def defending_stats_table(self):
        list_of_player_stats = self.misc_stats_table()
        table_body = self.soup.find("div", { "id" : "div_stats_defense_9" })
        rows = table_body.find_all("tr")    

        for index, value in enumerate(rows[2:-2]):
                total_tackles = (value.find('td', {'data-stat':'tackles'})).text
                successful_tackles = (value.find('td', {'data-stat':'tackles_won'})).text
                percent_of_dribblers_tackled = (value.find('td', {'data-stat':'challenge_tackles_pct'})).text
                blocks = (value.find('td', {'data-stat':'blocks'})).text
                shot_blocks = (value.find('td', {'data-stat':'blocked_shots'})).text
                interceptions = (value.find('td', {'data-stat':'interceptions'})).text
                clearances = (value.find('td', {'data-stat':'clearances'})).text
                defensive_stats = [total_tackles, successful_tackles, percent_of_dribblers_tackled, blocks, shot_blocks, interceptions, clearances]
                for stat in defensive_stats:
                    list_of_player_stats[index].append(stat)

        return list_of_player_stats

class SalaryParser:

    def __init__(self, club, list_of_player_stats):
        self.club = club
        with open(f'{self.club}-Salary', 'rb') as pd:
            self.soup = BeautifulSoup(pd.read(), 'html.parser')
        self.list_of_player_stats = list_of_player_stats
    
    def get_salary(self):

        tbody = self.soup.find_all('tbody')
        for table in tbody:
            for row in table:
                data = (row.find_all('td'))
                name = data[0].text
                try:
                    salary = (data[2].text)[1:]
                    salary = int(salary.replace(',',''))
                except IndexError:
                    continue
                for index, value in enumerate(self.list_of_player_stats):
                    if value[0].lower()in unidecode(name.lower()):
                        self.list_of_player_stats[index].append(salary)           
        for i in self.list_of_player_stats:
            if len(i) == 44:
                i.append('NULL')                  
        return self.list_of_player_stats

class MarketValueParser:

    def __init__(self,club, list_of_player_stats):
        self.club = club
        with open(f'{self.club}-Market-Value', 'rb') as pd:
            self.soup = BeautifulSoup(pd.read(), 'html.parser')
        self.list_of_player_stats = list_of_player_stats
    
    def get_market_worth(self):
        tbody = self.soup.find('table', class_ ='table table-striped-rowspan ft-table mb-0')
        rows = tbody.find_all('tr')
        rows = rows[2:]
        for row in rows:
            try:
                name = row.a.text
                worth = (row.find('span', class_ = 'player-tag').text)[1:-1]
                worth = float(worth) * 0.88
                worth = round(worth * 1000000, 0)
                for index, value in enumerate(self.list_of_player_stats):
                    if value[0].lower()in unidecode(name.lower()):
                        self.list_of_player_stats[index].append(worth)
                            
            except AttributeError:
                continue
        for i in self.list_of_player_stats:
            if len(i) == 45:
                i.append('NULL')
        return self.list_of_player_stats

class PlayerNumberParser:
    def __init__(self,club, list_of_player_stats):
        self.club = club
        with open(f'{self.club}-Number', 'rb') as pd:
            self.soup = BeautifulSoup(pd.read(), 'html.parser')
        self.list_of_player_stats = list_of_player_stats
    
    def get_player_number(self):
        tbody = self.soup.find_all('span', class_ ='playerCardInfo')
        for player in tbody:
            name = (player.find('h4')).text
            number = (player.find('span', class_ = 'number')).text
            for index, value in enumerate(self.list_of_player_stats):
                if value[0].lower() in unidecode(name.lower()) :
                    self.list_of_player_stats[index].append(number)
        for index, value in enumerate(self.list_of_player_stats):
            if len(str(value[-1])) > 2 :
                self.list_of_player_stats.pop(index)
        for i in self.list_of_player_stats:
            if len(i) == 46:
                i.append('NULL')
        return self.list_of_player_stats
 
class DataProcessing:

    def __init__(self, club, list_of_player_stats):
        self.club = club
        list_of_player_stats = list_of_player_stats
        for index, value in enumerate(list_of_player_stats):
            if len(value) >47:
                list_of_player_stats[index] = value[:-1]
    def remove_ronaldo(self):
        for index, player in enumerate(list_of_player_stats):
            if player[0] == 'Cristiano Ronaldo':
                list_of_player_stats.pop(index)

        return list_of_player_stats

    def empty_values_to_null(self):
        list_of_player_stats = self.remove_ronaldo()
        for player in list_of_player_stats:

            for index, data_point in enumerate(player):
                if data_point == '':
                    player[index] = 'NULL'

        return list_of_player_stats
    
    def add_club(self):
        list_of_player_stats = self.empty_values_to_null()
        for player in list_of_player_stats:
            player.append(self.club)
        return list_of_player_stats
    
    def export_to_csv(self):
        list_of_player_stats = self.add_club()


        fields = ['name', 'nationality', 'position', 'age', 'matches_played', 'starts', 'minutes', 'ninteys','goals',
        'assists', 'yellow_card', 'red_card', 'progressive_carries', 'progressive_passes', 'goals_conceeded', 'shots_on_target_against', 
        'saves', 'clean_sheets', 'shots', 'shots_on_target', 'passes_com', 'passes_com_s', 'passes_com_m',
        'passes_com_l', 'key_passes', 'passes_into_third', 'passes_into_pen', 'touches', 'touches_def_pen', 'touches_def_third', 
        'touches_mid_third', 'touches_att_third', 'touches_att_pen', 'sucessful_takeons', 'aerial_duels_won',
        'fouls_committed','fouls_drawn','total_tackles', 'successful_tackles', 'percent_of_dribblers_tackled', 'blocks', 'shot_blocks', 
        'interceptions', 'clearances', 'salary', 'estimated_market_value', 'number', 'club'] 
        
        df = pd.DataFrame(list_of_player_stats, columns=fields)

        df.to_csv(f'{self.club}-Players.csv')

        return df
    

if __name__ == '__main__':
        df_list = []
        for club in clubs:
            list_of_player_stats = BrefParser(club).defending_stats_table()
            list_of_player_stats = SalaryParser(club, list_of_player_stats).get_salary()
            list_of_player_stats = MarketValueParser(club, list_of_player_stats).get_market_worth()
            list_of_player_stats = PlayerNumberParser(club, list_of_player_stats).get_player_number()
            df = DataProcessing(club, list_of_player_stats).export_to_csv()
            df_list.append(df)

master_db = pd.concat(df_list, ignore_index=True)
master_db.to_csv('Master.csv')