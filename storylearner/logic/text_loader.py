import pandas as pd
import requests
import os

class TextLoader:

    def __init__(self):
        self.df = pd.read_csv("./pg_catalog_de.csv")

    def get_dataframe(self):
        '''Return the dataframe containing all the metadata to all german texts.

        Returns:
            pd.Dataframe: The pandas dataframe.
        '''
        return self.df

    def get_all_ids(self):
        '''Get the IDs of all german texts.

        Returns:
            list: List of IDs as int.
        '''
        return self.df["Text#"].to_list()

    def download_to(self, target_dir, ids_to_download, preprocess=lambda x: x):
        '''Download the texts with the given IDs from the Gutenberg server.

        Args:
            target_dir (str): Directory to save files to.
            ids_to_download (list): List of IDs of the texts to download.
            preprocess (function, optional): Function for preprocessing texts before saving to file. Defaults to lambdax:x.
        '''
        blank_link = "https://www.gutenberg.org/ebooks/book-id.txt.utf-8"
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        print("Starting Download...")
        downloaded = 0
        for id in ids_to_download:
            link = blank_link.replace("book-id", str(id))
            file_name = target_dir + str(id) + ".txt"
            if not os.path.exists(file_name):
                x = requests.get(link)
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(preprocess(x.text))
                    f.close()
                downloaded += 1
            if downloaded % 10 == 0 and downloaded != 0:
                print(str(downloaded) + " / " + str(len(ids_to_download)))


tl = TextLoader()
tl.download_to("./raw_data/", tl.get_all_ids())
