import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class TextDataFrameCreator:

    def __init__(self, directory_path):
        '''Uses the class functions to create the complete Dataframe and save the variables after each step.

        Args:
            directory_path (str): Path that leads to the directory containing the txt files for the dataframe.
        '''
        self.directory_path = directory_path
        self.list_of_all_filenames, self.list_of_all_cleaned_texts = self.read_text_files_from_directory(self.directory_path)
        self.dataframe = self.turn_filenames_and_cleaned_texts_into_dataframe(
            self.list_of_all_filenames, self.list_of_all_cleaned_texts
        )
        self.add_describing_columns_to_dataframe()
        self.add_average_sentence_length()


    def read_text_files_from_directory(self, directory_path: str):
        '''
        Input: Path to directory containing only text files.
        Ouptut: List of all filenames in directory, list of all cleaned texts from files
        -> return list:filenames, list:cleaned_texts
        '''

        # Create empty lists for variables
        list_of_all_filenames = []
        list_of_all_cleaned_texts = []

        for filename in os.listdir(directory_path):

            # Read the file
            filepath = os.path.join(directory_path, filename)
            f = open(filepath, 'r', encoding='utf-8')
            content = f.read()

            # Clean the text
            # by removing all characters except letters and selected characters in variable: important_characters
            important_characters = ",. :"
            text_only_letters_and_lower_case = ''.join(
                character for character in content if character.isalpha() or character in important_characters
            )

            # Append current variables to corresponding lists
            list_of_all_filenames.append(filename)
            list_of_all_cleaned_texts.append(text_only_letters_and_lower_case)

        return list_of_all_filenames, list_of_all_cleaned_texts


    def turn_filenames_and_cleaned_texts_into_dataframe(self, list_of_all_filenames: list, list_of_all_cleaned_texts: list):
        '''
        Input: List of all filenames and list of all cleaned texts of those files.
        Output: DataFrame with ... variables.
        '''

        dataframe_as_dictionary = {
            'filenames': list_of_all_filenames,
            'cleaned_text': list_of_all_cleaned_texts,
        }

        dataframe = pd.DataFrame(dataframe_as_dictionary)

        return dataframe


    def add_describing_columns_to_dataframe(self):
        '''
        Input: DataFrame with columns named ("filenames", "cleaned_text")
        Output: DataFrame with given and added columns
        (
            - "word_list",
            - "word_count_with_duplicates",
            - "word_count_without_duplicates",
            )
        '''

        # Add word_list column
        self.dataframe['word_list'] = self.dataframe['cleaned_text'].apply(
            lambda x: x.replace(',', ' ').replace(
                '.', ' ').replace(':', ' ').lower().split()
        )

        # Add word_count_with_duplicates column
        self.dataframe['word_count_with_duplicates'] = self.dataframe['word_list'].apply(
            lambda x: len(x)
            )

        # Add word_count_with_duplicates column
        self.dataframe['word_count_without_duplicates'] = self.dataframe['word_list'].apply(
            lambda x: len(set(x))
        )

        # Create function to calculate the average word length
        def calculate_average_word_length(word_list: list):
            '''
            Input: word_list
            Output: average word length
            '''
            # Calculate the total characters in the given text
            total_characters = len(
                ''.join(character for word in word_list for character in word))

            # Calculate the total words in the given text
            total_words = len(word_list)

            # Calculate average
            average_word_length = total_characters / total_words

            return average_word_length

        # Apply function to calculate the average word length to DataFrame
        self.dataframe['average_word_length'] = self.dataframe['word_list'].apply(
            lambda x: calculate_average_word_length(x)
        )


    def add_average_word_rarity_column(self, word_rarity_ranking: pd.DataFrame):
        '''_summary_

        Args:
            word_rarity_ranking (pd.DataFrame): _description_
        '''

        def average_word_rarity_calculator(word_list: list , word_rarity_ranking: pd.DataFrame):
            '''_summary_

            Args:
                word_list (_type_): _description_
                word_rarity_ranking (_type_): _description_
            '''
            # Summe aller Prozentanteile Wörter = 0
            # Anzahl Wörter im Text mit Duplikaten

            # Iteration über alle Wörter des Texts
            ## Wenn in word_list:
            ### Summe += Prozentanteile des jeweiligen Wortes

            # Durschnitt = Summe / Anzahl


            sum_percentage = 0
            amount_words = len(word_list)

            for word in word_list:
                try:
                    curr_percentage = word_rarity_ranking.loc[word, 'word_percentage']
                    sum_percentage += curr_percentage
                except KeyError:
                    continue

            return sum_percentage / amount_words

        # Apply the function average_word_rarity_calculator to each list in the pd.Series 'word_list' column
        # Create a column average_word_list
        self.dataframe['average_word_rarity'] = self.dataframe['word_list'].apply(
            lambda x: average_word_rarity_calculator(x, word_rarity_ranking)
        )

    def add_average_sentence_length(self):
        '''Adds the average sentence length to the dataframe. Adds 2 columns:
        "word_list_including_symbols' and "average_sentence_length"
        '''

        # Replace the punctuation with a punctuation in between to spaces
        # Create a list with all the words and punctuations seperated from the words
        self.dataframe['word_list_including_symbols'] = self.dataframe['cleaned_text'].apply(
            lambda x: x.replace(',', ' , ').replace(
                '.', ' . ').replace(':', ' : ').lower().split()
        )

        # Calculate the average sentence length
        # Words / symbols
        self.dataframe['average_sentence_length'] = self.dataframe['word_count_with_duplicates'] / (self.dataframe['word_list_including_symbols'].str.len() - self.dataframe['word_count_with_duplicates'])

    def create_scaled_dataframe(self):

        # Filter needed columns from dataframe
        filtered_dataframe = self.dataframe.filter(
            items=['filenames', 'average_word_length', 'average_sentence_length', 'average_word_rarity']
        )

        # Use filename from column 'filenames' as the index
        usable_dataframe = filtered_dataframe.set_index('filenames')

        # Create the scaler and fit and transform the data
        mmscaler = MinMaxScaler()
        scaled_ndarray = mmscaler.fit_transform(usable_dataframe)

        # Turn scaled_ndarray into DataFrame
        self.scaled_dataframe = pd.DataFrame(scaled_ndarray, columns=usable_dataframe.columns)

        # Set filenames as index
        self.scaled_dataframe['filenames'] = filtered_dataframe['filenames']
        self.scaled_dataframe['id'] = self.scaled_dataframe['filenames'].apply(lambda x: int(x.replace(".txt", "")))
        #self.scaled_dataframe = self.scaled_dataframe.set_index('filenames')

        # Add a difficulty store column to the scaled_dataframe
        self.scaled_dataframe['difficulty_score'] = (
            self.scaled_dataframe['average_word_length']
            + self.scaled_dataframe['average_sentence_length']
            + (1 - self.scaled_dataframe['average_word_rarity'])
            )



if __name__ == '__main__':
    testclass = TextDataFrameCreator("./raw_data")
    print(testclass.dataframe.columns)
    print(testclass.dataframe['average_sentence_length'])
    print(testclass.dataframe['cleaned_text'])
    print(testclass.dataframe['word_list_including_symbols'])
