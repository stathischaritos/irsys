from django.shortcuts import render_to_response
from functions import *


def home(request):


	d = {}
	#title = request.GET
	option = "first_page"

	if "query" in request.GET:
		query = request.GET["query"]
		option = "query"
	elif "qid" in request.GET:
		qid = int(request.GET["qid"])
		if qid != 6 and qid !=7:
			option = "first_page"
		else:
			option = "predefined"


	if option == "first_page":
		title = "Welcome to IRSYS!"
		welcome_text = "IRSYS is end to end information retrieval system made for the course IR at the University of Amsterdam by Stathis, Jay and Johan. Input and run a Query on the top right corner to see some results!"
		d = {"start" : {"title" : title , "welcome_text" : welcome_text }}
	elif option == "predefined":
		predefined_queries = {
                        '6' : "sustainable ecosystems",
                        '7' : 'air guitar textile sensors'
                     }
		results = chart_results(qid)
		title = "Results for Predefined Query '" + predefined_queries[str(qid)] +"' :"
		d = {"results": {"title": title , "results" : results}}
	elif option=="query":
		index = load_index()
		results = run_query( query , index )
		results =  results[0:min(10,len(results))]
		title = "Top 10 results for query '" + query +"' :"
		d = {"qresults": {"title": title , "results" : results}}

	return render_to_response('home.html', d)