import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import os
import sys
jac = 'Juan Antonio Corbalán'
season = int(sys.argv[1])
first_day = int(sys.argv[2])
current_day = int(sys.argv[3])
links = []
for x in range(first_day, current_day+1):
    url = 'http://ducksattack.com/DASL/boxes/day{}.htm'.format(x)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    links.extend(['http://ducksattack.com/DASL/boxes/' + x['href'] for x in soup.find_all('a') if x.text == 'Box Score'])

def get_game(url):
    dfs = pd.read_html(url)
    team1 = dfs[1].columns[0]
    team2 = dfs[2].columns[0]
    df1 = dfs[1].rename(columns={team1:'Player'}).drop(columns={dfs[1].columns[-1]})[:-2]
    df2 = dfs[2].rename(columns={team2:'Player'}).drop(columns={dfs[2].columns[-1]})[:-2]
    df1['team'] = [team1]*len(df1)
    df1['opp'] = [team2]*len(df1)
    df1['day'] = url.split('/')[-1].split('-')[0]
    df2['team'] = [team2]*len(df2)
    df2['opp'] = [team1]*len(df2)
    df2['day'] = url.split('/')[-1].split('-')[0]
    return pd.concat((df1,df2))

if f"{season}season.csv" in os.listdir():
    season = pd.read_csv(f"{season}season.csv")
else:     
    season = pd.DataFrame()
i = 0
print(len(season))
for index, link in enumerate(links):
    time.sleep(.1)
    temp = get_game(link)
    temp['game_id'] = index
    season = pd.concat((season, temp))

season['day'] = pd.to_numeric(season['day'], errors='coerce')
season = season.loc[~season.day.isna()]

season[season.columns[2:10]] = season[season.columns[2:10]].apply(pd.to_numeric, errors='coerce') 
season['TSA'] = season['FGA'] + .44*season['FTA']
season['TS'] = season['PTS']/(2*season['TSA'])
print(season.info())
if 'Usage' not in season.columns:
    season['Usage'] = np.nan
for x in season.loc[season.Usage.isna()].index:
    this_game = season.iloc[x]
    season.loc[x,'Usage'] = (100*(season.loc[x,'FGA'] + .44*season.loc[x,'FTA'] + season.loc[x,'TO'])*(this_game['MIN'].sum()/5))/((this_game['FGA'].sum() + .44*this_game['FTA'].sum() + this_game['TO'].sum())*season.loc[x,'MIN'])
    
for x in season.columns[3:16]:
    season['{}/36'.format(x)] = (season[x]/season['MIN'])*36

season.to_csv('96season.csv', index=False)

