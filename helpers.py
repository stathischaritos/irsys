
import pickle
from indexing import *
from query import *

def load_index(dir = "index.pkl"):
      if os.path.exists(dir):
            pkl_file = open(dir, 'rb')
            index = pickle.load(pkl_file)
            indexed_docs = pickle.load(pkl_file)
            pkl_file.close()
      else:
            index = {}
            indexed_docs = {}
      return index , indexed_docs


def save_index(index , indexed_docs):
      output = open('index.pkl', 'wb')
      pickle.dump(index, output)
      pickle.dump(indexed_docs, output)
      output.close()


def index(dir_or_file):
      index, indexed_docs = load_index()

      if os.path.isfile(dir_or_file):
            print "Indexing Document '" + dir_or_file + "' ..."
            index_document(dir_or_file,index,indexed_docs)
      elif os.path.isdir(dir_or_file):
            print "Indexing Directory '" + dir_or_file + "' ..."
            index_directory(dir_or_file, index, indexed_docs)

      save_index(index,indexed_docs)
      print "Done!"
      return index, indexed_docs


def run_query(query_string):
      print "Running Query..."
      index, indexed_docs = load_index()
      result = intersection(query_string , index)
      return result


