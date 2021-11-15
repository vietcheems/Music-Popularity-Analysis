import csv
from browsermobproxy import Server
from selenium import webdriver
import os
import time
import pandas as pd
from view_extractor import extract_info_from_har
from datetime import datetime


read_album_path = "./Scrape/Spotify/spotify-playlist.csv"
headerSong = ['id', 'name',
                'playcount', 'album_index', 'album_id', 'album_name']
headerAlbum = ['album_index', 'album_id', 'album_name']


def get_failed_ablum(failed_path_before, failed_path_after, success_path):
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
        print("current album id: {}".format(i))
        try:
            try:
                get_har(success_path, failed_path_after, df, i)
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


def get_har(sucess_file, failed_file, df, i):
    print('scrape album {}'.format(i))
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

            if isinstance(extract_info_from_har(proxy.har), pd.DataFrame):
                found = True
                # df = extract_info_from_har("HAR folder/" + file_name)
                df = extract_info_from_har(proxy.har)
                df['album_index'] = i
                df['album_id'] = id
                df['album_name'] = album_name
                df = df[['song_id', 'song_name', 'playcount',
                         'album_index', 'album_id', 'album_name']]
                print('success!')
                print(df)
                df.to_csv(sucess_file, mode='a', header=False, index=False)
                server.stop()
                driver.quit()
                currentTime = time.time()
                print(currentTime - startTime)
                exit
            else:
                pass
            print("wait")
            currentTime = time.time()
            time.sleep(1)
        server.stop()
        driver.quit()
        return found
    found = loop(file_name)
    for j in range(3):
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

    # with open("HAR folder/" + file_name, 'w') as har_file:
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


def first_iteration(start_index, end_index, success_path, failed_1_path):
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
                get_har(success_path,
                        failed_1_path, df, i)
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