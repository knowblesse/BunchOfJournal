# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 20:42:35 2017

@author: Jeong Ji Hoon
@Knowblesse

Description:
    Create Unigram and find 100 most appeared words
"""

import nltk
from nltk.util import ngrams
from collections import Counter


DATA_FILE = 'FullText_2013.txt'
# Open Data Files
try :
    with open(DATA_FILE,'r', encoding='UTF-8') as file:
        raw = file.read() 
        file.close()
except IOError as err:
    print('\n Error : Data File\n')
    print(err)

# Count the words
token = nltk.word_tokenize(raw.lower())
raw_bigram = ngrams(token,2)

bigram = Counter(raw_bigram)



# Print Results
try:
    with open('Result_bigram_2013_FT.txt','w',encoding='UTF-8') as of:
        rank = 1
        for element in bigram.most_common(300):
            of.writelines(str(rank) + ' : ' + str(element) + '\n')
            rank = rank + 1
except IOError as err:
    print('Error Saving the Result : ' + str(err))