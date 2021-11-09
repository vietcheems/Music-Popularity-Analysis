import pprint
import time

from browsermobproxy import Server
from selenium import webdriver
import os
import json
import time
import pandas as pd
start = time.time()




#mở 1 proxy mới
def start_proxy():
    chrome_options = webdriver.ChromeOptions()
    server = Server("G:/browsermob-proxy/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat", options={'port': 8090})
    server.start()
    proxy = server.create_proxy()

    chrome_options.add_argument("--proxy-server={}".format(proxy.proxy))
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')


    #cái này ông phải tải chrome webdriver, xong thêm path của cái đấy ở dưới
    path = "path/to/webdriver"
    driver = webdriver.Chrome(path, options=chrome_options)
    return driver,server,proxy


def get_har(album_name,album_id,i):

    id = album_id[i]
    name = album_name[i]
    name = name + ".har"
    url = "https://open.spotify.com/album/" + id

    driver, server, proxy = start_proxy()

    driver.get(url)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    har_options = {'captureContent': True}
    proxy.new_har(name, options=har_options)
    time.sleep(10)

    print(type(proxy.har))
    with open("destination/folder" + name, 'w') as har_file:
        json.dump(proxy.har, har_file)
        
    server.stop()
    driver.quit()

if __name__ == '__main__':
    df = pd.read_csv("spotify-playlist.csv", sep='\t')
    album_name = df['album']
    album_id = df["album_id"]

    for i in range(len(album_id)):
        get_har(album_name, album_id, i)

    end = time.time()
    print(end - start)
