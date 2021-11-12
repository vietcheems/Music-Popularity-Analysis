import json
import time

import pandas as pd
import csv
info_query_url = "https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryAlbumTracks&variables"


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


if __name__ == "__main__":
    from apscheduler.schedulers.background import BackgroundScheduler

    sched = BackgroundScheduler()



    def foo():
        print("The seconds")
        time.sleep(5)


    df = pd.read_csv("spotify-playlist.csv", sep='\t')
    print(type(df))
    startTime = time.time()
    endTime = time.time()
    while (endTime - startTime <= 60):
        foo()
        endTime = time.time()



    # seconds can be replaced with minutes, hours, or days
    """

    df = pd.read_csv("spotify-playlist.csv", sep='\t')
    data = [ df['album_id'], df['album']]
    headers = ['album_id', 'album']
    df = pd.concat(data, axis = 1, keys = headers)
    df = df.drop_duplicates()
    df.to_csv('albums',mode = "w", index = False)
    name = df['album'][11] + ".har"
    name = ''.join(char for char in name if ( char.isalnum() or char == " " or char == "."))
    print(name)
    df.reset_index(drop = True, inplace=True)
    print(df)

    print(df.loc[17].values)
    for i in range(len(df['album'])):
        if i in [17,26, 82,93,99,100,112,115,141,151,157,159,167,168, 175,176, 181, 190, 197]:
            with open('fail_index.csv', 'a', newline="") as f:
                print(df['track_id'][i])
                row = [i, df['album_id'][i], df['album'][i]]
                writer = csv.writer(f)
                writer.writerow(row)

    #print(extract_info_from_har('pythonProject/HAR folder/Blinding Lights.har')) """
