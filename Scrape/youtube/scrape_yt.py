import requests
import pandas as pd
from string import punctuation
import os
 
current_api_index = 12 # index of the api currently being used
start_index = 1782 # index of the song to start scraping at

api = [
    'AIzaSyDsayLz55WJ4o5Oe7zkA8ul1srKJ-7y1os',
    "AIzaSyC5o8i_16ajtWMnLekeuoQ7kUPClT1lIFk",
    'AIzaSyBfIbxkDF157ZOZHo4wtcvVUOx-hIGMow8',
    'AIzaSyCNLcOR6ndfBk_j84RhbCa5nh22TVnhYcQ',
    'AIzaSyCcKNTMCjC8__Mf1Pp5tqMPI0EoyQQ1HcA',
    'AIzaSyDC4-R7EO6jj-lqMEBa-ouPvEZcip9qcCo',
    'AIzaSyBF1pekwc--yzpnNOT7ngtvAjap5EPunBg',
    'AIzaSyD4QJjuWsxT7Yai22hEUi2GOu_fHauSHKU',
    'AIzaSyBkh1YSZef2EJtJ278Fxd1LkBk5OgbVrqU',
    'AIzaSyDHW3jggCWoln8-7zWAAaG6SkGoWX5FWd0',
    'AIzaSyCn4r0n2u8IX_fmfviXAs_dciJloJTFM3k',
    'AIzaSyAXFX95asW6J6y-GiQnRFWWKQVLJQBB3AA'
]

# get the other keys
key_path = "Scrape/youtube/key"
for file_name in os.listdir(key_path):
	path = os.path.join(key_path, file_name)
	with open(path) as f:
		lines = f.readlines()
		for line in lines:
			api.append(line)

# get all songs
df = pd.read_csv(
	"Scrape/Spotify/spotify-playlist.csv", sep="\t")

# create log file
with open("Scrape/youtube/response/failed_log", "w") as f:
	pass


# iterate through the songs
for index, row in df.iterrows():
	# start scraping at start_index
	if index >= start_index:
		# remove special characters from keyword
		keyword = row["track"] + " " + row["artist"]
		for c in punctuation:
			keyword = keyword.replace(c, "")
		print(keyword)
		done = False
		while not done:
			try:
				# calling the api
				print("----getting the response----")
				r = requests.get(
					"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q={}&type=video&key={}".format(keyword, api[current_api_index]))
				print("----got the response----")
				# 200 => succeeded
				if r.status_code == 200:
					with open("Scrape/youtube/response/{}.json".format(index), 'w') as f:
						f.write(r.text)
					done = True
				# 403 => quota exceeded, try again using the next api in the list
				elif r.status_code == 403:
					print("-----quota exceeded, changing api-----")
					current_api_index += 1
				# failed for some reason, store this in failed_log
				else:
					print(r.status_code)
					with open("Scrape/youtube/response/failed_log", "a") as f:
						f.write("{},{}\n".format(index, keyword))
						f.write(r.status_code + "\n")
						f.write(r.text + "\n")
					print("-----failed at album {}-----".format(index))
					done = True
			except Exception as e:
				print(e)
				print("------trying again------")
		break
