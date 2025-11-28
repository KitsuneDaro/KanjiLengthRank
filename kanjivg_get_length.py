#!/usr/bin/env python3

import os
from tqdm import tqdm
import pandas as pd
from svg.path import parse_path

KANJI_SOURCE_FOLDER = '../kanjivg-20250816-main/kanji/'
KANJI_DESTINATION_FOLDER = './converted/'

# A function that allows you to retrieve a string between two specified strings
def find_between(s: str, first, last):
    try:
        start = s.find( first ) + len( first )
        end = s.find( last, start )
        return s[start:end]
    except ValueError:
        return ""

kanji_length_dict = pd.DataFrame(columns=('char', 'length', 'count'))

# Iterate through each svg file in the kanji directory.
file_list = os.listdir(KANJI_SOURCE_FOLDER)

for file in tqdm(file_list):
    # The source and target files
    source_file = open(KANJI_SOURCE_FOLDER + file, 'r', encoding='utf8')

    # The array that will contain all values of 'd' (the path code) in the original svg file
    dpath = []
    kanji_char = ''

    # Retrieve the value of 'd' (the path code) in the original svg file

    for line in source_file:
        if '<g' in line and 'kvg:element="' in line and kanji_char != '':
            kanji_char = find_between(line, 'kvg:element="', '"')

        if '<path' in line and 'd="' in line:
            dpath.append(find_between(line, ' d="', '"/>'))

    source_file.close()

    # The value of i represents 
    all_path_length = 0
    
    # Then we handle the black kanji strokes, which will be animated in the foreground
    for b in dpath:
        path_length = parse_path(b).length()
        
        all_path_length += path_length
    
    kanji_length_dict.loc[len(kanji_length_dict), :] = (kanji_char, all_path_length, len(dpath))

kanji_length_dict.to_csv('./output/result_origin.csv')

# When the script is finished converting all files in the specified directory, it will print the following message to indicate it has finished.
print('Done.')
