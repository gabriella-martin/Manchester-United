
import csv
import requests 
from bs4 import BeautifulSoup

''' For this project I am using fbref.com to scrape most of my football data
    There are many different options to choose from, also using an
    API is another viable option but will probably cost money for the 
    size of the batch process'''

# PLAYER FOOTBALL STATS

# python3 BatchData_Pipeline.py

'''url = 'https://fbref.com/en/squads/19538871/Manchester-United-Stats'
response = requests.get(url)
with open ('Player-Data', 'wb') as p:
    p.write(response.content)'''
names = []
with open('Player-Data', 'rb') as pd:
    soup = BeautifulSoup(pd.read(), 'html.parser')

    #standard stats table first

    table_body = soup.find("div", { "id" : "all_stats_standard" })
    rows = table_body.find_all("tr")
    
    # first two rows are not data 
    player_stats = []
    
    for i in rows[2:]:
        try:

            # only want players who have actually played
            matches_played = (i.find('td', {'data-stat':'games'})).text
            if matches_played == '0':
                continue

            name = i.a.text
            nationality = ((i.find('td', {'data-stat':'nationality'})).text)[-3:]
            position = (i.find('td', {'data-stat':'position'})).text
            age = ((i.find('td', {'data-stat':'age'})).text)[:2]
            starts = (i.find('td', {'data-stat':'games_starts'})).text
            minutes = (i.find('td', {'data-stat':'minutes'})).text
            minutes = int(minutes.replace(',',''))
            goals = (i.find('td', {'data-stat':'goals'})).text
            assists = (i.find('td', {'data-stat':'assists'})).text
            y_card = (i.find('td', {'data-stat':'cards_yellow'})).text
            r_card = (i.find('td', {'data-stat':'cards_red'})).text
            pro_carries = (i.find('td', {'data-stat':'progressive_carries'})).text
            pro_passes = (i.find('td', {'data-stat':'progressive_passes'})).text
            player_list = [name, nationality, position, age, matches_played, starts, minutes, goals, assists, y_card, r_card, pro_carries, pro_passes]
            player_stats.append(player_list)
        except AttributeError:
            pass


                
    # goalkeeper stats

    table_body = soup.find("div", { "id" : "div_stats_keeper_9" })
    rows = table_body.find_all("tr")
    for i in rows[2:]:
        try:
            for player in player_stats:
                name = i.a.text
                if name in player[0]:
                    goals_conceeded = (i.find('td', {'data-stat':'gk_goals_against'})).text
                    shots_on_target_against = (i.find('td', {'data-stat':'gk_shots_on_target_against'})).text
                    saves = (i.find('td', {'data-stat':'gk_saves'})).text
                    clean_sheets = (i.find('td', {'data-stat':'gk_clean_sheets'})).text
                    player.append(goals_conceeded)
                    player.append(shots_on_target_against)
                    player.append(saves)
                    player.append(clean_sheets)

        except AttributeError:
            pass

    for player in player_stats:
        if len(player) == 13:
            (player.append('NULL'))
            (player.append('NULL'))
            (player.append('NULL'))
            (player.append('NULL'))

    # shooting stats        

    table_body = soup.find("div", { "id" : "div_stats_shooting_9" })
    rows = table_body.find_all("tr")    

    for index, value in enumerate(rows[2:-2]):
        
            shots = (value.find('td', {'data-stat':'shots'})).text
            shots_on_target = (value.find('td', {'data-stat':'shots_on_target'})).text
            player_stats[index].append(shots)
            player_stats[index].append(shots_on_target)


    # passing stats

    table_body = soup.find("div", { "id" : "div_stats_passing_9" })
    rows = table_body.find_all("tr")    

    for index, value in enumerate(rows[2:-2]):

            passes_com = (value.find('td', {'data-stat':'passes_pct'})).text
            passes_com_s = (value.find('td', {'data-stat':'passes_pct_short'})).text
            passes_com_m = (value.find('td', {'data-stat':'passes_pct_medium'})).text
            passes_com_l = (value.find('td', {'data-stat':'passes_pct_long'})).text
            key_passes = (value.find('td', {'data-stat':'assisted_shots'})).text
            passes_into_third = (value.find('td', {'data-stat':'passes_into_final_third'})).text
            crosses_into_pen = (value.find('td', {'data-stat':'crosses_into_penalty_area'})).text
            player_stats[index].append(passes_com)
            player_stats[index].append(passes_com_s)
            player_stats[index].append(passes_com_m)
            player_stats[index].append(passes_com_l)
            player_stats[index].append(key_passes)
            player_stats[index].append(passes_into_third)
            player_stats[index].append(crosses_into_pen)


    # possession stats

    table_body = soup.find("div", { "id" : "div_stats_possession_9" })
    rows = table_body.find_all("tr")    

    for index, value in enumerate(rows[2:-2]):

            touches = (value.find('td', {'data-stat':'touches'})).text
            t_def_pen = (value.find('td', {'data-stat':'touches_def_pen_area'})).text
            t_def_third = (value.find('td', {'data-stat':'touches_def_3rd'})).text
            t_mid_third = (value.find('td', {'data-stat':'touches_mid_3rd'})).text
            t_att_third = (value.find('td', {'data-stat':'touches_att_3rd'})).text
            t_att_pen = (value.find('td', {'data-stat':'touches_att_pen_area'})).text
            sucessful_takeons = (value.find('td', {'data-stat':'take_ons_won_pct'})).text
            player_stats[index].append(touches)
            player_stats[index].append(t_def_pen)
            player_stats[index].append(t_def_third)
            player_stats[index].append(t_mid_third)
            player_stats[index].append(t_att_third)
            player_stats[index].append(t_att_pen)
            player_stats[index].append(sucessful_takeons)

    # possession stats

    table_body = soup.find("div", { "id" : "div_stats_misc_9" })
    rows = table_body.find_all("tr")    

    for index, value in enumerate(rows[2:-2]):

            aerial_duels_won = (value.find('td', {'data-stat':'aerials_won_pct'})).text
            player_stats[index].append(aerial_duels_won)

# turning empty values to null
for player in player_stats:
    for index, data_point in enumerate(player):
        if data_point == '':
            player[index] = 'NULL'



# removing Ronaldo
for index, player in enumerate(player_stats):
    if player[0] == 'Cristiano Ronaldo':
        player_stats.pop(index)

# GETTING WAGE FROM ANOTHER SITE AS BREF NOT GOT ALL INFO

'''url = 'https://salarysport.com/football/premier-league/manchester-united-f.c./'
response = requests.get(url)
with open ('Player-Salary', 'wb') as p:
    p.write(response.content)'''

with open('Player-Salary', 'rb') as pd:
    soup = BeautifulSoup(pd.read(), 'html.parser')

tbody = soup.find_all('tbody')

for table in tbody:
    for row in table:
        data = (row.find_all('td'))
        name = data[0].text
        try:
            salary = (data[2].text)[1:]
            salary = int(salary.replace(',',''))
        except IndexError:
            continue
        for index, value in enumerate(player_stats):
            if value[0].lower() == name.lower():
                player_stats[index].append(salary)

# GETTING CURRENT ESTIMATED MARKET VALUE

'''url = 'https://www.footballtransfers.com/en/teams/uk/man-utd'
response = requests.get(url)
with open ('Player-Market-Value', 'wb') as p:
    p.write(response.content)
'''
with open('Player-Market-Value', 'rb') as pd:
    soup = BeautifulSoup(pd.read(), 'html.parser')

tbody = soup.find('table')

rows = soup.find_all('tr')

for row in rows:
    try:
        name = row.a.text
        worth = (row.find('span', class_ = 'player-tag').text)[1:-1]
        worth = round(float(worth) * 0.88, 2)
        
        for index, value in enumerate(player_stats):
            if len(value) == 35:
                if value[0].lower() == name.lower():
            
                    player_stats[index].append(worth)
    except AttributeError:
        continue



  
  
# field names 
fields = ['name', 'nationality', 'position', 'age', 'matches_played', 'starts', 'minutes', 'goals',
'assists', 'y_card', 'r_card', 'pro_carries', 'pro_passes', 'goals_conceeded', 'shots_on_target_against', 
'saves', 'clean_sheets', 'shots', 'shots_on_target', 'passes_com', 'passes_com_s', 'passes_com_m',
'passes_com_l', 'key_passes', 'passes_into_third', 'crosses_into_pen', 'touches', 't_def_pen', 't_def_third', 
't_mid_third', 't_att_third', 't_att_pen', 'sucessful_takeons', 'aerial_duels_won','salary', 'estimated_market_value'] 
    
# data rows of csv file 

  
with open('Player.csv', 'w') as p:
      
    # using csv.writer method from CSV package
    write = csv.writer(p)
      
    write.writerow(fields)
    write.writerows(player_stats)
    






