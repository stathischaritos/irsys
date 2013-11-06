from indexing import *



def run_query(query_string , index , model='intersection'):
            print "Running Query..."
            result =[]
            if model =='intersection':
                  result = intersection(query_string , index)
            elif model == 'bm25':
            	result = bm25(query_string,index)
            elif model == 'tfidf':
           		result = tfidf(query_string,index)
            return result
      


def bm25(query_string,index):
	#magic

	result = "nothing done yet"

	#result = sorted(result, key=lambda tup: tup[1])[::-1]
	return result

def tfidf(query_string,index):
	#magic

	result = "tfidf nothing done yet"

	#result = sorted(result, key=lambda tup: tup[1])[::-1]
	return result

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

	# for x in a:   		
	# 	doc = []
	# 	for word in query:
	# 		doc +=[word , index['tokens'][word]['counts'][x] ]
	result = []
	for doc in index['indexed_docs']:
		if doc in a:
			result += [[doc , 1]]
		else:
			result += [[doc , 0]]

	## Sort Results by score
	result = sorted(result, key=lambda tup: tup[1])[::-1]
	return result

