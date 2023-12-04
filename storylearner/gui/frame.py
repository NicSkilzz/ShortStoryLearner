import tkinter as tk
from tkinter import ttk
from tkinter import *
from storylearner.logic.rarity_ranking_creator import RarityRankingCreater
from storylearner.logic.text_dataframe_creator import TextDataFrameCreator

class App(tk.Frame):
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df
        self.pack()
        self.grid()


        B = Button(self, text ="Search")
        B.grid(row = 0, column = 2, pady = 2)
        B.bind("<Button-1>", self.print_contents)

        l1 = Label(self, text = "Entry:")
        l1.grid(row = 0, column = 0, sticky = W, pady = 2)

        self.e1 = Entry(self)
        self.e1.grid(row = 0, column = 1, pady = 2)


    def print_contents(self, event):
        print(f"{self.e1.get()}")
        self.CreateUI()

    def CreateUI(self):
        self.tv = ttk.Treeview(self)
        self.tv['columns'] = ('ID', 'Title', 'Difficulty')
        self.tv.column("#0", anchor="w", width=0, stretch=NO)

        for column in self.tv['columns']:
            self.tv.heading(column, text=column)
            self.tv.column(column, anchor='center', width=300)

        self.tv.grid(row = 1, column = 1, pady = 2)

        for row in range(self.df.shape[0]):
            self.tv.insert(parent="", index=0, text="", values=(
                self.df['id'][row], self.df['filenames'][row], self.df['difficulty_score'][row])
                           )


tdf_creator = TextDataFrameCreator("./raw_data")
rr_creator = RarityRankingCreater(tdf_creator.dataframe)
tdf_creator.add_average_word_rarity_column(rr_creator.word_rarity_ranking)
tdf_creator.create_scaled_dataframe()
df = tdf_creator.scaled_dataframe


root = tk.Tk()
root.geometry('1200x770')
root.title("NICO")
myapp = App(root, df)
myapp.mainloop()



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
