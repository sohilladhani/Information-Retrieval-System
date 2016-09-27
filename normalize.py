"""This module helps to calculate normalized vectors of each document based on the inverted indexes"""

import cPickle as pickle
import math

print "Calculating normalized vectors... Please wait..."
word_freq_list = pickle.load(open('word_freq_list.pickle','rb'))
doc_ids = pickle.load(open('doc_ids.pickle','rb'))


def calculate_normalized_vectors():
	"""This method calculates the normalized vectors of each document in the corpus"""
	#tf-idf calculation for each document and normalize
	dict_of_tf_norm_weight = dict()					#list of dictionary of normalized weight of each token
	for i in range(0,len(word_freq_list)):		
		tf_weight = dict()						#term-frequency for each token. key = token; value = (1+log10(frequency)) of that token in that doc
		tf_norm_weight = dict()					#normalized weight for each token. key = token; value = normalize wt of that token
		word_freq = word_freq_list[i]			#get word_freq dictionary from the list. key = token; value = freq of that token in that doc
		square_sum = 0	#square of weights
		#calculate weight of each token
		for key,value in word_freq.items():		
			wt = 1 + math.log10(value)
			tf_weight[key] = wt
			square_sum+=wt*wt
		
		square_sum_root = math.sqrt(square_sum)	#square root of weights of each token
		
		for key,value in tf_weight.items():
			tf_norm_weight[key] = tf_weight[key] / square_sum_root	#find normalized weights
		
		dict_of_tf_norm_weight[doc_ids[i]] = tf_norm_weight	#add to the list of normalized weights
	
	pickle.dump(dict_of_tf_norm_weight, open('dict_of_tf_norm_weight.pickle','wb'))
	
calculate_normalized_vectors()
print "Done!"