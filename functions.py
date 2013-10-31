import nltk
import os
from progressbar import ProgressBar
import pickle

def preprocess(text):
      processed_text = nltk.word_tokenize(text)
      return processed_text

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


def index_directory(collection_directory = "collection/"):
      index , indexed_docs = load_index()
      pbar = ProgressBar()

      for root, dirs, files in os.walk(collection_directory):
          for file in pbar(files):
              if file.endswith(".txt"):
                  index_document(collection_directory + file, index, indexed_docs)
      save_index(index,indexed_docs)
      return index, indexed_docs

def index_document(file,index,indexed_docs):
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
      if doc_id not in indexed_docs:
            indexed_before  = False
            indexed_docs[doc_id] = {}
            indexed_docs[doc_id]["length"] = len(tokenized_text)
      else : 
            indexed_before = True

      ## Add counts to global index
      for word in document.iteritems():
            if word[0] not in index:
                  index[word[0]] = {}
                  index[word[0]]['df'] = 1
            else:
                  if not indexed_before:
                        index[word[0]]['df'] += 1

            index[word[0]][doc_id] = word[1]
      ##################################################################





