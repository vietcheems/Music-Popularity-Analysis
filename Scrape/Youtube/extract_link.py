import pandas as pd
import os
import json

folder = "Scrape/youtube/2_round/response"
df = pd.DataFrame()

for file_name in os.listdir(folder):
	if file_name == "failed_log":
		continue
	file_path = os.path.join(folder, file_name)
	with open(file_path, 'r') as f:
		d = json.loads(f.read())
	song = d['items'][0]
	row = {key:value for (key,value) in song['snippet'].items() if key in ['publishedAt', 'channelId', 'title', 'channelTitle']}
	spotify_index = file_name.split(".")[0]
	row['spotify_index'] = spotify_index
	row['video_id'] = song['id']['videoId']
	df = df.append(row, ignore_index=True)

print(df.head())
df.to_csv("Scrape/youtube/2_round/youtube.csv", index=False)