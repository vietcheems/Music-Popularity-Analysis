import pprint
import csv
from browsermobproxy import Server
from selenium import webdriver
import os
import json
import time
import pandas as pd
from view_extractor import extract_info_from_har




#mở 1 proxy mới
def start_proxy():
    chrome_options = webdriver.ChromeOptions()
     #cái này thì dẫn directory của browsermob-proxy.bat
    server = Server("path/to/browsermob-proxy.bat", options={'port': 8090})
    server.start()
    proxy = server.create_proxy()

    chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--headless')



    #cái này ông phải tải chrome webdriver, xong thêm path của cái đấy ở dưới
    path = "path/to/chromedriver"
    driver = webdriver.Chrome(path, options=chrome_options)
    return driver,server,proxy


def get_har(sucess_file, failed_file, df, i):
    id = df['album_id'][i]
    df= df.set_index('album_id')
    album_name = df['album'][i]
    file_name = album_name + ".har"
    url = "https://open.spotify.com/album/" + id

    driver, server, proxy = start_proxy()

    driver.get(url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    har_options = {'captureContent': True}
    proxy.new_har(file_name, options=har_options)
    #time.sleep(15)
    file_name = ''.join(char for char in file_name if ( char.isalnum() or char == " " or char == "."))
    #driver.set_page_load_timeout(60)

    found = False
    currentTime = time.time()
    startTime = time.time()

    while (currentTime - startTime <= 8) and (found == False):

        if isinstance(extract_info_from_har(proxy.har), pd.DataFrame):
            found = True
            # df = extract_info_from_har("HAR folder/" + file_name)
            df = extract_info_from_har(proxy.har)
            df['album_index'] = i
            df['album_id'] = id
            df['album_name'] = album_name
            df = df[['song_id', 'song_name', 'playcount', 'album_index', 'album_id', 'album_name']]
            df.to_csv(sucess_file, mode='a', header=False, index=False)
            server.stop()
            driver.quit()
            currentTime = time.time()
            print(currentTime - startTime)
            exit
        else:
            pass

        currentTime = time.time()
        time.sleep(1)

    if (found == False):
        print("failed")
        currentTime = time.time()
        #print(currentTime - startTime)
        row = [i, id, album_name]
        with open(failed_file, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        server.stop()
        driver.quit()



    #with open("HAR folder/" + file_name, 'w') as har_file:
        #json.dump(proxy.har, har_file)
    """try:
        df = extract_info_from_har("HAR folder/" + file_name)
        df['album_index'] = i
        df['album_id'] = id
        df['album_name'] = album_name
        df = df[['song_id', 'song_name','playcount', 'album_index', 'album_id', 'album_name']]
        df.to_csv(sucess_file, mode='a', header=False, index=False)
        server.stop()
        driver.quit()
    except:
        row = [i,id, album_name]
        with open(failed_file, 'a', newline= "") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        server.stop()
        driver.quit()"""


if __name__ == '__main__':
    df = pd.read_csv("spotify-playlist.csv", sep='\t')
    data = [ df['album_id'], df['album']]
    headers = ['album_id', 'album']
    df = pd.concat(data, axis = 1, keys = headers)
    df = df.drop_duplicates()
    df.reset_index(drop = True, inplace=True)
    headerSong = ['album_index','id', 'name', 'playcount', 'album_id', 'album_name']
    headerAlbum = ['album_index','album_id', 'album_name']


    #ông chỉnh index ở đây nhé
    for i in range(2000,len(df['album_id'])):
        try:
            try:
                get_har("spotify_songs.csv", "failed_album.csv", df, i)
            except:
                with open('failed_album.csv', 'a', newline="") as f:
                    row = [i, df['album_id'][i], df['album'][i]]
                    writer = csv.writer(f)
                    writer.writerow(row)
        except:
            print('Failed to fill information at index ', i)
