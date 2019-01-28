#!/
# usr/bin/env python3

'''
Title: part_2.py
Date: January 28th, 2019
Authors: Luke Rowe, Luod Dai
Version: Final

This program use the locality sensitive hashing technique to find similar_questions
questions in a database of questions with Jaccard similarity >= 0.6. The results are
outputted into a tsv file, __INSERT_NAME_HERE___

'''

from typing import Dict, List
from fnv import *
import uuid

B = 14
R = 6
LARGE_PRIME = 15373875993579943603

# 6*14*2 random numbers for the hash functions
RANDOM_NUM_DICT = {} 
hash_tables = {}

'''
This function generates and returns a random 64-bit integer

return: rand64: int: randomly generated 64-bit integer
'''
def random_number():
	rand64 = uuid.uuid4().int & (1 << 64) - 1
	return rand64

'''
This functions constructs and returns a size-6 minhash signature

paramater(s): table_num: int: an integer in [0,13] corresponding to one of the 14 hash tables
			  words_64: set: set of distinct 64-bit integers corresponding to the words in a given question
return: hash_sig: tuple: a tuple of 6 min-hashes (the min-hash signature)	
'''
def build_hash_sig(table_num, words_64):
	#retrieves 6 min hashes and stores the min-hashes into a tuple
	hash_sig = tuple([get_min_hash(table_num, j, words_64) for j in range(R)])
	return hash_sig

'''
This functions generates the min-hash for a particular question and for a particular hash table_num

paramater(s): table_num: int: an integer in [0,13] corresponding to one of the 14 hash tables
			  min_hash_num: int: an integer in [0,5] corresponding to the min-hash number in the signature
			  words: set: set of distinct 64-bit integers corresponding to the words in a given question
return: int: the min-hash
'''
def get_min_hash(table_num, min_hash_num, words_64):
	hash_codes= []
	
	#retrieve the random numbers corresponding to this hash table and min-hash number
	a = RANDOM_NUM_DICT[(table_num,min_hash_num,'a')]
	b = RANDOM_NUM_DICT[(table_num,min_hash_num,'b')]

	#generate hash codes for each word
	for word_64 in words_64:
		#linear hash function (ax+b)modp
		hash_code = (a * word_64 + b) % LARGE_PRIME
		hash_codes.append(hash_code)

	return min(hash_codes)

'''
This function constructs 14 hash tables of qids of similar questions indexed by min-hash signature

parameter(s): questions_as_words_64: dict: dictionary of set of fnv hashes for each questions indexed by qid
'''
def build_hash_tables(questions_as_words_64):
	for j in range(B):
		#This is like parsing through each question
		for qid in questions_as_words_64.keys():

			h_j = build_hash_sig(j, questions_as_words_64[qid])

			if h_j not in hash_tables[j].keys():
				hash_tables[j][h_j] = [str(qid)]

			else:
				hash_tables[j][h_j].append(str(qid))

'''
This function computes and returns the Jaccard similarity of 2 questions

parameter(s): questions_as_words: dict: dictionary of set of words for each question indexed by qid
			  qid: int qid of the first question
			  qid_2: int qid of the second question
return: jac_sim: float: jaccard similarity of question 1 and question 2
'''	
def compute_jac_sim(questions_as_words,qid,qid_2):
	first_set = set(questions_as_words[qid])
	second_set = set(questions_as_words[qid_2])
	jac_sim = len(first_set.intersection(second_set)) / len(first_set.union(second_set))
	
	return jac_sim

'''
This function finds the similarity of the questions in the database, and for each question, writes the 
questions with similarity >=0.6 to that question to a tsv file

parameter(s): questions_as_words: dict: dictionary of set of words for each question indexed by qid
			  questions_as_words_64: dict: dictionary of set of fnv hashes for each questions indexed by qid
			  output: file: output tsv file
'''
def find_sim(questions_as_words,questions_as_words_64,output):
	for qid in questions_as_words_64.keys():
		#set of qids of similar questions to the current questions
		similar_questions = set([])
		
		output.write(qid + '\t')

		#for each hash table, compute hash signature of current question and collect similar qids 
		for j in range(B):
			h_j = build_hash_sig(j,questions_as_words_64[qid])
			
			#we are not interested in length one values, since we are guaranteed that the
			#qid of the current question will be in the set of values for that hash signature
			if h_j in hash_tables[j].keys() and len(hash_tables[j][h_j]) >= 2 :
				similar_questions = similar_questions.union(set(hash_tables[j][h_j]))

		#create copy so we can iterate and remove redundant similar questions
		similar_questions_copy = similar_questions.copy()

		if len(similar_questions) != 0:
			#remove current question's qid from its set of similar qids
			similar_questions.remove(str(qid))

			#remove false positives
			for qid_2 in similar_questions_copy:
				jaccard_sim = compute_jac_sim(questions_as_words,qid,int(qid_2))
				if jaccard_sim < 0.6:
					similar_questions.remove(qid_2)

		sim_q_str = ','.join(similar_questions)

		'''TURN INTO FILE WRITE AFTER TESTING'''
		output.write(sim_q_str, "\n")

'''
This function preprocesses the lines in the input tsv file by building two dictionaries
indexed by qid: the first dictionary with sets of words as values, and the second dictionary
with sets of fnv hash codes of the words as values

parameter(s): lines: list: list of lines (strings) from the input tsv file
			  questions_as_words: dict: dictionary of set of words for each question indexed by qid
			  questions_as_words_64: dict: dictionary of set of fnv hashes for each questions indexed by qid
return: tuple: a tuple containing the processed input dictionaries
'''
def preprocess(lines,questions_as_words,questions_as_words_64):
	
	# questions start on line 2
	for i in lines[1:]:
		if len(i.split('\t')) == 2:
			(qid_0, question) = i.split('\t')
			# express words in question as a set, to remove duplicates
			words = set(question.strip().split(' '))
			questions_as_words[int(qid_0)] = words

	# convert words of each question into 64-bit integer using the fnv hash algorithm
	# as a preprocessing step, so that we only use the fnv algorithm once per database traversal
	for qid in questions_as_words.keys():
		words_64 = []
		for word in questions_as_words[qid]:
			word_encode = word.encode('utf-8')
			word_64 = hash(word_encode, bits=64)
			words_64.append(word_64)
		questions_as_words_64[int(qid)] = words_64

	return (questions_as_words, questions_as_words_64)

def main():
	f = open('./question_150k.tsv', encoding='utf8')
	output = open('./question_sim_150.tsv', "w")
	
	#header for tsv file
	output.write("qid" + '\t' + "similar-qids\n")

	#make ditionary of random values for the 14*6 hash functions used in this algorithm
	for i in range(B):
		for j in range(R):
			RANDOM_NUM_DICT[(i, j,'a')] = random_number()
			RANDOM_NUM_DICT[(i, j, 'b')] = random_number()

	#create 14 dictionaries corresponding to the 14 hash tables
	for i in range(B):
		hash_tables[i] = {}

	#dictionary containing questions' words as 64-bit integers (from fnv hash algorithm) indexed by qid
	questions_as_words_64 = {}
	# dictionary containing each questions' words indexed by qid
	questions_as_words = {}

	#list of lines with the end "\n" stripped off
	lines = [line.rstrip('\n') for line in f]
	
	#preprocess the lines so that we can efficiently build the hash tables
	(questions_as_words, questions_as_words_64) = preprocess(lines,questions_as_words,questions_as_words_64)
	#build hash tables and find similar questions for each question in the database
	build_hash_tables(questions_as_words_64)
	find_sim(questions_as_words,questions_as_words_64,output)
	
	f.close()
	output.close()

if __name__ == '__main__':
	main()
