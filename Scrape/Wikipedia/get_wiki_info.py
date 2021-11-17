import pprint

import wikipedia
import pandas as pd
df = pd.read_csv("C:/Users/Dung/PycharmProjects/Music-Popularity-Analysis/Scrape/Spotify/spotify-playlist.csv", sep = "\t")
data = [df['track'], df['artist']]
headers = ['track', 'artist']
df = pd.concat(data, axis=1, keys=headers)
for i in range(0,1):
    result = wikipedia.search(df['track'][i] + " " + df['artist'][i] + " song")
    page = wikipedia.page(result[0], auto_suggest=False)
    url = page.url
    html = page.html()
    pprint.pprint(html)
    print(url)
    #page = wikipedia.page(result[0])
    #print(page)