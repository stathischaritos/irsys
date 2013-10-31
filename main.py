#!/usr/bin/python
from functions import *
import sys


if len(sys.argv) < 3 or len(sys.argv) > 4 :
      print " Usage :  ./main.py -[index/query]  [ (document/directory) / query_string ]"
else:
      if sys.argv[1] == "-index":
            index,indexed_docs = index(sys.argv[2])
      elif sys.argv[1] == "-query":
            result = run_query(sys.argv[2])
            print result