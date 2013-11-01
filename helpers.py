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


def print_statistics(index , token = 'of'):
      total_tokens = 0
      for x in index['indexed_docs']:
            total_tokens += index['indexed_docs'][x]['length']

      unique_tokens = len(index['tokens'])

      token_counts = index['tokens'][token]['total_counts']

      print "Total Number of Tokens : "  , total_tokens
      print "Number of Unique Tokens : "  ,  unique_tokens
      print "Total Count of Token  '" + token + "' : " , token_counts


def evaluate(query,qid,model='intersection'):
      index = load_index()
      result = run_query(query , index , model)

      rank = 1
      score = 1.0
      runID = 1

      ## Write res file of the query
      f = open('/home/stathis/Projects/UVA_IR/results/'+ str(qid) +".res",'wb')
      string = ""
      i = 0
      for doc in result:
            i += 1
            string += str(qid) + " Q0 " + doc[0] +" "+ str(i) + " " + str(doc[1]) + " " + str(runID) + "\n"
      f.write(string)
      f.close() 

      ##evaluation using terrier
      call(["/home/stathis/Projects/UVA_IR/terrier/bin/trec_terrier.sh", "-e /home/stathis/Projects/UVA_IR/results/"+ str(qid) +".res"])

      f = open("/home/stathis/Projects/UVA_IR/results/"+ str(qid) +".eval",'r')
      evaluation= f.read()
      f.close()
      return evaluation
      


