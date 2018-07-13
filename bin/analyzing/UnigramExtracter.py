# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 20:42:35 2017

@author: Jeong Ji Hoon
@Knowblesse

Description:
    Create Unigram and find 500 most appeared words
"""

import nltk
from collections import Counter


DATA_FILE = 'Abstracts_2016.txt'
# Open Data Files
try :
    with open(DATA_FILE,'r', encoding='UTF-8') as file:
        raw = file.read() 
        file.close()
except IOError as err:
    print('\n Error : Data File\n')
    print(err)
    
# Open Exception Word File
try :
    with open('C:\exclude.txt','r') as excludeFile:
        ex = excludeFile.read()
        excludeFile.close()
except:
    print('\n Error : Exclude File is Missing\n')

# Count the words
token = nltk.word_tokenize(raw.lower())
token_ex = nltk.word_tokenize(ex)

raw_unigrams = Counter(token)
unigrams = raw_unigrams.copy()

# Delete Frequenct Meaningless Words
for exEl in token_ex:
    if exEl in unigrams:
        del(unigrams[exEl])

# Print Results
try:
    with open('Result_2013.txt','w',encoding='UTF-8') as of: # Output File
        rank = 1
        for element in unigrams.most_common(500):
            of.writelines(str(rank) + ' : ' + str(element) + '\n')
            rank = rank + 1
except IOError as err:
    print('Error Saving the Result : ' + str(err))