import csv

import numpy as np
import pandas
import pandas as pd
from bs4 import BeautifulSoup
import requests
#blinding lights

#source = requests.get("https://en.wikipedia.org/wiki/Blinding_Lights").text


#print(citations)

def get_genres(url):
    if isinstance(url,float):
        return None
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    infobox = soup.find('table', class_="infobox vevent")
    if infobox != None:
        hlist = infobox.find('td', class_='infobox-data category hlist')
        if hlist != None:
            genre_rows = hlist.find_all('a')
            genres = []
            for row in genre_rows:
                genres.append(row.text.strip().lower())
            genres = [genre for genre in genres if  ('[' not in genre)]
            return ",".join(genres)
        else:
            return None

    else:
        infobox = soup.find('table', class_ = 'infobox vevent haudio')
        if infobox != None:
            hlist = infobox.find('td', class_='infobox-data category hlist')
            if hlist != None:
                genre_rows = hlist.find_all('a')
                genres = []
                for row in genre_rows:
                    genres.append(row.text.strip().lower())
                for element in genres:
                    if '[' in element:
                        genres.remove(element)
                genres = [genre for genre in genres if ('[' not in genre)]
                return ",".join(genres)
            else:
                return None
        else:
            return None

if __name__ == "__main__":
    df = pd.read_csv('wiki.csv', sep='\t', encoding='cp1252')

    for i in range(len(df['url'])):
        track_id = df['track_id'][i]
        track = df['track'][i]
        artist = df['artist'][i]
        url = df['url'][i]
        genres = get_genres(url)
        if genres != None:
            row = [track_id,track,artist,url,genres]
            print(row)
            with open('wiki_genres.csv',mode = 'a',newline='',encoding='cp1252') as f:
                writer = csv.writer(f, delimiter = '\t')
                writer.writerow(row)
        else:
            row = [track_id, track, artist, url,""]
            print(row)
            with open('wiki_genres.csv',mode = 'a',newline='',encoding='cp1252') as f:
                writer = csv.writer(f, delimiter = '\t')
                writer.writerow(row)






    #df.to_csv('log.csv', mode='a', index=False, header=False)






