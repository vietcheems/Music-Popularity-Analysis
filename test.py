import pprint
import csv
from browsermobproxy import Server
from selenium import webdriver
import os
import json
import time
import pandas as pd

def extract_info_from_har(har_file):
    '''
    Extract songs' id, name and playcount from a har file
    Input: har file path
    Output: dataframe containing id, name and playcount of each song in the album
    '''

    # read har file
    #with open(har_file) as f:
        #har_file = json.loads(f.read())

    # get entry requesting for songs info
    try:
        entry_with_song_info = []
        for entry in har_file['log']['entries']:
            if info_query_url in entry['request']['url'] and entry['request']['method'] == "GET":
                entry_with_song_info.append(entry)
        assert len(entry_with_song_info) == 1
        entry_with_song_info = entry_with_song_info[0]

        # parse response content
        response_content = json.loads(
            entry_with_song_info['response']['content']['text'])

        # get the actual songs info
        songs = response_content['data']['album']['tracks']['items']

        # iterate through the songs in the album to get song id, name and playcount and store them in a dictionary
        important_info = {
            'song_id': [],
            'song_name': [],
            'playcount': []
        }
        for song in songs:
            important_info['song_id'].append(song['track']['uri'].split(":")[-1])
            important_info['song_name'].append(song['track']['name'])
            important_info['playcount'].append(song['track']['playcount'])

        # convert into dataframe to concatenate later
        df = pd.DataFrame.from_dict(important_info)
        return df
    except:
        return None

# cái này thì dẫn directory của browsermob-proxy.bat
server = Server(
    "/home/viet/OneDrive/Studying Materials/Introduction to Data Science/EDA Project/browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy", options={'port': 8090})
server.start()
proxy = server.create_proxy()

profile  = webdriver.FirefoxProfile()
path = "/home/viet/OneDrive/Studying Materials/Introduction to Data Science/EDA Project/geckodriver-v0.30.0-linux64/geckodriver"
driver = webdriver.Firefox(executable_path=path, proxy=proxy, firefox_profile=profile)


driver.get("https://open.spotify.com/album/7oJa8bPFKVbq4c7NswXHw8")
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
proxy.new_har("google", options={'captureContent': True})
time.sleep(10)
print(proxy.har)
print(extract_info_from_har(proxy.har)) # returns a HAR JSON blob
time.sleep(20)
print(extract_info_from_har(proxy.har))
server.stop()
driver.quit()