from helpers import *

index = load_index()

newf = open('trec/newtrec.qrels','wb')

with open('trec/trec.qrels','r') as f:
    for line in f:
        parts =  line.split(" ")
        if parts[2] in index["indexed_docs"]:
        	newf.write(line)



newf.close()