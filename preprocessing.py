import nltk
import re

def preprocess(text, stemmer = "porter" , lemmatization = "wordnet" , remove_stopwords = False , stopwords=[]):
	
	text = re.sub(r'\W+', ' ', text)
	text = text.lower()
	tokenised_text = nltk.word_tokenize(text)
	tokenised_text = normalize(tokenised_text,lemmatization,stemmer)
	##remove stopwords
	if remove_stopwords:
		tokenised_text = f_remove_stopwods(tokenised_text ,stopwords)
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

def load_stopwords(choice = 'nltk' ,lemmatization = 'wordnet' , stemmer = 'porter'):
	if choice == 'nltk':
		stopwords = nltk.corpus.stopwords.words('english')
	else:
		if choice=="small":
			file_string = "ensmall.stopwords"
		else :
			file_string = "en.stopwords"
		f = open(file_string,'r')
		raw_text = f.read()
		f.close()
		stopwords = nltk.word_tokenize(raw_text)
	print lemmatization , stemmer
	stopwords = normalize(stopwords,lemmatization,stemmer)
	return stopwords


def f_remove_stopwods(tokenised_text , stopwords):
	return [w for w in tokenised_text if w.lower() not in stopwords]



def normalize(tokenised_text , lemmatization = 'wordnet' , stemmer = 'porter'):
	##Lematisation
	if lemmatization == 'wordnet':
		tokenised_text = wordnet(tokenised_text)
	else:
		## Stemming
		if stemmer == 'porter':
			tokenised_text = porter(tokenised_text)
		elif stemmer == 'lancaster' :
			tokenised_text = lancaster(tokenised_text)
	return tokenised_text
