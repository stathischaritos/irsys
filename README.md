IRSYS (IR SYSTEM)
=================
This is an end to end IR system written in Python , as part of a lab assignment in the Course of IR at UvA. 

I separated the components of the system in different files (preprocessing - indexing  - query models) and i made a main executable script 
called irsys which has the following usage:

	usage: irsys [-h] [-j {index,query,session}] [-p PATH] [-q QUERY] [-e]
             [-qid {6,7}]

	optional arguments:
	  -h, --help            show this help message and exit
	  -j {index,query,session}, --job {index,query,session}
	                        Specify the job you need to run.
	  -p PATH, --path PATH  Path of file or directory to index
	  -q QUERY, --query QUERY
	                        Query string to run (for single query mode)
	  -e, --eval            Make res file and evaluate using terrier
	  -qid {6,7}, --qid {6,7}
	                        Pick one of the predefined queries to evaluate using
	                        terrier


By default the program will start in "session" mode where you can run multiple queries. Otherwise you need to specify a job (index, query , session) and then you will get prompted for the required inputs , or you can also add them as arguments like -p for the indexing path or -q for the single query string. More arguments are to be added later ex. for what stemmers to use , providing a list of stopwords etc.

So it can now index either a specified file or directory ( re-indexing also works as an update not as simple addition ) , and you can
run a simple AND query (taking the intersection of the documents for every term of the query).

To run and evaluate one of the peredefined queries you can do:

	./irsys -qid 6


Preprocessing:
===============

Sentence and Word Tokeniser 

Word Clustering - Stemming - Lemmatization
--------------------------------------------

-	Porter Stemmer
-	Lancaster Stemmer 
-	Other Stemmers
-	WordNet

I made three new functions in the preprocessing component that do Porter Stemming - Lancaster and Wordnet Lemmatization (all from nltk) of the tokenised text and so  now we can run all these processes but we need to remove the old index if it uses a different stemmer combination. I should add some index info in the index dict so that its done automatically (it should get deleted if the new stemming is different than the old , also the queries need to be preprocessed the same way as the index.)

to use wordnet we need the nltk_data folder which you can download by opening the python session and doing :

	import nltk
	nltk.download()

It might take some time , and space , but you can just choos the wordnet package you dont have to download the whole thing.

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

-	Boolean
-	tf-idf
-	BM25
-	cosine-distance

In Boolean Retrieval when you have a query like " term1 term2 term3"
you can do the intersection of the documents for every term, meaning that you return only the documents
that contain all query terms. For the other models we coud implement a weighting factor for each document
that depends on how many of the terms it contains , and figure out these weights by optimising on the developement set.


Evaluation:
=================
For evaluation is is suggested in the assignment to use :
	http://thetrecfiles.nonrelevant.net/

But for easier local evaluation i downloaded "terrier" from http://terrier.org/ that has an evaluation module for trec files:

To do evaluation with Terrier we need to have the trec.qrels inside the trec folder (this is a setting at "terrier/etc/terrier.parameters")
and specify the file or folder of results (.res files ) you want to evaluate:

	./trec_terrier.sh -e /home/stathis/Projects/UVA_IR/results/*

I think this way its going to be easier to evaluate automatically each query right after running it.


One issue we have is that the some of the "relevant" files in the qrels file do not exist in our collections as it is a subset of the whole
collection. This way we will always get worse precision due to our incomplete document set. To solve this we could remove these document ids from the qrels file.

Ok i did write a script to generate a new qrels file but im getting the same precision results for the intersection query...

I made a simple evaluation function in helpers.py

Django demo:
=============
I made a simple django page to demonstrate the system using only python code.
to start the django server go inside the irsysweb directory and run:

	python manage.py runserver

And then go to http://127.0.0.1:8000/irsys/


Dependencies:
===============
NLTK 
-----

	http://nltk.org/

Simple text Progressbar
------------------------

	sudo pip install progressbar


Django
-------
	sudo pip install django