from progressbar import ProgressBar
from preprocessing import *
import os

def index_directory(collection_directory , index):
      pbar = ProgressBar()

      if collection_directory[len(collection_directory)-1] != '/':
            collection_directory += '/'

      for root, dirs, files in os.walk(collection_directory):
          for file in pbar(files):
              if file.endswith(".txt"):
                  index_document(collection_directory + file, index)


      
def index_document(file,index):
      ## Open every file in the collection and read the text
      f = open(file,'r')
      raw_text = f.read()
      file = file.split('/')
      file = file[len(file)-1]
      ############## Preprocessing Steps here ##########################
      ## Result should be a list of tokens
      tokenized_text = preprocess(raw_text)
      ##################################################################

      ############## Indexing Steps here ###############################
      ## Result should be a posting list
      ## Do inner document counts - can run this in parallel.
      document = {}
      for term in tokenized_text:
            if term in document:
                  document[term] += 1
            else:
                  document[term] = 1

      ## Save document id and length
      doc_id = file[0:(len(file)-4)]


      if doc_id not in index['indexed_docs']:
            indexed_before  = False
            index['indexed_docs'][doc_id] = {}
            index['indexed_docs'][doc_id]["length"] = len(tokenized_text)
      else : 
            indexed_before = True

      ## Add counts to global index
      for word in document.iteritems():
            if word[0] not in index['tokens']:
                  index['tokens'][word[0]] = {}
                  index['tokens'][word[0]]['df'] = 1
                  index['tokens'][word[0]]['counts'] = {}
                  index['tokens'][word[0]]['total_counts'] = word[1]
            else:
                  if not indexed_before:
                        index['tokens'][word[0]]['df'] += 1
                        index['tokens'][word[0]]['total_counts'] += word[1]
                  else:
                        index['tokens'][word[0]]['total_counts'] -= index['tokens'][word[0]]['counts'][doc_id]
                        index['tokens'][word[0]]['total_counts'] +=word[1]


            index['tokens'][word[0]]['counts'][doc_id] = word[1]
      ##################################################################