import os
#from pathlib import Path


rel_path_directory = './raw_data'

for filename in os.listdir(rel_path_directory):
    filepath = os.path.join(rel_path_directory, filename)
    f = open(filepath, 'r')
    content = f.read()
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    clean_content = ''.join(character.lower() for character in content if character.isalpha() or character==' ')
    content_list = clean_content.split()
    print(len(content_list))
    print(len(set(content_list)))
