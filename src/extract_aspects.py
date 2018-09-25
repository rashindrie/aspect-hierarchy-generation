#!/usr/bin/env python

"""
File for aspect extraction functions
"""
import numpy as np
import pickle
import sys
import nltk
#>>> nltk.download('averaged_perceptron_tagger')

from collections import Counter
from nltk.corpus import stopwords

from external.my_potts_tokenizer import MyPottsTokenizer

def get_sentences(review):
	"""
	INPUT: full text of a review
	OUTPUT: a list of sentences

	Given the text of a review, return a list of sentences. 
	"""

	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	
	if isinstance(review, str):
		return sent_detector.tokenize(review)
	else: 
		raise TypeError('Sentence tokenizer got type %s, expected string' % type(review))


def tokenize(sentence):
	"""
	INPUT: string (full sentence)
	OUTPUT: list of strings

	Given a sentence in string form, return 
	a tokenized list of lowercased words. 
	"""

	pt = MyPottsTokenizer(preserve_case=False)
	return pt.tokenize(sentence)


def pos_tag(toked_sentence):
	"""
	INPUT: list of strings
	OUTPUT: list of tuples

	Given a tokenized sentence, return 
	a list of tuples of form (token, POS)
	where POS is the part of speech of token
	"""
	return nltk.pos_tag(toked_sentence)


def pos_tag_stanford(toked_sentence):
	"""
	INPUT: list of strings
	OUTPUT: list of tuples

	Given a tokenized sentence, return 
	a list of tuples of form (token, POS)
	where POS is the part of speech of token
	"""

	from nltk.tag.stanford import POSTagger
	st = POSTagger('/Users/jeff/Zipfian/opinion-mining/references/resources/stanford-pos/stanford-postagger-2014-06-16/models/english-bidirectional-distsim.tagger', 
               '/Users/jeff/Zipfian/opinion-mining/references/resources/stanford-pos/stanford-postagger-2014-06-16/stanford-postagger.jar')

	return st.tag(toked_sentence)


def aspects_from_tagged_sents(tagged_sentences):
	"""
	INPUT: list of lists of strings
	OUTPUT: list of aspects

	Given a list of tokenized and pos_tagged sentences from reviews
	about a given restaurant, return the most common aspects
	"""

	STOPWORDS = set(stopwords.words('english'))

	# find the most common nouns in the sentences
	noun_counter = Counter()

	for sent in tagged_sentences:
		for word, pos in sent: 
			if pos=='NNP' or pos=='NN' and word not in STOPWORDS:
				noun_counter[word] += 1

	# list of tuples of form (noun, count)
	return [noun for noun, _ in noun_counter.most_common(20)]


def demo_aspect_extraction(): 
	"""
	Demo the aspect extraction functionality on one restaurant
	"""
	from main import read_data, get_reviews_for_business, extract_aspects

	file =  open('../data/reviews.txt', 'r') 
	reviews =  file.read()

	print "Extracting aspects..."
	aspects = extract_aspects(reviews)

	print "Aspects list:" 
	for i,aspect in enumerate(aspects):
		print aspect  

	with open('../data/aspect_list.bin', 'wb') as fp:
		pickle.dump(aspects,fp)

if __name__ == "__main__":
	demo_aspect_extraction()






