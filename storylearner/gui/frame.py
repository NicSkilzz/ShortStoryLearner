import tkinter as tk
from storylearner.logic.rarity_ranking_creator import RarityRankingCreater
from storylearner.logic.text_dataframe_creator import TextDataFrameCreator

tdf_creator = TextDataFrameCreator("./raw_data")
rr_creator = RarityRankingCreater(tdf_creator.dataframe)
tdf_creator.add_average_word_rarity_column(rr_creator.word_rarity_ranking)
tdf_creator.create_scaled_dataframe()
print(tdf_creator.scaled_dataframe)

# window
window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()
window.mainloop()
