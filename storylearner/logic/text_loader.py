import pandas as pd
import requests
import os

class TextLoader:

    def __init__(self):
        self.df = pd.read_csv("./pg_catalog_de.csv")

    def get_dataframe(self):
        return self.df

    def get_all_ids(self):
        return self.df["Text#"].to_list()

    def download_to(self, target_dir, ids_to_download, preprocess=lambda x: x):
        blank_link = "https://www.gutenberg.org/ebooks/book-id.txt.utf-8"
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        for id in ids_to_download:
            link = blank_link.replace("book-id", str(id))
            x = requests.get(link)
            file_name = target_dir + str(id) + ".txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(preprocess(x.text))
                f.close()


tl = TextLoader()
tl.download_to("./raw_data/", [1, 2])
