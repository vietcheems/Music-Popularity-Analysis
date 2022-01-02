import csv
from browsermobproxy import Server
from selenium import webdriver
import os
import time
import pandas as pd
from datetime import datetime
import json

label_query_url = "https://api-partner.spotify.com/pathfinder/v1/query?operationName=getAlbumMetadata&variables"
track_query_url = "https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryAlbumTracks&variables"
read_album_path = "./Scrape/Spotify/spotify-playlist.csv"
headerSong = ['id', 'name',
              'playcount', 'album_index', 'album_id', 'album_name']
headerAlbum = ['album_index', 'album_id', 'album_name']


def get_failed_ablum(failed_path_before, failed_path_after, success_path, try_attempt=3):
    df = pd.read_csv(read_album_path, sep='\t')
    data = [df['album_id'], df['album']]
    headers = ['album_id', 'album']
    df = pd.concat(data, axis=1, keys=headers)
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)

    failed_df = pd.read_csv(failed_path_before)

    # ông chỉnh index ở đây nhé
    for i in failed_df['album_index']:
        print(datetime.now().time())
        try:
            try:
                get_har(success_path, failed_path_after, df, i, try_attempt)
            except:
                print("Failed at {}".format(i))
                with open(failed_path_after, 'a', newline="") as f:
                    row = [i, df['album_id'][i], df['album'][i]]
                    writer = csv.writer(f)
                    writer.writerow(row)
        except:
            print('Failed to fill information at index ', i)


# mở 1 proxy mới
def start_proxy():
    chrome_options = webdriver.ChromeOptions()
    # cái này thì dẫn directory của browsermob-proxy.bat
    server = Server(
        "/home/viet/OneDrive/Studying Materials/Introduction to Data Science/EDA Project/browsermob-proxy-2.1.4-bin/browsermob-proxy-2.1.4/bin/browsermob-proxy", options={'port': 8090})
    server.start()
    proxy = server.create_proxy()

    chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument('--headless')

    # cái này ông phải tải chrome webdriver, xong thêm path của cái đấy ở dưới
    path = "/home/viet/OneDrive/Studying Materials/Introduction to Data Science/EDA Project/chromedriver_linux64/chromedriver"
    driver = webdriver.Chrome(path, options=chrome_options)
    return driver, server, proxy


def get_har(folder_path, failed_file, df, i, try_attempt):
    print('scraping album {}'.format(i))
    id = df['album_id'][i]
    df = df.set_index('album_id')
    album_name = df['album'][i]
    file_name = album_name + ".har"
    url = "https://open.spotify.com/album/" + id

    def loop(file_name):
        driver, server, proxy = start_proxy()
        print("chrome started")

        driver.get(url)
        print("done loading page")
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        print("done scrolling")

        har_options = {'captureContent': True}
        proxy.new_har(file_name, options=har_options)
        # time.sleep(15)
        file_name = ''.join(char for char in file_name if (
            char.isalnum() or char == " " or char == "."))
        # driver.set_page_load_timeout(60)

        found = False
        currentTime = time.time()
        startTime = time.time()

        while (currentTime - startTime <= 3) and (found == False):
            print("waiting")
            time.sleep(1)
            if isinstance(extract_info_from_har(proxy.har), pd.DataFrame):
                print("-------har file found-------")
                found = True
                har_path = os.path.join(folder_path, str(i) + ".har")
                with open(har_path, "w") as f:
                    json.dump(proxy.har, f)
                    print("-------har file written successfully--------")
                currentTime = time.time()
                print(
                    "-------time taken: {}s---------".format(round(currentTime - startTime)))
                break

            currentTime = time.time()

        server.stop()
        driver.quit()
        return found
    found = loop(file_name)
    for j in range(try_attempt):
        if (found == False):
            print("Cant find the response with viewcount, trying again")
            found = loop(file_name)
            currentTime = time.time()
            #print(currentTime - startTime)
        else:
            return
    print("failed after 3 tries")
    row = [i, id, album_name]
    with open(failed_file, 'a', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def first_iteration(start_index, end_index, folder_path, failed_1_path, try_attempt=3):
    df = pd.read_csv(read_album_path, sep='\t')
    data = [df['album_id'], df['album']]
    headers = ['album_id', 'album']
    df = pd.concat(data, axis=1, keys=headers)
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)

    # ông chỉnh index ở đây nhé
    for i in range(start_index, end_index):
        print(datetime.now().time())
        try:
            try:
                get_har(folder_path,
                        failed_1_path, df, i, try_attempt)
            except:
                print("Failed at {}".format(i))
                with open(failed_1_path, 'a', newline="") as f:
                    row = [i, df['album_id'][i], df['album'][i]]
                    writer = csv.writer(f)
                    writer.writerow(row)
        except:
            print('Failed to fill information at index ', i)


def create_csv(path, column_name):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(column_name)
            print("{} created".format(path))
    else:
        print("{} already exists".format(path))


def extract_info_from_har(har):
    '''
    Extract songs' id, name and playcount from string
    Input: har string
    Output: dataframe containing id, name and playcount of each song in the album
    '''

    # read har file
    # with open(har_file) as f:
    #har_file = json.loads(f.read())

    # get entry requesting for songs info
    try:
        entry_with_song_info = []
        for entry in har['log']['entries']:
            if track_query_url in entry['request']['url'] and entry['request']['method'] == "GET":
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
            important_info['song_id'].append(
                song['track']['uri'].split(":")[-1])
            important_info['song_name'].append(song['track']['name'])
            important_info['playcount'].append(song['track']['playcount'])

        # convert into dataframe to concatenate later
        df = pd.DataFrame.from_dict(important_info)
        return df
    except:
        return None


def extract_info_from_har_file(har_file, mode='playcount'):
    '''
    Extract info from har file
    Input: 
        har file path
        mode:
            "playcount": songs' id, name, and playcount
            "label": album id, record label
            "copyright": album id, copyright info
    Output: dataframe containing id, name and playcount of each song in the album
    '''

    # read har file
    with open(har_file) as f:
        har_file = json.loads(f.read())

    if mode == "playcount":
        # get entry requesting for songs info
        entry_with_song_info = []
        for entry in har_file['log']['entries']:
            if track_query_url in entry['request']['url'] and entry['request']['method'] == "GET":
                entry_with_song_info.append(entry)
        assert len(entry_with_song_info) == 1
        entry_with_song_info = entry_with_song_info[0]

        # parse response content and  get the actual songs info
        response_content = json.loads(
            entry_with_song_info['response']['content']['text'])
        songs = response_content['data']['album']['tracks']['items']

        # iterate through the songs in the album to get song id, name and playcount and store them in a dictionary
        important_info = {
            'song_id': [],
            'song_name': [],
            'playcount': []
        }
        for song in songs:
            important_info['song_id'].append(
                song['track']['uri'].split(":")[-1])
            important_info['song_name'].append(song['track']['name'])
            important_info['playcount'].append(song['track']['playcount'])

    elif mode == "label":
        # get entry requesting album info
        for entry in har_file['log']['entries']:
            if label_query_url in entry['request']['url'] and entry['request']['method'] == "GET":
                entry_with_label = entry

        # parse response content and get the record label
        response_content = json.loads(
            entry_with_label['response']['content']['text'])
        label = response_content['data']['album']['label']
        album_id = response_content['data']['album']['uri'].split(":")[-1]

        important_info = {
            'album_id': [album_id],
            'label': [label]
        }
    
    elif mode == "copyright":
        for entry in har_file['log']['entries']:
            if label_query_url in entry['request']['url'] and entry['request']['method'] == "GET":
                entry_with_label = entry

        # parse response content and get copyright text
        response_content = json.loads(
            entry_with_label['response']['content']['text'])
        album_id = response_content['data']['album']['uri'].split(":")[-1]
        copyrights = response_content['data']['album']['copyright']['items']


        # put album_id and copyright texts into a dictionary
        important_info = {
            'album_id': [],
            'copyright': []
        }
        for cp in copyrights:
            important_info['album_id'].append(album_id)
            important_info['copyright'].append(cp['text'])

    else:
        raise Exception("Not a valid mode. Available modes are playcount, label, copyright")
    
    # convert into dataframe to concatenate later
    df = pd.DataFrame.from_dict(important_info)
    return df

if __name__ == "__main__":
    print(extract_info_from_har_file("Scrape/Spotify/har-0-199/0.har",mode="bruh"))