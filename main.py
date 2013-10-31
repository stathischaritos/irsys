import nltk
import os

collection_directory = "/home/stathis/Projects/UVA_IR/collection/"

for root, dirs, files in os.walk(collection_directory):
    for file in files:
        if file.endswith(".txt"):
            print "Preprocessing File :" + file + " ..."
            f = open(collection_directory + file,'r')
            raw_text = f.read()
            tokenized_text = nltk.word_tokenize(raw_text)
            print tokenized_text
            break

