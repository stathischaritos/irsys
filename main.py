import nltk
import os
from progressbar import ProgressBar


collection_directory = "/home/stathis/Projects/UVA_IR/collection/"
index = {}
doc_lengths = {}
pbar = ProgressBar()

for root, dirs, files in os.walk(collection_directory):
    for file in pbar(files):
        if file.endswith(".txt"):
            ## Open every file in the collection and read the text
            f = open(collection_directory + file,'r')
            raw_text = f.read()

            ############## Preprocessing Steps here ##########################
            ## Result should be a list of tokens
            tokenized_text = nltk.word_tokenize(raw_text)
            ##################################################################


            ############## Indexing Steps here ###############################
            ## Result should a posting list
            document = {}
            doc_id = file[0:(len(file)-4)]
            for term in tokenized_text:
            	if term in document:
            		document[term] += 1
            	else:
            		document[term] = 1
            for word in document.iteritems():
            	if word[0] not in index:
            		index[word[0]] = {}
            		index[word[0]]['df'] = 1
            	else:
            		index[word[0]]['df'] += 1
            	index[word[0]][doc_id] = word[1]
            ##################################################################

print index['the']
