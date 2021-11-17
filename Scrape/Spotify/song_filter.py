import pandas as pd
df = pd.read_csv("spotify_songs.csv", sep = ",")
df_2400 = pd.read_csv("success_2400.csv",sep = ",")
df_2800 = pd.read_csv("success_2800.csv",sep = ",")
df = df.append(df_2400,ignore_index=True)
df = df.append(df_2800,ignore_index=True)

#df = pd.concat([df,df_2400, df_2800])
df.drop(df[pd.to_numeric(df['playcount']) < 100000000].index, inplace=True)
#df = df.sort_values(by = ['playcount'], ascending = False)
df = df.sort_values(by = ['album_index'], ascending = True)
print(pd.to_numeric(df['album_index']))

print(df['name'].value_counts())

df.to_csv("spotify_songs_filtered.csv", mode='w', header=True, index=False)


