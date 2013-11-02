import nltk

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
