import os
import pandas as pd
from utils import first_iteration, get_failed_ablum, create_csv, headerAlbum

base_dir = "./Scrape/Spotify"
start_index = 0
end_index = 1
folder_path = os.path.join(base_dir, "har" + "-" + str(start_index) + "-" + str(end_index))
end_index += 1
failed_1_path = os.path.join(folder_path, "failed_1.csv")

if __name__ == "__main__":
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    create_csv(failed_1_path, headerAlbum)

    first_iteration(start_index, end_index, folder_path, failed_1_path)

    done = len(pd.read_csv(failed_1_path)) == 0
    failed_file_index = 1
    while not done:
        current_failed_path = os.path.join(folder_path, "failed_{}.csv".format(failed_file_index))
        create_csv(current_failed_path, headerAlbum)

        failed_file_index += 1
        next_failed_path = os.path.join(folder_path, "failed_{}.csv".format(failed_file_index))
        create_csv(next_failed_path, headerAlbum)

        get_failed_ablum(current_failed_path, next_failed_path, folder_path)

        remaining = len(pd.read_csv(next_failed_path))
        if remaining == 0:
            print("------no remaining album to scrape--------")
            done = True
        else:
            print("------{} albums remaining, continue scraping--------".format(remaining))

