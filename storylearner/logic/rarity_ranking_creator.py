import pandas as pd

from storylearner.logic.text_dir_iteration import DataFrameCreator

class RarityRankingCreater:

    def __init__(self, dataframe):
        '''Uses the class functions to create the word rarity ranking.

        Args:
            dataframe (pd.DataFrame): DataFrame that contains word lists from all texts.
        '''
        self.dataframe = dataframe
        self.total_word_list_with_duplicates = self.create_total_word_list_with_duplicates(
            self.dataframe
        )
        self.word_rarity_ranking = self.create_word_rarity_ranking(
            self.total_word_list_with_duplicates
        )

    def create_total_word_list_with_duplicates(self, dataframe: pd.DataFrame):
        '''
        Input: DataFrame with a "word_list" column.
        Output: List containing all the words from all the texts with duplicates.
        '''
        total_word_list_with_duplicates = [
            word for list in dataframe['word_list'] for word in list]

        return total_word_list_with_duplicates


    def create_word_rarity_ranking(self, total_word_list_with_duplicates: list):
        '''
        Input: List of all the words from all the texts with duplicates
        Output: DataFrame with columns ("word", "word_percentage", "ranking")
        '''

        # Calculate total_amount_words
        total_amount_words = len(total_word_list_with_duplicates)

        # Create word_list_without_duplicates
        word_list_without_duplicates = list(set(total_word_list_with_duplicates))

        # Create lists for columns: "word" and "word_percentage"
        word_list = []
        word_percentage_list = []
        print("Starting Iteration word_list_without_duplicates")
        amount = 0
        print(len(word_list_without_duplicates))
        # Iterate through word_list_without_duplicates and calculate the percentage of each word
        for current_word in word_list_without_duplicates:
            amount += 1
            if amount % 100 == 0:
                print(f"{amount} / {len(word_list_without_duplicates)}")
            if current_word not in word_list:
                current_word_count = 0
                for word in total_word_list_with_duplicates:
                    if word == current_word:
                        current_word_count += 1

                # Calculate current_word_percentage
                current_word_percentage = current_word_count / total_amount_words

                # Append current values to lists
                word_list.append(current_word)
                word_percentage_list.append(current_word_percentage)

        # Create a temporary dictionary
        word_rarity_df_as_dict = {
            'word': word_list,
            'word_percentage': word_percentage_list
        }

        # Turn dictionary into DataFrame
        word_rarity_df = pd.DataFrame(word_rarity_df_as_dict)

        # Sort dataframe by word_percentage (descending)
        word_rarity_ranking_df = word_rarity_df.sort_values(
            'word_percentage', ascending=False, ignore_index=True)

        # Add ranking column to word_rarity_ranking_df
        word_rarity_ranking_df['ranking'] = word_rarity_ranking_df.index + 1

        # Set the words as the index of the df
        word_rarity_ranking_df = word_rarity_ranking_df.set_index('word')

        return word_rarity_ranking_df


if __name__ == '__main__':
    # Create Test-DataFrame
    rel_path_directory = './raw_data'
    testclass = DataFrameCreator(rel_path_directory)
    first_dataframe = testclass.dataframe
    print("Created DataFrame")

    # Create total_word_list_with_duplicates
    testclass2 = RarityRankingCreater(first_dataframe)
    print(testclass2.word_rarity_ranking)
    print(testclass2.word_rarity_ranking.loc['and', 'word_percentage'])

    # Add average word rarity to dataframe
    testclass.add_average_word_rarity_column(testclass2.word_rarity_ranking)
    print(testclass.dataframe['average_word_rarity'])
