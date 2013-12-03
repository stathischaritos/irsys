import pickle
from indexing import *
from query import *
from subprocess import call
from pylab import *



def load_index(dir = "/home/stathis/Projects/UVA_IR/index.pkl"):
      if os.path.exists(dir):
            pkl_file = open(dir, 'rb')
            index = pickle.load(pkl_file)
            pkl_file.close()
      else:
            index = {}
            index['indexed_docs'] = {}
            index['tokens'] = {}
            index['info'] = {}
            index['info']['stemmer'] = " "
            index['info']['lemmatization'] = " "
            index['info']['remove_stopwords'] = False
                        
      return index 


def save_index(index):
      output = open('/home/stathis/Projects/UVA_IR/index.pkl', 'wb')
      pickle.dump(index, output)
      output.close()


def print_statistics(index , token = 'of'):
      total_tokens = 0
      for x in index['indexed_docs']:
            total_tokens += index['indexed_docs'][x]['length']

      unique_tokens = len(index['tokens'])

      token_counts = 0

      if token in index['tokens']:
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
      evaluation = f.read()
      f.close()

      #return chart_results(str(qid))
      
      return evaluation
      

def index(dir_or_file , stemmer = 'lancaster' , lemmatization = "wordnet" , remove_stopwords = False , stopwords = 'nltk'):
      index = load_index()
      if ( (index['info']['stemmer'] != stemmer ) or (index['info']['lemmatization'] != lemmatization) or (index['info']['remove_stopwords'] != remove_stopwords)  ) :
            index = {}
            index['indexed_docs'] = {}
            index['tokens'] = {}
            index['info'] = {}
            index['info']['stemmer'] = stemmer
            index['info']['lemmatization'] = lemmatization
            index['info']['remove_stopwords'] = remove_stopwords
            
      
      if 'stopwords' not in index['info']:
            index['info']['stopwords'] = load_stopwords(stopwords ,lemmatization , stemmer)

      print "Settings :"
      print "Lemmatization :" + lemmatization
      print "Stemmer:" + stemmer
      print "Remove Stopwords :" + str(remove_stopwords)

      if os.path.isfile(dir_or_file):
            print "Indexing Document '" + dir_or_file + "' ..."
            index_document(dir_or_file,index , stemmer , lemmatization ,remove_stopwords , index['info']['stopwords'])
      elif os.path.isdir(dir_or_file):
            print "Indexing Directory '" + dir_or_file + "' ..."
            index_directory(dir_or_file, index , stemmer , lemmatization ,remove_stopwords , index['info']['stopwords'])

      save_index(index)
      print "Done!"
      return index
      

def chart_results(qid):
      results = {}

      precx = []
      precy = []

      pprecx = []
      pprecy = []

      with open("/home/stathis/Projects/UVA_IR/results/"+ str(qid) +".eval",'r') as infile:
            i = 0
            for row in infile:
                  line = nltk.word_tokenize(row) 
                  if len(line) == 3 :
                        results[line[0]] = line[2];
                  elif len(line) == 5 :
                        if line[0] == 'Number':
                              results['NumberOfQueries'] = line[4];
                        else:
                              # results["P" + line[2]] = line[4];
                              precx += [line[2]]
                              precy += [line[4]]
                  elif len(line) == 6 :
                        # results["PP" + line[2]] = line[5];
                        pprecx += [line[2]] 
                        pprecy += [line[5]]

                  elif len(line) == 4 :
                        if line[0] == 'Relevant':
                              results['RelevantRetrieved'] = line[3];
                        else:
                              results[line[0]] = line[3]; 

      rcParams['figure.figsize'] = 7, 3

      # Make an example plot with two subplots...
      fig = figure()
      ax1 = fig.add_subplot(1,2,1)
      ax1.plot(precx,precy ,color="blue", linewidth=2.5, linestyle="-" ,label="Precision at")
      ax1.legend(loc='upper right')
      ax2 = fig.add_subplot(1,2,2)
      ax2.plot(pprecx,pprecy ,color="blue", linewidth=2.5, linestyle="-" ,label="Precision at %")
      ax2.legend(loc='upper right')
      fig.savefig("/home/stathis/Projects/UVA_IR/results/"+str(qid)+'.png' ,transparent=True)
      fig.savefig("/home/stathis/Projects/UVA_IR/irsysweb/query/static/"+str(qid)+'.png' ,transparent=True)
      results["path"] ="/static/"+str(qid)+'.png'
      return results
      # subplot(1,2,1)
      # plot(precx,precy ,color="blue", linewidth=2.5, linestyle="-" ,label="Precision at")
      # legend(loc='upper right')
      # subplot(1,2,2)
      # plot(pprecx,pprecy ,color="blue", linewidth=2.5, linestyle="-" ,label="Precision at %")
      # legend(loc='upper right')
      # show()


     
