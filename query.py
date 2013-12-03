from indexing import *
import operator
import math

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
      


def tfidf(query_string,index):
	print 'Model tfidf'

	## Preprocess the Query String using the same steps as the index. 
	N = len(index['indexed_docs'])
	query = preprocess(query_string,index['info']['stemmer'],index['info']['lemmatization'] , index['info']['remove_stopwords'] , index['info']['stopwords'])
	result = []
	newd = {}
    
    ## Run tf-idf
	for word in query:
	    max_freq = max(index['tokens'][word]['counts'].iteritems(), key=operator.itemgetter(1))[1]
	    df = index['tokens'][word]['df']
	    idf = math.log(float( 1+ N ) / float(1 + df))
	    for tf_doc_id in index['tokens'][word]['counts'].keys() :	
	    	freq = index['tokens'][word]['counts'] [tf_doc_id]
	    	tf = float(freq) / max_freq #float(tel['length'])
	    	tfidf = float(tf) * float(idf)
	    	if tf_doc_id not in newd :
	    		newd[tf_doc_id] = tfidf
	    	else :
	    		newd[tf_doc_id] += tfidf

	for key, value in newd.iteritems():
		temp = [key,value]
		result.append(temp)

	## Rank results according to score
	result = sorted(result, key=lambda tup: tup[1])[::-1]
	return result



def bm25(query_string,index):
	print 'Model bm25'
	
	N = len(index['indexed_docs'])
	sum_of_idf = 0
	result = []
	a = []

	query = preprocess(query_string,index['info']['stemmer'],index['info']['lemmatization'] , index['info']['remove_stopwords'] , index['info']['stopwords'])
	for word in query:
		df = index['tokens'][word]['df']
		sum_of_idf += math.log(float( 1+ N ) / float(1 + df))
	
	newd = {}
	#average document length for the whole collection
	total_tokens = 0
	for x in index['indexed_docs']:
		total_tokens += index['indexed_docs'][x]['length']

	lave = float(total_tokens / len(index['indexed_docs']))
	k1 = float(1.2)
	b = float(0.75)

	#Cumpute and store the score
	for word in query:
	    #print max(index['tokens'][word]['counts'].iteritems(), key=operator.itemgetter(1))
	    max_freq = max(index['tokens'][word]['counts'].iteritems(), key=operator.itemgetter(1))[1]
	    for tf_doc_id in index['tokens'][word]['counts'].keys() :
	    	freq = index['tokens'][word]['counts'] [tf_doc_id]
	    	tf = float(freq) / float(max_freq) #float(tel['length'])
	    	ld = float(index['indexed_docs'][tf_doc_id]['length'])
	    	score = ((k1+1)*tf)/(k1*((1-b)+b*(ld/lave))+tf) * sum_of_idf
	    	if tf_doc_id not in newd :
	    		newd[tf_doc_id] = score
	    	else :
	    		newd[tf_doc_id] += score


	for key, value in newd.iteritems():
		temp = [key,value]
		result.append(temp)

	result = sorted(result, key=lambda tup: tup[1])[::-1]
	return result

def intersection(query_string,index):
	
	print "running intersection"
	query = preprocess(query_string,index['info']['stemmer'],index['info']['lemmatization'] , index['info']['remove_stopwords'] , index['info']['stopwords'])
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

	result = []
	for doc in index['indexed_docs']:
		if doc in a:
			result += [[doc , 1]]
		else:
			result += [[doc , 0]]

	## Sort Results by score
	result = sorted(result, key=lambda tup: tup[1])[::-1]
	return result

