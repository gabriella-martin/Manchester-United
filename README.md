<h1 align="center">Manchester United in the Premier League</h1>

*The best way to understand the app is by visiting it [here](https://gabriella-martin-manchester-united-general-hmrzii.streamlit.app/), please first read the disclaimer below*

**Technologies Used**: Python, Git, AWS S3, AWS RDS,  PostgreSQL, Psycopg2, Pandas, Streamlit, Plotly, Requests & BeautifulSoup
<div align="center">
	<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" height="90" width="80"   />
	 <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" height="90" width="80"  />
	<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="html5" width="80" height="90"/>
	<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original-wordmark.svg"  width="80" height="90"/>
    <img src="https://google.github.io/sqlcommenter/images/psycopg2-logo.png"height="90" width="100" /> 
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" height="90" width="80"   />
    <img src="https://avatars.githubusercontent.com/u/45109972?s=280&v=4" height="90" width="80"   />
    <img src="https://mobilitydb.com/images/plotly.png" height="90" width="80" /> 
    	<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Requests_Python_Logo.png/374px-Requests_Python_Logo.png" height="90" width="60"   />
	<img src="https://www.jeveuxetredatascientist.fr/wp-content/uploads/2022/06/BeautifulSoup-1080x428.jpg" height="60" width="130"  />

  </div>
          
<br>

***Disclaimer**: I use Streamlit Community Cloud (free) to host this project, as this is a free hosting service, the speed can be slightly slow, but streamlit was used to greatly simplify the front-end coding without sacrificing on aesthetics and allow me to focus on the back-end core of this project*

##### Introduction & Quick Overview

The main goal of this app is to analyse the performance of  Manchester United throughout this Premier League season, while also gaining insights into the league as a whole. To retrieve the HTML data I used the Python library requests and to parse the HTML I used BeautifulSoup. The data is then processed and cleaned with Python before it is loaded onto AWS PostgresSQL RDS and backed up in a S3 bucket. Storing with the AWS cloud allows me to have flexiblity to expand the database as there is a wealth of premier league data I wish to leverage in the next stages of this app. 

Once loaded in to the database I query the data with SQL in my Python scripts with the Pscopg2 adapter and calculate some core metrics for each United player and the team as a whole. As the entirety of player premier league data is scraped and stored in this database, I can compare the United data to the rest of the Premier League and create interactive visualisations with Streamlit & Plotly. 

I store the data in an AWS PostgreSQL RDS and store a copy of the data in an AWS S3 bucket. Storing in the cloud allows me to have flexiblity to expand the database as there is an abundance of premier league data that I can leverage in the future. Psycopg2 is used as a PostgreSQL adapter for Python

The app is split up into five main sections;

- Scraping the data 
- Storing the data
- Connecting to the data
- Computing statistics
- Visualising the data

#### 1) Scraping

*The link to all the club datasource links can be found [here](https://github.com/gabriella-martin/Manchester-United/blob/main/data/club_data_links.csv), the code for grabbing the html can be found [here](https://github.com/gabriella-martin/Manchester-United/blob/main/pipelines/html_grabber.py) and the code for parsing the HTML to retrieve the data and cleaning/processing the data can be found [here](https://github.com/gabriella-martin/Manchester-United/blob/main/pipelines/batch_pipeline.py). As the web scraper has to be run after each PL matchweek to ensure up-to-date data, I wrote [unittests](https://github.com/gabriella-martin/Manchester-United/tree/main/tests) for the parser to ensure the whole process runs smoothly.*

Initially, I began by identifying the data that I wanted to extract and subsequently determined the appropriate source from which to retrieve said data.

**Individual Player Data**

 I wanted player specific data for each player in the EPL this season. For each team in the EPL, comprehensive player stats can be found at [football reference](https://fbref.com/en/squads/19538871/Manchester-United-Stats). There is a wealth of stats from this site but I chose about 50 core statistics to scrape for each player.

By including financial data such as player salaries and estimated market values, it is also possible to calculate the value for money that each player provides to their team. This analysis can help teams identify players who may be over or underpaid relative to their on-field performance, providing valuable insights for comparison across the league. I scraped the salary data from [here](https://salarysport.com/football/premier-league/manchester-united-f.c./) and the estimated market value data from [here](https://www.footballtransfers.com/en/teams/uk/man-utd). Next, I wanted to grab the shirt number of each player and used the official premier league [website](https://www.premierleague.com/clubs/12/Manchester-United/squad). This process was automated across all of the 20 clubs and collated into one master player data CSV, which you can view [here](https://github.com/gabriella-martin/Manchester-United/blob/main/data/players.csv).

**Fixture Data**

I knew I wanted to get past & present fixture data including the teams playing, the goals scored by each team. [FBref](https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures) have a single table  all premier league fixtures, past and upcoming, and their results which they allow easy download of, this was added to another CSV ready for storing. The database for this particular section can be found [here](hhttps://github.com/gabriella-martin/Manchester-United/blob/main/data/fixtures.csv).

**Standings Data**

Rather than creating another scraper to get the table data, with all of this season's fixture data I had all the data I needed to code the logic behind the table and could instead write some Python to get up to date standings.

#### 2) Storing

With my two databases, player data and fixture data, I first backed up the databases in a AWS S3 bucket using this [script](https://github.com/gabriella-martin/Manchester-United/blob/main/pipelines/aws_pipeline.py). I then stored the database with AWS PostgreSQL RDS. Using SQL I then began to explore my data by writing queries, here is an example of finding the top goalscoring defenders in the premier league

![alt text](resources/examplequery.png)

#### 2) Connecting

So with the database all set up, I connected the database to my python script using psycopg2, the following code sets up the connection and executes a simple query:

```python

import psycopg2

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'database-1.c0lrvxe9frij.eu-west-2.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = st.secrets['DATABASE_PASSWORD'] 
PORT = 5432
DATABASE = 'football'

with psycopg2.connect(host=ENDPOINT, user=USER, password=PASSWORD, dbname=DATABASE, 
port=PORT) as conn:
    with conn.cursor() as cur:
        cur.execute('''SELECT name FROM players WHERE club = 'Manchester United' LIMIT 5;''')
        results = cur.fetchall()
        cur.close()
```

#### 3) Computing 

**Player Data**:

I wanted to separate players by position so I decided what attributes would be insightful for each position and came to the following categories:

- **Goalkeepers**: General & Saving

- **Defenders:** General, Threat-Handling & Defender Upfield Stats
  
- **Midfielders:** General, Threat-Handling & Midfielder Upfield Stats

- **Forwards:** General, Game Involvement & Goal Involvement

In order for a player to be showcased by my web-application I set the requirement that they must have played over 90 minutes in total (this does not have to be consecutive) as this was the best way to ensure that the per 90 stats would be an accurate measure. For example if a player has only played for 10 minutes in total but managed to score a goal in this time, their goals per 90 would be 9 goals; clearly an innacurate measure. 

Given that player data was aggregated across all Premier League matches and players have played for varying total durations, it is imperative to normalize the raw data on a per 90-minute basis. This adjustment is necessary to facilitate meaningful comparisons between players who have played disparate amounts, thus ensuring the accuracy and reliability of the analysis.

With these categories of data in mind, I coded a data pipeline that would connect to my AWS PostgreSQL RDS and query each metric with SQL. The full code for retrieving and formatting these statistics can be found [here](https://github.com/gabriella-martin/Manchester-United/blob/main/pipelines/player_stats_pipeline.py). Each category of data has its own retrieving method and sometimes a formatting method, here is an example of the methods for the category 'threat handling' within my PlayerStatFormatting class. The use of try/except is to handle any NULL datapoints or any situations where python would attempt to divide by 0. 

```python
    def get_threat_handling_stats(self):
        threat_stats = ['shot_blocks', 'blocks', 'interceptions', 'clearances', 
        'total_tackles', 'successful_tackles','sucessful_takeons', 'fouls_committed' ]
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

```
**Average Player Data**

To compare Manchester United players against the average statistics of players in the same position from a opposition club, I developed a similar class to the player statistics class. However, instead of using queries for individual player statistics, I adjusted them to retrieve average statistics for players in the desired position from the relevant club. Rather than looking like:

```python
q = f"""SELECT {value} FROM players WHERE name = '{self.player}';"""
```
they instead looked like:
```python
q = f"""SELECT AVG({value}) FROM players WHERE club = '{self.club}' and position = '{self.position}';"""
```
The full code for calculating club position specific averages can be viewed [here](https://github.com/gabriella-martin/Manchester-United/blob/main/pipelines/club_average_pipeline.py).

**Club General Data**

With the fixture data, I coded the simple logic behind the PL table, assigning three points for a win, one for a draw, and zero for a loss. I created a class that would analyse the fixture data for each club. This class would return a Pandas dataframe for each club, here is a snippet of the code:
```python
    def create_club_dataframe(self):
        matches_played, point_list, goals_scored, goals_conceeded, opponents, net_goals = self.get_matches_played()
        df = pd.DataFrame({'Matches Played': matches_played ,'Points':point_list, 'Goals Scored': goals_scored, 
        'Goals Conceeded': goals_conceeded, 'Net Goals': net_goals, 'Opponents':opponents})
        df['Points Sum'] = df['Points'].cumsum()
        df['Points Rolling Average'] =df['Points'].expanding(1).mean()
        df['Goals Scored CMA'] =df['Goals Scored'].expanding(1).mean()
        df['Goals Conceeded CMA'] =df['Goals Conceeded'].expanding(1).mean()
        df['Net Goals CMA'] =df['Net Goals'].expanding(1).mean()
        return df
```
Intuitively, by looking at the 'Points Sum' column for each of the club dataframes, we can easily order the clubs by points to get the current table standings. The full code for these club-wide stats can be viewed [here](https://github.com/gabriella-martin/Manchester-United/blob/main/pipelines/club_general_pipeline.py).

### 4) Visualising

**Position Pages**

*The full code for the front-end of each page can be viewed [here](https://github.com/gabriella-martin/Manchester-United/tree/main/pages)*

With a pipeline of statistical retrival established, then came coding a visually appealing player card, this was coded using the Streamlit framework. Here is an example for what a forward stat card looks like, the full code for the outline of the stat cards can be viewed [here](https://github.com/gabriella-martin/Manchester-United/blob/main/stat_cards.py). Here is an example forward stat card:

<center> <img src = "resources/exampleforward.png" > </center>

As this project is focused on Manchester United, I downloaded all the player images from their website, for the rest of the premier league teams, a blacked out version is used for simplicity. Each position (GK, DF, MF & FW) has its own page to ensure like-for-like comparisons.

I next began the core aim of this project; comparison. I coded multiple comparison options that would show percentage change comparison against the following choices:

- The other United players with that position
- Average of the United players with that position
- Average of the players in the same position from each opposing club 

Here are some examples of how comparisons look:

<center> <img src = "resources/examplecomparison.png" > </center>

<center> <img src = "resources/examplecomparison2.png" > </center>


**General Page**

*The full code for the front-end of this page can be viewed [here](https://github.com/gabriella-martin/Manchester-United/blob/main/General.py)*

This page enables comparison at the club level and uses the statistics retrived from the general stats script. The user chooses a team to compare against (teams are given in current standing order) and can view graphical visualisations of core statistics like goals conceeded, goals scored, net goals, points per game and cumulative points to get an idea of how United as a whole stack up against the opposition.

Here is an example of one of these graphical comparisons:

<center> <img src = "resources/examplegraph.png" > </center>

**Upcoming Page**

*The full code for the front-end of this page can be viewed [here](https://github.com/gabriella-martin/Manchester-United/blob/main/pages/5_Upcoming.py)*

As part of my Premier League player statistics project, I developed a page that is similar to the general comparison page. However, instead of displaying comparison statistics for the entire PL, this page queries the fixtures database to retrieve information about the next match that Manchester United is due to play. The corresponding stats are then served to the user, enabling a comparison between United and their next opponent. This feature is useful in helping fans and analysts prepare for upcoming matches and can provide valuable insights into potential areas of focus for Manchester United's gameplay. By analyzing the data presented, fans and analysts can gain a better understanding of the strengths and weaknesses of both teams, aiding in more informed predictions and analysis of the match. Here is an example of such:

<center> <img src = "resources/exampleupcoming.png" > </center>
