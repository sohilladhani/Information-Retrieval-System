"""This module generates tokens out of the documents and creates necessary data structures and also serialize those data structures. \nThis module ultimately creates the inverted indexes needed for further processing"""


import nltk
import unicodedata
import string
from nltk.corpus import brown
from nltk.corpus import abc
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
from nltk.stem.porter import *
from sklearn.feature_extraction.text import CountVectorizer
import cPickle as pickle
import math


#globals
corpus = 'brown/'
"""global dictionary: key = token; value = list of doc ids"""
post_dict = dict()
"""global dictionary: key = token; value = no of docs containing that token"""
post_dict_df = dict()
"""global list of dictionaries of each document: key = token; value = token frequency in each document"""
word_freq_list = []
"""global dictionary: key = docID; value = no. of tokens in that doc"""
doc_words = dict()
"""list of doc_ids"""
doc_ids = brown.fileids()
"""distinct tokens set"""
set_of_distinct_tokens = set()
"""set of stop words"""
sw = set(stopwords.words("english"))

print "Tokenizing..."

def tokenize_corpus():
	"""This method tokenizes the corpus. It first goes through every document of the corpus, then tokenize them and apply PorterStemmer to stem those tokens."""
	for doc_id in doc_ids:	#for each document
		"""dictionary: key = token; value = frequency of that token"""
		word_freq = dict()
		doc_path = nltk.data.find('corpora/' + corpus + doc_id)		#path of the document
		#print doc_path
		doc_content = open(doc_path,'rb').read()		#read the document content and save it as string
		doc_content = doc_content.lower()			#normalization: case-folding
		doc_content = unicode(doc_content, errors='ignore')	#reading as unicode
		tokens_ = CountVectorizer().build_tokenizer()(doc_content)	#tokenization
		#tokens = tokens_
		tokens = [word for word in tokens_ if word not in sw]	#remove stopwords from tokens
		stemmer = PorterStemmer()		#instance of Porter Stemmer
		for w in tokens:		#for each token
			stemmed = stemmer.stem(w)	#stem the token
			stemmed = stemmed.encode('utf8')	 #convert to utf-8
			if stemmed not in set_of_distinct_tokens:	#check if the stemmed token is not in the set of distinct tokens
				set_of_distinct_tokens.add(stemmed)		#add into set if not present
				post_dict[stemmed] = [doc_id]			#add token->docId_list to the global posting list
				post_dict_df[stemmed] = 1				#add token having no of docs as 1
				word_freq[stemmed] = 1					#set token's frequency to 1
			else:										#if token present
				if doc_id not in post_dict[stemmed]:		#if document is not already in the list of token
					post_dict[stemmed].append(doc_id)	#append doc_id to posting list of the token (to prevent duplicates)
					post_dict_df[stemmed]+=1				#add 1 to the no of docs
				if stemmed not in word_freq:				#if stemmed token comes first time in that document
					word_freq[stemmed] = 1				#set token's frequency to 1
				else:									#if token has already appeared in current document
					word_freq[stemmed]+=1				#increament frequency of that token
		word_freq_list.append(word_freq)					#append local frequency list to global frequency list
		doc_words[doc_id] = len(tokens)					#key = docID; value = no. of tokens - (future use)

tokenize_corpus()

print "Done tokenizing!"

def serialize_objects():
	"""This method serializes the necessary objects in the form of pickle files."""
	#serializing necessary objects
	pickle.dump(post_dict, open('post_dict.pickle','wb'))
	pickle.dump(post_dict_df, open('post_dict_df.pickle','wb'))
	pickle.dump(word_freq_list, open('word_freq_list.pickle','wb'))
	pickle.dump(set_of_distinct_tokens, open('set_of_distinct_tokens.pickle','wb'))
	pickle.dump(doc_ids, open('doc_ids.pickle','wb'))

print "Building indexes...."
serialize_objects()
print "Done building indexes..."

