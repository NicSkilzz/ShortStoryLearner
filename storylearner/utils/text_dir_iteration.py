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
        text_only_letters_and_lower_case = ''.join(character for character in content if character.isalpha() or character in important_characters)

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


rel_path_directory = './raw_data'
list_of_all_filenames, list_of_all_cleaned_texts = read_text_files_from_directory(rel_path_directory)
dataframe = turn_filenames_and_cleaned_texts_into_dataframe(list_of_all_filenames, list_of_all_cleaned_texts)
print(dataframe)
