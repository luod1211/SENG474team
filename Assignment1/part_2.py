#!/
# usr/bin/env python3

from typing import Dict, List
from fnv import *
import uuid

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

    return hash_sig

def get_min_hash(sig_num, min_hash_num, words):
    hash_codes= []

    a = RANDOM_NUM_DICT[(sig_num,min_hash_num,'a')]
    b = RANDOM_NUM_DICT[(sig_num,min_hash_num,'b')]

    for word in words:
        word_encode = word.encode('utf-8')
        # fuse the nv.fnv_1a algorithm to hash a string to a 64-bit number
        word_64 = hash(word_encode, bits=64)

        hash_code = (a * word_64 + b) % LARGE_PRIME

        hash_codes.append(hash_code)

    return min(hash_codes)

def build_hash_tables(questions_as_words):
    for j in range(B):
        #This is like parsing through each questions
        for (qid, words) in questions_as_words:
            h_j = build_hash_sig(j, words)

            if h_j not in hash_tables["hash_table_{}".format(j)].keys():
                hash_tables["hash_table_{}".format(j)][h_j] = [int(qid)]

            else:
                hash_tables["hash_table_{}".format(j)][h_j].append(int(qid))
                #print("Hello!")


            if(int(qid) % 50 == 0 or int(qid) % 50 == 1):
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
        hash_tables["hash_table_{}".format(i)] = {}

    print("Hash Tables: ", hash_tables)

    #list of lines with the end "\n" stripped off
    lines = [line.rstrip('\n') for line in f]

    questions_as_words = []

    # questions start on line 2
    for i in lines[1:1000]:
        if len(i.split('\t')) == 2:
            (qid, question) = i.split('\t')
            # express words in question as a set, to remove duplicates
            words = set(question.strip().split(' '))
            questions_as_words.append((qid,words))

    build_hash_tables(questions_as_words)

    #2print("Final hash tables: ", hash_tables["hash_table_1"])

if __name__ == '__main__':
    main()