import nltk

def preprocess(text):
      processed_text = nltk.word_tokenize(text)
      return processed_text