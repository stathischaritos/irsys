IRSYS (IR SYSTEM)
=================
This is an end to end IR system written in Python , as part of a lab assignment in the Course of IR at UvA. 

Preprocessing:
===============

Sentence and Word Tokeniser 

Word Clustering - Stemming - Lemmatization
-------------------------------------------

	Porter Stemmer
	
	Lancaster Stemmer 
	
	Other Stemmers
	
	WordNet
	
Stop words
--------------
 ( remove or index separately? )
I was thinking we could index stop words in a separate file and then run some experiments on subgroups of them . For example we 
could try taking only the N most frequent stopwords.

Granularity:
-------------
Right now we index every document as a whole , and this is fine for small documents , buts for langer documents like books , it is best to treat chapters or pages separately.


Indexing:
===============
The index at this point has the following structure:

index=>{

	"indexed_docs"=>{
						"doc1" => { "length" => 1000},
						"doc2" => { "length" => 500},
						....
					},

	"tokens" =>{
					"the" =>{ 
								"counts" => {
												"doc1" => 5,
												"doc2" => 10,
												....
											},
								"df"    =>  10,
								"total_counts" => 100
							},
				
					"of"  =>{ 
								"counts" => {
												"doc1" => 20,
												"doc2" => 30,
												....
											},
								"df"    =>  25,
								"total_counts" => 200
							},
					....
				}
}



There seem to be some invalid characters , i think it has to do with the encoding , fix it later.

IR: 
==============

We can implement the following ranking functions:
-Boolean
-tf-idf
-BM25
-cosine-distance

In Boolean Retrieval when you have a query like " term1 term2 term3"
you can do the intersection of the documents for every term, meaning that you return only the documents
that contain all query terms. For the other models we coud implement a weighting factor for each document
that depends on how many of the terms it contains , and figure out these weights by optimising on the developement set.


Dependencies:
===============
NLTK 
-----

	http://nltk.org/

Simple text Progressbar
------------------------

	sudo pip install progressbar