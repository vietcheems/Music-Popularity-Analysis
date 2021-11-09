import json
import pandas as pd

info_query_url = "https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryAlbumTracks&variables"

def extract_info_from_har(file_path:str) -> pd.DataFrame:

	#read har file
	with open(file_path) as f:
		har_file = json.loads(f.read())

	#get entry requesting for songs info
	entry_with_song_info = []
	for entry in har_file['log']['entries']:
		if info_query_url in entry['request']['url']:
			entry_with_song_info.append(entry)
	assert len(entry_with_song_info) == 1
	entry_with_song_info = entry_with_song_info[0]
	
	#parse response content
	response_content = json.loads(entry_with_song_info['response']['content']['text'])
	
	#get the actual songs info
	songs = response_content['data']['album']['tracks']['items']

	#iterate through the songs in the album to get song id, name and playcount and store them in a dictionary
	important_info = {
		'id':[], 
		'name':[], 
		'playcount':[]
	}
	for song in songs:
		important_info['id'].append(song['track']['uri'].split(":")[-1])
		important_info['name'].append(song['track']['name'])
		important_info['playcount'].append(song['track']['playcount'])

	#convert into dataframe to concatenate later
	df = pd.DataFrame.from_dict(important_info)

	return df