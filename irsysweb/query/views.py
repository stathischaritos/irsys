from django.shortcuts import render_to_response



def home(request):
	import sys
	sys.path.insert(0, '/home/stathis/Projects/UVA_IR')
	from helpers import *
	d = {}
	#title = request.GET
	first_page = True

	if "query" in request.GET:
		query = request.GET["query"]
		first_page = False
	
	if first_page:
		title = "Welcome to IRSYS!"
		welcome_text = "IRSYS is end to end information retrieval system made for the course IR at the University of Amsterdam by Stathis, Jay and Johan. Input and run a Query on the top right corner to see some results!"
		d = {"start" : {"title" : title , "welcome_text" : welcome_text }}
	else:
		##results = evaluate("sustainable ecosystems",6)
		results = chart_results(6)
		title = "Results for Query : '" + "sustainable ecosystems" +"'"
		d = {"results": {"title": title , "results" : results}}
		graph_dir = ""

	return render_to_response('home.html', d)