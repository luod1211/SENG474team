#!/
# usr/bin/env python3

from typing import Dict, List
from fnv import *
import uuid

LARGE_PRIME = 15373875993579943603
RANDOM_NUM_DICT = {}  # 6*14*2 random numbers for the hash functions
B = 14
R = 6


def random_number():
    rand64 = uuid.uuid4().int & (1 << 64) - 1
    return rand64


def generate_hash(a, b, word_64):
    return (a * word_64 + b) % LARGE_PRIME


def build_hash_sig(sig_num, words):
    hash_sig = tuple([get_min_hash(sig_num, j, words) for j in range(R)])

    return hash_sig


def get_min_hash(sig_num, min_hash_num, words):
    hash_codes = []

    a = RANDOM_NUM_DICT[(sig_num, min_hash_num, 'a')]
    b = RANDOM_NUM_DICT[(sig_num, min_hash_num, 'b')]

    for word in words:
        word_encode = word.encode('utf-8')
        # fuse the nv.fnv_1a algorithm to hash a string to a 64-bit number
        word_64 = hash(word_encode, bits=64)

        hash_codes.append(generate_hash(a, b, word_64))

    return min(hash_codes)


def main():
    f = open('./question_150k.tsv', encoding='utf8')

    # make ditionary of random values for the 14*6 hash functions used in this algorithm
    for i in range(B):
        for j in range(R):
            RANDOM_NUM_DICT[(i, j, 'a')] = random_number()
            RANDOM_NUM_DICT[(i, j, 'b')] = random_number()

    # initialize 14 hash tables
    '''
            IMPORTANT: THERE HAS TO BE A BETTER WAY TO DO THIS
    '''
    hash_tables = {}

    # create nested dictionary of 14 hash tables
    for i in range(B):
        hash_tables["hash_table_{}".format(i)] = {}

    print("Hash Tables: ", hash_tables)

    # list of lines with the end "\n" stripped off
    lines = [line.rstrip('\n') for line in f]

    # questions start on line 2
    for i in lines[1:10000]:
        if len(i.split('\t')) == 2:
            (qid, question) = i.split('\t')
            # express words in question as a set, to remove duplicates
            words = set(question.strip().split(' '))

            D = [build_hash_sig(j, words) for j in range(B)]

            if int(qid) % 500 == 1 or int(qid) % 500 == 0:
                print(D)
            '''
            COMPARE D (say D_1) for "question" to every other questions' D (say D_2).
            As long as D_1[i] = D_2[i] for some i, then they are considered "similar".

            To record this, we will create a new dictionary, say sim_dict, where we index into
            the dictionary by qid and the value of the dictionary are the questions similar to the 
            question with that qid.

            '''


if __name__ == '__main__':
    main()