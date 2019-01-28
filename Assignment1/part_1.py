#!/
# usr/bin/env python3

'''
Title: part_1.py
Date: January 28th, 2019
Authors: Luke Rowe, Luod Dai
Version: Final

This program loops through the database to find similar 
questions in a database of questions with Jaccard similarity >= 0.6. The results are
outputted into a tsv file, question_sim_4k.tsv.
'''

import re
import csv

'''
Compute the jaccard similarity between two questions

parameter(s): line1: list: first list being compared
			  line2: list: second list being compared
return: float: the float value of the jaccard similarity of two lists
'''
def jaccard(line1, line2):
	intersection = len(list(set(line1).intersection(set(line2))))
	
	union = (len(set(line1))+len(set(line2))) - intersection
	
	return float(intersection)/union

'''
parse the words from lines read to individual words for comparison
parameter(s): lines: list: the lines read from the tsv file
			  questions: list: the list for the parsed words
return: questions: list: updated list of parsed words
'''
def parse_words(lines ,questions):
	#counter for the lines
	lineCount = 0
	#confirm qids and questions exist, then parse the words
	for line in lines:
		if (len(line.split('\t')) == 2) and line.split('\t')[0].isdigit():
			(qid, question) = line.split('\t')
			
			#questions contains pairs: qid and a list of words
			questions.append([])
			questions[lineCount].append(qid)
			
			words = []  
			for word in question.split(' '):
				words.append(word)
			questions[lineCount].append(words)
			lineCount += 1
	
	return questions

def main():
	lines = [line.rstrip('\n') for line in open('./question_4k.tsv', encoding = 'utf8')]
	questions = []
	#parse lines so questions has individual words
	questions = parse_words(lines,questions)

	#table with qids and corresponding similar ids
	simids = []
	idcount = 0

	#writing the results to tsv file
	output = open('./question_sim_4k.tsv', "w")
	output.write("qid" + '\t' + "similar-qids\n")
	tsv_writer = csv.writer(output, delimiter=',')
	
	for (qid1,line1) in questions:
		output.write(qid1 + '\t')
		simids.append([])
		for (qid2,line2) in questions:
			if (jaccard(line1, line2) >= 0.6) and (qid2 != qid1):
				simids[idcount].append(qid2)
		tsv_writer.writerow(simids[idcount])
		idcount += 1

	output.close()

main()
