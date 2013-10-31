import nltk
import os

collection_directory = "/home/stathis/Projects/UVA_IR/collection/"

index = {}
doc_lengths = {}

for root, dirs, files in os.walk(collection_directory):
    for file in files:
        if file.endswith(".txt"):
            print "Preprocessing File :" + file + " ..."
            f = open(collection_directory + file,'r')
            raw_text = f.read()
            tokenized_text = nltk.word_tokenize(raw_text)
            document = {}
            doc_id = file[0:(len(file)-4)]
            for term in tokenized_text:
            	if term in document:
            		document[term] += 1
            	else:
            		document[term] = 1
            print document['the']
            for word in document.iteritems():
            	if word[0] not in index:
            		index[word[0]] = {}
            		index[word[0]]['df'] = 1
            	else:
            		index[word[0]]['df'] += 1
            	index[word[0]][doc_id] = word[1]
            break

print index['the']
