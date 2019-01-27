#!/
# usr/bin/env python3

from typing import Dict, List
from fnv import *
import uuid
import numpy as np

LARGE_PRIME = 15373875993579943603
RANDOM_NUM_DICT = {} #6*14*2 random numbers for the hash functions
hash_tables = {}
B = 14
R = 6

def random_number():
    rand64 = uuid.uuid4().int & (1 << 64) - 1
    return rand64


def build_hash_sig(sig_num, words):
    hash_sig = tuple([get_min_hash(sig_num, j, words) for j in range(R)])
    #hash_sig = (1,2,3,4,5,6)
    return hash_sig

def get_min_hash(sig_num, min_hash_num, words):
    hash_codes= []

    a = RANDOM_NUM_DICT[(sig_num,min_hash_num,'a')]
    b = RANDOM_NUM_DICT[(sig_num,min_hash_num,'b')]


    #print("Words: ", words)
    for word in words:
        #print("Words: ", words)
        #word_encode = word.encode('utf-8')
        # fuse the nv.fnv_1a algorithm to hash a string to a 64-bit number
        #word_64 = hash(word_encode, bits=64)

        hash_code = (a * word + b) % LARGE_PRIME
        #hash_code = 10
        hash_codes.append(hash_code)

    return min(hash_codes)

def build_hash_tables(questions_as_words):
    for j in range(B):
        #This is like parsing through each questions
        for (qid, words) in questions_as_words:
            words_64 = []
            for word in words:
                word_encode = word.encode('utf-8')
                word_64 = hash(word_encode, bits=64)
                words_64.append(word_64)

            h_j = build_hash_sig(j, words_64)

            if h_j not in hash_tables[j].keys():
                hash_tables[j][h_j] = [int(qid)]

            else:
                hash_tables[j][h_j].append(int(qid))
                #print("Hello!")


            if(int(qid) % 1000 == 0 or int(qid) % 1000 == 1):
                print(qid)


def main():
    f = open('./question_150k.tsv', encoding='utf8')

    #make ditionary of random values for the 14*6 hash functions used in this algorithm
    for i in range(B):
        for j in range(R):
            RANDOM_NUM_DICT[(i, j,'a')] = random_number()
            RANDOM_NUM_DICT[(i, j, 'b')] = random_number()

    #create nested dictionary of 14 hash tables
    for i in range(B):
        hash_tables[i] = {}

    print("Hash Tables: ", hash_tables)

    #list of lines with the end "\n" stripped off
    lines = [line.rstrip('\n') for line in f]

    questions_as_words = []

    # questions start on line 2
    for i in lines[1:]:
        if len(i.split('\t')) == 2:
            (qid, question) = i.split('\t')
            # express words in question as a set, to remove duplicates
            words = set(question.strip().split(' '))
            questions_as_words.append((qid,words))

    build_hash_tables(questions_as_words)

    for j in range(B):
        for sig in hash_tables[j]:
            if len(hash_tables[j][sig]) >= 2:
                print(hash_tables[j][sig])

    #print("Final hash tables: ", hash_tables["hash_table_1"])

if __name__ == '__main__':
    main()

