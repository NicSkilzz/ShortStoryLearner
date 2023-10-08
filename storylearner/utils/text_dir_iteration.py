import os
import pandas as pd


def read_text_files_from_directory(directory_path: str):
    '''
    Input: Path to directory containing only text files.
    Ouptut: List of all filenames in directory, list of all cleaned texts from files
    -> return list:filenames, list:cleaned_texts
    '''

    # Create empty lists for variables
    list_of_all_filenames = []
    list_of_all_cleaned_texts = []

    for filename in os.listdir(directory_path):

        #Read the file
        filepath = os.path.join(directory_path, filename)
        f = open(filepath, 'r')
        content = f.read()

        # Clean the text
        ## by removing all characters except letters and selected characters in variable: important_characters
        important_characters = ",. :"
        text_only_letters_and_lower_case = ''.join(
            character for character in content if character.isalpha() or character in important_characters
            )

        # Append current variables to corresponding lists
        list_of_all_filenames.append(filename)
        list_of_all_cleaned_texts.append(text_only_letters_and_lower_case)

    return list_of_all_filenames, list_of_all_cleaned_texts


def turn_filenames_and_cleaned_texts_into_dataframe(list_of_all_filenames: list, list_of_all_cleaned_texts: list):
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


def add_describing_columns_to_dataframe(dataframe: pd.DataFrame):
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
    dataframe['word_list'] =  dataframe['cleaned_text'].apply(
        lambda x: x.replace(',', ' ').replace('.', ' ').replace(':', ' ').lower().split()
        )

    # Add word word_count_with_duplicates column
    dataframe['word_count_with_duplicates'] = len(dataframe['word_list'])

    # Add word word_count_with_duplicates column
    dataframe['word_count_without_duplicates'] = dataframe['word_list'].apply(
        lambda x: len(set(x))
            )

    return dataframe


def create_total_word_list_with_duplicates(dataframe: pd.DataFrame):
    '''
    Input: DataFrame with a "word_list" column.
    Output: List containing all the words from all the texts with duplicates.
    '''
    total_word_list_with_duplicates = [word for list in dataframe['word_list'] for word in list]

    return total_word_list_with_duplicates


rel_path_directory = './raw_data'
list_of_all_filenames, list_of_all_cleaned_texts = read_text_files_from_directory(rel_path_directory)
dataframe = turn_filenames_and_cleaned_texts_into_dataframe(list_of_all_filenames, list_of_all_cleaned_texts)
new_dataframe = add_describing_columns_to_dataframe(dataframe)
total_word_list_with_duplicates = create_total_word_list_with_duplicates(new_dataframe)
print(len(total_word_list_with_duplicates))
