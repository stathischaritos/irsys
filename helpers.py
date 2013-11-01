import pickle
from indexing import *
from query import *
from subprocess import call

def load_index(dir = "index.pkl"):
      if os.path.exists(dir):
            pkl_file = open(dir, 'rb')
            index = pickle.load(pkl_file)
            pkl_file.close()
      else:
            index = {}
            index['indexed_docs'] = {}
            index['tokens'] = {}
            
      return index 


def save_index(index):
      output = open('index.pkl', 'wb')
      pickle.dump(index, output)
      output.close()


def index(dir_or_file):
      index = load_index()

      if os.path.isfile(dir_or_file):
            print "Indexing Document '" + dir_or_file + "' ..."
            index_document(dir_or_file,index)
      elif os.path.isdir(dir_or_file):
            print "Indexing Directory '" + dir_or_file + "' ..."
            index_directory(dir_or_file, index)

      save_index(index)
      print "Done!"
      return index


def run_query(query_string , index):
      print "Running Query..."
      result = intersection(query_string , index)
      return result


def print_statistics(index , token = 'of'):
      total_tokens = 0
      for x in index['indexed_docs']:
            total_tokens += index['indexed_docs'][x]['length']

      unique_tokens = len(index['tokens'])

      token_counts = index['tokens'][token]['total_counts']

      print "Total Number of Tokens : "  , total_tokens
      print "Number of Unique Tokens : "  ,  unique_tokens
      print "Total Count of Token  '" + token + "' : " , token_counts


def evaluate(query,qid):
      index = load_index()
      result = run_query(query , index)
      rank = 1
      score = 1.0
      runID = 1

      ## Write res file of the query
      f = open('results/'+ str(qid) +".res",'wb')
      string = ""
      for doc in result:
            string += str(qid) + " Q0 " + doc +" "+ str(rank) + " " + str(score) + " " + str(runID) + "\n"
      f.write(string)
      f.close() 

      ##evaluation using terrier
      call(["./terrier/bin/trec_terrier.sh", "-e results/"+ str(qid) +".res"])

      f = open("results/"+ str(qid) +".eval",'r')
      evaluation= f.read()
      f.close()
      print evaluation


