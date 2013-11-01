import pickle
from indexing import *
from query import *

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


