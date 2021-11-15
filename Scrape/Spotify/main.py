import os
import pandas as pd
from utils import first_iteration, get_failed_ablum, create_csv, headerSong, headerAlbum

base_dir = "./Scrape/Spotify"
start_index = 2400
end_index = 2420
folder_path = os.path.join(base_dir, str(start_index))
success_path = os.path.join(folder_path, "success.csv")
failed_1_path = os.path.join(folder_path, "failed_1.csv")

if __name__ == "__main__":
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    create_csv(success_path, headerSong)
    create_csv(failed_1_path, headerAlbum)

    first_iteration(start_index, end_index, success_path, failed_1_path)

    done = len(pd.read_csv(failed_1_path)) == 0
    failed_file_index = 1
    while not done:
        current_failed_path = os.path.join(folder_path, "failed_{}".format(failed_file_index))
        failed_file_index += 1
        next_failed_path = os.path.join(folder_path, "failed_{}".format(failed_file_index))

        get_failed_ablum(current_failed_path, next_failed_path, success_path)

        done = len(pd.read_csv(next_failed_path)) == 0
