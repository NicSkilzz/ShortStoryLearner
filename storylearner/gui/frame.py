import tkinter as tk
from tkinter import ttk
from tkinter import *
from storylearner.logic.rarity_ranking_creator import RarityRankingCreater
from storylearner.logic.text_dataframe_creator import TextDataFrameCreator

class App(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()
        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>',
                             self.print_contents)

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

root = tk.Tk()
myapp = App(root)
myapp.mainloop()
# tdf_creator = TextDataFrameCreator("./raw_data")
# rr_creator = RarityRankingCreater(tdf_creator.dataframe)
# tdf_creator.add_average_word_rarity_column(rr_creator.word_rarity_ranking)
# tdf_creator.create_scaled_dataframe()
# df = tdf_creator.scaled_dataframe

# # window
# window = tk.Tk()
# greeting = tk.Label(text="Hello, Tkinter")

# tree_view = ttk.Treeview(window)
# tree_view.pack()
# tree_view["columns"] = list(df.columns)
# for i in list(df.columns):
#     tree_view.column(i, anchor="w")
#     tree_view.heading(i, text=i, anchor="w")

# for index, row in df.iterrows():
#     tree_view.insert("", 0, text=index, values=list(row))

# greeting.pack()
# window.mainloop()
