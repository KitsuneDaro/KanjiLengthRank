#!/usr/bin/env python3

import os
from tqdm import tqdm
import pandas as pd
from svg.path import parse_path

KANJI_SOURCE_FOLDER = '../kanjivg-20250816-main/kanji/'

# A function that allows you to retrieve a string between two specified strings
def find_between(s: str, first, last):
    try:
        start = s.find( first ) + len( first )
        end = s.find( last, start )
        return s[start:end]
    except ValueError:
        return ""

# Iterate through each svg file in the kanji directory.
file_list = os.listdir(KANJI_SOURCE_FOLDER)
kanji_length_dict = pd.read_csv('./output/result_failed.csv', index_col=0)

for i, file in tqdm(enumerate(file_list)):
    # The source and target files
    source_file = open(KANJI_SOURCE_FOLDER + file, 'r', encoding='utf8')

    # The array that will contain all values of 'd' (the path code) in the original svg file
    dpath = []
    kanji_char = ''

    # Retrieve the value of 'd' (the path code) in the original svg file

    for line in source_file:
        if '<g' in line and 'kvg:element="' in line:
            kanji_char = find_between(line, 'kvg:element="', '"')
            break

    source_file.close()
    
    kanji_length_dict.loc[i, 'char'] = kanji_char
    kanji_length_dict.loc[i, 'id'] = file[:-4]

kanji_length_dict = kanji_length_dict.reindex(columns=('id', 'char', 'count', 'length'))
kanji_length_dict.to_csv('./output/result_fixed.csv')

# When the script is finished converting all files in the specified directory, it will print the following message to indicate it has finished.
print('Done.')
