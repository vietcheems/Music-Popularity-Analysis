import pandas as pd


def merge_view():
    yt = pd.read_csv("Scrape/Youtube/youtube_rescrape_nodup.csv")
    sp_playcount = pd.read_csv("Scrape/Spotify/playcount.csv")
    sp_playcount_sub = sp_playcount[["song_id", "playcount"]]
    sp_feature = pd.read_csv("Scrape/Spotify/spotify-playlist.csv", sep="\t")
    sp_feat_sub = sp_feature.drop(
        columns=["Unnamed: 0", "artist_id", "album_id"])
    sp = sp_feat_sub.join(sp_playcount_sub.set_index("song_id"), on="track_id")
    full = sp.merge(yt, left_index=True, right_on="spotify_index", how="left")
    full_drop = full.drop(columns=["spotify_index", "channelId"])
    full_drop.rename(columns={'publishedAt': 'yt_release_date',
                     'release_date': 'sp_release_date'}, inplace=True)
    full_drop['explicit'] = full_drop['explicit'].astype(int)
    # drop songs with view less than 10 mil
    full_drop = full_drop[full_drop['view'] > 1e7]
    full_drop.to_csv("Analysis/data_no_genre.csv", index=False)


def merge_genre():
    genre = pd.read_csv("Scrape/Wikipedia/genre_grouped.csv")
    genre = genre[["track_id", "genres"]]
    full = pd.read_csv("Analysis/data_no_genre.csv")
    full_with_genre = pd.merge(full, genre, how="left", on="track_id")
    full_with_genre.to_csv("Analysis/data_with_genre.csv", index=False)


if __name__ == "__main__":
    merge_view()
    merge_genre()
