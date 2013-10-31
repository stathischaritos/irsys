Preprocessing:
===============

Sentence and Word Tokeniser 

Word Clustering - Stemming - Lemmatization

	Porter Stemmer
	
	Lancaster Stemmer 
	
	Other Stemmers
	
	WordNet
	
Stop words ( remove or index separately? )

Granularity


Indexing:
===============
I think the index needs to be a dictionary of the form:
[term][df] => [ [doc_id , tf] , [doc_id , tf] , [doc_id , tf] , [doc_id , tf] , [doc_id , tf] ]

ok i made a dictionary for the index that we can use like:

index["term"]["df"] to get the document frequency

index["term"]["doc_id"] to get the term frequency for each document


There seem to be some invalid characters , i think it has to do with the encoding , fix it later.

IR:
==============
We can implement the following systems:
Boolean
tf-idf
BM25
cosine-distance

