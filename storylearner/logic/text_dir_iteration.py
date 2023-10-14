import os
import pandas as pd
import spacy

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

        # Read the file
        filepath = os.path.join(directory_path, filename)
        f = open(filepath, 'r', encoding='utf-8')
        content = f.read()

        cleaned_text = clean_text(content)
        

        # Append current variables to corresponding lists
        list_of_all_filenames.append(filename)
        list_of_all_cleaned_texts.append(cleaned_text)

    return list_of_all_filenames, list_of_all_cleaned_texts


def clean_text(text: str):

    # remove all characters except letters and selected characters in variable: important_characters
    important_characters = ",. :"
    cleaned_text = ''.join(
        character for character in text if character.isalpha() or character in important_characters
    )

    # remove all names
    # if throws error run: python[3] -m spacy download de_core_news_lg
    # nlp = spacy.load("de_core_news_lg")
    # doc = nlp(text)
    # for ne in doc.ents:
    #     print(ne.label_)
    #     print(ne)
    # print(nlp.pipe_names)
    return cleaned_text


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
    dataframe['word_list'] = dataframe['cleaned_text'].apply(
        lambda x: x.replace(',', ' ').replace(
            '.', ' ').replace(':', ' ').lower().split()
    )

    # Add word_count_with_duplicates column
    dataframe['word_count_with_duplicates'] = len(dataframe['word_list'])

    # Add word_count_with_duplicates column
    dataframe['word_count_without_duplicates'] = dataframe['word_list'].apply(
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
    dataframe['average_word_length'] = dataframe['word_list'].apply(
        lambda x: calculate_average_word_length(x)
    )

    return dataframe


if __name__ == '__main__':
    rel_path_directory = './raw_data'
    list_of_all_filenames, list_of_all_cleaned_texts = read_text_files_from_directory(
        rel_path_directory)
    dataframe = turn_filenames_and_cleaned_texts_into_dataframe(
        list_of_all_filenames, list_of_all_cleaned_texts)
    new_dataframe = add_describing_columns_to_dataframe(dataframe)
    print(new_dataframe['cleaned_text'])
