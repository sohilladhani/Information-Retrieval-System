"""This module helps the user to query the corpus and fetch the relevant documents"""

import nltk
import unicodedata
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
import cPickle as pickle
import math
import difflib

#unpickle the pickled objects
print "loading necessary files.... please wait...."
post_dict = pickle.load(open('post_dict.pickle', 'rb'))
post_dict_df = pickle.load(open('post_dict_df.pickle', 'rb'))
word_freq_list = pickle.load(open('word_freq_list.pickle','rb'))
set_of_distinct_tokens = pickle.load(open('set_of_distinct_tokens.pickle','rb'))
dict_of_tf_norm_weight = pickle.load(open('dict_of_tf_norm_weight.pickle','rb'))
doc_ids = pickle.load(open('doc_ids.pickle','rb'))
print "files loaded!"


no_of_docs = len(doc_ids)
sw = set(stopwords.words("english"))	       #set of stop words
post_dict_keys = []

for key, value in post_dict.items():
    post_dict_keys.append(key)
    


def query_main():
    """This method is the main method through which the query is processed. It is divided into following parts:\n
    1. Tokenizing and stemming the query \n
    2. Calculating tf-raw and tf-weight \n
    3. Calculating idf \n
    4. Calculating normalized weight of the query tokens \n
    5. Calculating score of the document \n
    """
    j = 0
    while j<1:
        query_word_freq = dict()
        query_tf_weight = dict()
        query_idf = dict()
        query_weight = dict()
        query_norm_weight = dict()
        query_doc_score = dict()
        the_query = raw_input("Enter query: ")
        the_query = the_query.lower()
        tokens_ = CountVectorizer().build_tokenizer()(the_query)
        tokens = [word for word in tokens_ if word not in sw]
        
        #handling spelling mistakes entered in queries
        for w in tokens:
            if w not in post_dict_keys:
                tokens.extend(difflib.get_close_matches(w, post_dict_keys))
        
        stemmer = PorterStemmer()
        """Finding tf-raw for each token"""
        for w in tokens:
            stemmed = stemmer.stem(w)
            stemmed = stemmed.encode('utf8')
            if stemmed not in query_word_freq:
                query_word_freq[stemmed] = 1
            else:
                query_word_freq[stemmed] += 1
        
        square_sum = 0.0
        """Calculating tf-weight and idf of each token and calculating resulting weight (tf * idf)"""
        for stemmed,value in query_word_freq.items():
            query_tf_weight[stemmed] = 1 + math.log10(value)
            try:
                query_idf[stemmed] = math.log10(no_of_docs/post_dict_df[stemmed])
            except:
                continue
            query_weight[stemmed] = query_tf_weight[stemmed] * query_idf[stemmed]
            square_sum += query_weight[stemmed] * query_weight[stemmed]
        
        square_sum_root = math.sqrt(square_sum)
        """Calculating normalized weight of each token"""
        if square_sum_root == 0:
            print "Seems like the word you entered is present in most of the documents of corpus. Try something else"
            j = 0
            continue
        for stemmed,value in query_weight.items():
            query_norm_weight[stemmed] = value / square_sum_root
            
        print "Fetching documents for keywords: "
        for w in query_norm_weight.keys():
            print w,
        print "\n"
        
        
        """Calculating score of each document"""
        for key, value in dict_of_tf_norm_weight.items():
            score_temp = 0.0
            for stemmed,val in query_norm_weight.items():
                try:
                    score_temp += value[stemmed] * val 
                except:
                    score_temp += 0
            query_doc_score[key] = score_temp
        
        
        """Storing the results based on decreasing order of scores of the documents obtained in the previous step"""
        sorted_query_doc_score = []
        no_of_docs_found = 0
        for w in sorted(query_doc_score, key=query_doc_score.get, reverse=True):
            if query_doc_score[w] != 0.0:
                sorted_query_doc_score.append(w)
                no_of_docs_found += 1
        
        k = 0
        print "Number of documents found: ", no_of_docs_found
        for w in sorted_query_doc_score:
            k+=1
            #print w, query_doc_score[w]
            print w
            if k==10:
                k=0
                ans = raw_input("More? (y/n): ")
                if ans.lower()=='y':
                    continue
                else:
                    break
        
        
        cont = raw_input("Continue? (y/n): ")
        if cont.lower()=='y':
            j=0
        else:
            break
    
    
query_main()
        