# Create your views here.
from django.http import HttpResponse
import sys
sys.path.insert(0, '/home/stathis/Projects/UVA_IR')
from helpers import *



def index(request):

	string = evaluate("sustainable ecosystems",6)
	return HttpResponse("<pre>" + str(string) + "</pre>")
