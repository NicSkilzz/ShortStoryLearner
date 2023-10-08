import pandas as pd

from storylearner.logic.text_dir_iteration import read_text_files_from_directory, turn_filenames_and_cleaned_texts_into_dataframe, add_describing_columns_to_dataframe


def create_total_word_list_with_duplicates(dataframe: pd.DataFrame):
    '''
    Input: DataFrame with a "word_list" column.
    Output: List containing all the words from all the texts with duplicates.
    '''
    total_word_list_with_duplicates = [
        word for list in dataframe['word_list'] for word in list]

    return total_word_list_with_duplicates


def create_word_rarity_ranking(total_word_list_with_duplicates: list):
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

    # Iterate through word_list_without_duplicates and calculate the percentage of each word
    for current_word in word_list_without_duplicates:
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

    return word_rarity_ranking_df


if __name__ == '__main__':
    # Create Test-DataFrame
    rel_path_directory = './raw_data'
    list_of_all_filenames, list_of_all_cleaned_texts = read_text_files_from_directory(
        rel_path_directory)
    dataframe = turn_filenames_and_cleaned_texts_into_dataframe(
        list_of_all_filenames, list_of_all_cleaned_texts)
    new_dataframe = add_describing_columns_to_dataframe(dataframe)

    # Create total_word_list_with_duplicates
    total_word_list_with_duplicates = create_total_word_list_with_duplicates(
        new_dataframe)
    # print(len(total_word_list_with_duplicates))

    word_rarity_ranking = create_word_rarity_ranking(
        total_word_list_with_duplicates)
    print(word_rarity_ranking)
