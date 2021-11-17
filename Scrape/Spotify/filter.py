import pandas as pd



df_songs = pd.read_csv("spotify_songs.csv", sep = ",")
df_failed_albums = pd.read_csv('failed_album.csv', sep = ",", encoding='cp1252')

df_songs.drop_duplicates(subset=None, keep="first", inplace=True)
df_failed_albums.drop_duplicates(subset=None, keep="first", inplace=True)

success_index = df_songs['album_index']
success_index = [int(index) for index in success_index]
success_index = list(dict.fromkeys(success_index))

failed_index = df_failed_albums['album_index']
failed_index = [int(index) for index in failed_index]

df_failed_albums.drop(df_failed_albums[pd.to_numeric(df_failed_albums['album_index']).isin(success_index)].index, inplace=True)
df_failed_albums = df_failed_albums.drop(df_failed_albums[pd.to_numeric(df_failed_albums['album_index']) > 2399].index)

df_failed_albums.reset_index(drop=True, inplace=True)

df_songs.drop_duplicates(subset=None, keep="first", inplace=True)
df_failed_albums.drop_duplicates(subset=None, keep="first", inplace=True)

df_songs = df_songs.sort_values(by = ['album_index'], ascending = True)
df_failed_albums = df_failed_albums.sort_values(by = ['album_index'], ascending = True)

df_songs.to_csv("spotify_songs.csv", mode='w', header=True, index=False)
df_failed_albums.to_csv("failed_album.csv", mode='w', header=True, index=False)

print(df_songs)
print(df_failed_albums)

print(df_songs['album_index'].nunique())




