#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


# In[2]:


url1="https://fbref.com/en/comps/12/2020-2021/stats/2020-2021-La-Liga-Stats"


# In[3]:


data=requests.get(url1)
data.text


# In[4]:


from bs4 import BeautifulSoup
soup=BeautifulSoup(data.text)


# In[5]:


table_standings=soup.select('table.stats_table')[0]


# In[6]:


table_standings


# In[7]:


links = table_standings.find_all('a')
links = [l.get("href") for l in links]


# In[8]:


links = [l for l in links if '/squads/' in l]
print(links)


# In[9]:


team_urls = [f"https://fbref.com{l}" for l in links]
team_urls#these are absolute links


# In[10]:


team_url=team_urls[0]


# In[11]:


data=requests.get(team_url)
data.text


# In[12]:


import pandas as pd
matches = pd.read_html(data.text, match="Scores & Fixtures",header=None)
matches[0]


# In[13]:


soup = BeautifulSoup(data.text)
links = soup.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if l and 'all_comps/shooting/' in l]
links


# In[14]:


data = requests.get(f"https://fbref.com{links[0]}")
shooting = pd.read_html(data.text, match="Shooting")[0]
shooting.head()


# In[15]:


shooting.columns=shooting.columns.droplevel()
shooting.columns


# In[16]:


shooting.head()


# In[17]:


matches[0].shape


# In[18]:


team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
team_data.head()


# In[19]:


team_data.shape


# In[20]:


years = list(range(2021, 2020, -1))
print(years)
all_matches = []


# In[21]:


standings_url = "https://fbref.com/en/comps/12/2022-2023/stats/2022-2023-La-Liga-Stats"


# In[23]:


import time
for year in years:
    data = requests.get(standings_url)
    soup = BeautifulSoup(data.text)
    standings_table = soup.select('table.stats_table')[0]

    links = [l.get("href") for l in standings_table.find_all('a')]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]
    
    previous_season = soup.select("a.prev")[0].get("href")
    standings_url = f"https://fbref.com{previous_season}"
    
    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = requests.get(team_url)
        matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
        soup = BeautifulSoup(data.text)
        links = [l.get("href") for l in soup.find_all('a')]
        links = [l for l in links if l and 'all_comps/shooting/' in l]
        data = requests.get(f"https://fbref.com{links[0]}")
        shooting = pd.read_html(data.text, match="Shooting")[0]
        shooting.columns = shooting.columns.droplevel()
        try:
            team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
        except ValueError:
            continue
        team_data = team_data[team_data["Comp"] == "La Liga"]
        
        team_data["Season"] = year
        team_data["Team"] = team_name
        all_matches.append(team_data)
        time.sleep(1)


# In[24]:


len(all_matches)


# In[25]:


match_df = pd.concat(all_matches)


# In[26]:


match_df.columns = [c.lower() for c in match_df.columns]


# In[27]:


match_df


# In[37]:


years1 = list(range(2022, 2021, -1))
print(years1)
all_matches1 = []


# In[38]:


for year in years1:
    data = requests.get(standings_url)
    soup = BeautifulSoup(data.text)
    standings_table = soup.select('table.stats_table')[0]

    links = [l.get("href") for l in standings_table.find_all('a')]
    links = [l for l in links if '/squads/' in l]
    team_urls = [f"https://fbref.com{l}" for l in links]
    
    previous_season = soup.select("a.prev")[0].get("href")
    standings_url = f"https://fbref.com{previous_season}"
    
    for team_url in team_urls:
        team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
        data = requests.get(team_url)
        matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
        soup = BeautifulSoup(data.text)
        links = [l.get("href") for l in soup.find_all('a')]
        links = [l for l in links if l and 'all_comps/shooting/' in l]
        data = requests.get(f"https://fbref.com{links[0]}")
        shooting = pd.read_html(data.text, match="Shooting")[0]
        shooting.columns = shooting.columns.droplevel()
        try:
            team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
        except ValueError:
            continue
        team_data = team_data[team_data["Comp"] == "La Liga"]
        
        team_data["Season"] = year
        team_data["Team"] = team_name
        all_matches.append(team_data)
        time.sleep(1)


# In[39]:


match_df1 = pd.concat(all_matches)


# In[40]:


match_df1.columns = [c.lower() for c in match_df.columns]
match_df1


# In[41]:


len(all_matches)


# In[43]:


matches=pd.concat([match_df, match_df1])
matches


# In[44]:


matches.to_csv("matches.csv")


# In[45]:


matches.columns


# In[ ]:




