import pandas as pd
from tqdm import tqdm


df = pd.read_csv("wiki_genres.csv", sep="\t")
df_split = pd.DataFrame(columns=df.columns)
for index, row in tqdm(df.iterrows()):
	new_row = row.copy()
	if type(new_row["genres"]) == str: # nan check
		genre_list = row["genres"].split(",")
		for genre in genre_list:
			new_row["genres"] = genre
			df_split = df_split.append(new_row, ignore_index=True)
	else:
		df_split = df_split.append(new_row, ignore_index=True)

df_split.to_csv("genre_splitted.csv", index=False)




