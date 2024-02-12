from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

urls = []

url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=326021112'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')  # Use 'html.parser' instead of just 'html'

df_titles = []
df_data = []


titles = soup.find_all('section', {'aria-label': "Prisdetaljer"})
title = titles[0].find_all('span')
df_titles.append(title[0].text.strip())

text = title[1].text.strip()
numbers = ' '.join(re.findall(r'\d+', text))
df_data.append(numbers.replace(' ', ''))

keyinfo = soup.find_all('section', {'aria-labelledby': "keyinfo-heading"})

pattern = r'\d+'

for keyinfo in keyinfo:
    keyinfo_titles = keyinfo.find_all('dt')
    keyinfo_data = keyinfo.find_all('dd')
    for i in range(len(keyinfo_titles)):
        df_titles.append(keyinfo_titles[i].text.strip())
        text = keyinfo_data[i].text.strip()    
        if (re.search(pattern, text)):
            numbers = ' '.join(re.findall(r'\d+', text))
            df_data.append(numbers)
        else: 
            df_data.append(text)

print(df_titles)
print(df_data)
    
df = pd.DataFrame(columns=df_titles)
length = len(df)
df.loc[length] = df_data

print(df)