
from indexing import *

def intersection(query_string,index):
	query = preprocess(query_string)
	intersection = {}
	first = {}
	i = 0
	for word in query:
	    if word in index:
	          for tf in index[word]['counts'].iteritems():
	                if i == 1 :
	                      if tf[0] in first:
	                            if tf[0] in intersection:
	                                  intersection[tf[0]] += [word , tf]
	                            else:
	                                  intersection[tf[0]] =[word , tf]
	                else:
	                      first[tf[0]] = [[word , tf]]
	          i = 1
	    else:
	          print "Word '" + word + "' not found!"
	    
	if len(intersection) == 0 :
	    intersection = first

	print "Boolean search returned " + str(len(intersection)) + " results!"
	print "Here is the top ten:"
	result = intersection.items()[0:min(10,len(intersection))]
	return result

