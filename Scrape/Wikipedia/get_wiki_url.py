import csv
import pprint

import wikipedia
import pandas as pd
df = pd.read_csv("C:/Users/Dung/PycharmProjects/Music-Popularity-Analysis/Scrape/Spotify/spotify-playlist.csv", sep = "\t")
data = [df['track_id'], df['track'], df['artist']]
headers = ['track_id','track', 'artist']
df = pd.concat(data, axis=1, keys=headers)
row = ['track_id', 'track', 'url']
#with open('wiki links.csv', mode= "w", newline='') as f:
    #writer = csv.writer(f)
    #writer.writerow(row)
for i in range(4363,len(df['track'])):
    try:
        name = df['track'][i]
        name = name.lower()
        if '(feat' in name:
            index = name.find('(feat')
            name = name[:index]
            name = name.strip()
        if '(with' in name:
            index = name.find('(with')
            name = name[:index]
            name = name.strip()
        if '- from' in name:
            index = name.find('- from')
            name = name[:index]
            name = name.strip()
        if '(from' in name:
            index = name.find('(from')
            name = name[:index]
            name = name.strip()
        if '- remastered' in name:
            index = name.find('- remastered')
            name = name[:index]
            name = name.strip()
        if "- radio edit" in name:
            index = name.find('- radio edit')
            name = name[:index]
            name = name.strip()
        if "- single version" in name:
            index = name.find('- single version')
            name = name[:index]
            name = name.strip()


        name = name.replace('(', '')
        name = name.replace(')', '')
        name = name.replace('-', '')
        print(name)

        results = wikipedia.search(name + " " + df['artist'][i] + ' song')
        #print(result)
        if len(results) > 0:
            page = wikipedia.page(results[0], auto_suggest=False)
            print(page.url)
            row = [df['track_id'][i], df['track'][i], df['artist'][i],page.url]
            print(row)
            with open('wiki_links.csv', mode="a", newline='') as f:
                writer = csv.writer(f, delimiter = '\t')
                writer.writerow(row)
        else:
            row = [df['track_id'][i],df['track'][i], df['artist'][i], ""]
            print(row)
            with open('wiki_links.csv', mode="a", newline='') as f:
                writer = csv.writer(f, delimiter = '\t')
                writer.writerow(row)
    except:
        row = [df['track_id'][i], df['track'][i], df['artist'][i], ""]
        print(row)
        with open('wiki_links.csv', mode="a", newline='') as f:
           writer = csv.writer(f, delimiter = '\t')
           writer.writerow(row)


    #rl = page.url
    #html = page.html()
    #pprint.pprint(html)
    #print(url)
    #page = wikipedia.page(result[0])
    #print(page)