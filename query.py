
from indexing import *

def intersection(query_string,index):
	
	query = preprocess(query_string)
	a = []
	b = []
	i = 0
	
	query_clean = []
	for word in query:
	    if word in index['tokens']:
	    	query_clean += [word]

	query = query_clean

	for word in query:
	    if word in index['tokens']:
	    	if i == 0:
	    		a = index['tokens'][word]['counts'].keys()
	    		i = 1
	    	else:
	    		b = index['tokens'][word]['counts'].keys()
	    		a = list(set(a) & set(b))

	for x in a:   		
		doc = []
		for word in query:
			doc +=[word , index['tokens'][word]['counts'][x] ]
	return a

