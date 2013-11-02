import pickle
from subprocess import call
from pylab import *
from progressbar import ProgressBar
import os
import nltk


def index_directory(collection_directory , index ,  stemmer = 'porter' , lemmatization ="wordnet" , remove_stopwords = False):
      pbar = ProgressBar()

      if collection_directory[len(collection_directory)-1] != '/':
            collection_directory += '/'

      for root, dirs, files in os.walk(collection_directory):
          for file in pbar(files):
              if file.endswith(".txt"):
                  index_document(collection_directory + file, index , stemmer , lemmatization ,remove_stopwords)


      
def index_document(file,index , stemmer = 'porter' , lemmatization ="wordnet" , remove_stopwords = False):
      ## Open every file in the collection and read the text

      f = open(file,'r')
      raw_text = f.read()
      f.close()
      file = file.split('/')
      file = file[len(file)-1]
      ############## Preprocessing Steps here ##########################
      ## Result should be a list of tokens
      tokenized_text = preprocess(raw_text , stemmer , lemmatization , remove_stopwords)
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
def preprocess(text, stemmer = "porter" , lemmatization = "wordnet" , remove_stopwords = False):
    tokenised_text = nltk.word_tokenize(text)
      
      ##Lematisation
    if lemmatization == 'wordnet':
      tokenised_text = wordnet(tokenised_text)

    ## Stemming
    if stemmer == 'porter':
      tokenised_text = porter(tokenised_text)
    elif stemmer == 'lancaster' :
      tokenised_text = lancaster(tokenised_text)

    ##remove stopwords
    if remove_stopwords:
      tokenised_text = nltk_remove_stopwords(tokenised_text)


    return tokenised_text


def lancaster(tokenised_text):
      from nltk.stem.lancaster import LancasterStemmer

      st = LancasterStemmer()
      stemmed_tokens = []
      for token in tokenised_text:
            stemmed_tokens += [st.stem(token)]

      return stemmed_tokens

def porter(tokenised_text):
      from nltk.stem.porter import PorterStemmer

      st = PorterStemmer()
      stemmed_tokens = []
      for token in tokenised_text:
            stemmed_tokens += [st.stem(token)]

      return stemmed_tokens

def wordnet(tokenised_text):
      from nltk.stem.wordnet import WordNetLemmatizer
      lmtzr = WordNetLemmatizer()
      lemmas = []

      for token in tokenised_text:
            lemmas += [lmtzr.lemmatize(token)]

      return lemmas


def nltk_remove_stopwords(tokenised_text):
      stopwords = nltk.corpus.stopwords.words('english')
      return [w for w in tokenised_text if w.lower() not in stopwords]

def run_query(query_string , index , model='intersection'):
            print "Running Query..."
            result =[]
            if model =='intersection':
                  result = intersection(query_string , index)
            return result
      



def intersection(query_string,index):
      
      query = preprocess(query_string)
      a = []
      b = []
      i = 0
      
      query_clean = []
      for word in query:
          if word in index['tokens']:
            query_clean += [word]

      query = query_clean

      for word in query:
          if word in index['tokens']:
            if i == 0:
                  a = index['tokens'][word]['counts'].keys()
                  i = 1
            else:
                  b = index['tokens'][word]['counts'].keys()
                  a = list(set(a) & set(b))

      # for x in a:           
      #     doc = []
      #     for word in query:
      #           doc +=[word , index['tokens'][word]['counts'][x] ]
      result = []
      for doc in index['indexed_docs']:
            if doc in a:
                  result += [[doc , 1]]
            else:
                  result += [[doc , 0]]

      ## Sort Results by score
      result = sorted(result, key=lambda tup: tup[1])[::-1]
      return result


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
      evaluation= f.read()
      f.close()

      return chart_results(str(qid))
      
     ## return evaluation
      

def index(dir_or_file , stemmer = 'lancaster' , lemmatization = "wordnet" , remove_stopwords = False):
      index = load_index()

      if ( (index['info']['stemmer'] != stemmer ) or (index['info']['lemmatization'] != lemmatization) or (index['info']['remove_stopwords'] != remove_stopwords)  ) :
            index = {}
            index['indexed_docs'] = {}
            index['tokens'] = {}
            index['info'] = {}
            index['info']['stemmer'] = stemmer
            index['info']['lemmatization'] = lemmatization
            index['info']['remove_stopwords'] = remove_stopwords
      
      print "Settings :"
      print "Lemmatization :" + lemmatization
      print "Stemmer:" + stemmer
      print "Remove Stopwords :" + str(remove_stopwords)

      if os.path.isfile(dir_or_file):
            print "Indexing Document '" + dir_or_file + "' ..."
            index_document(dir_or_file,index , stemmer , lemmatization ,remove_stopwords)
      elif os.path.isdir(dir_or_file):
            print "Indexing Directory '" + dir_or_file + "' ..."
            index_directory(dir_or_file, index , stemmer , lemmatization ,remove_stopwords)

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
      ##ax1.legend(loc='best')
      ax2 = fig.add_subplot(1,2,2)
      ax2.plot(pprecx,pprecy ,color="blue", linewidth=2.5, linestyle="-" ,label="Precision at %")
      ##ax2.legend(loc='best')
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


     
