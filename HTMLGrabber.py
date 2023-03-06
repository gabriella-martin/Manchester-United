import csv
import requests 
from bs4 import BeautifulSoup 
from time import sleep
with open('club_data_links.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

data_type = (data[0])

for index, urls in enumerate(data):
    if index == 0:
        continue
    else:
        for index, url in enumerate(urls):
            if index == 0:
                club = url
                continue
            else:
                sleep(1)
                response = requests.get(url)
                with open (f'{club}-{data_type[index]}', 'wb') as p:
                    p.write(response.content)