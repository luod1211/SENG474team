#!/
# usr/bin/env python3

from typing import Dict, List
from fnv import *
import uuid

LARGE_PRIME = 15373875993579943603
RANDOM_NUM_DICT = {} #6*14*2 random numbers for the hash functions
B = 6
S = 14

def random_number():
    rand64 = uuid.uuid4().int & (1 << 64) - 1
    return rand64

def generate_hash(a,b,word_64):

    return (a * word_64 + b) % LARGE_PRIME



def build_hash_sig(sig_num, question):
    hash_sig = tuple([get_min_hash(sig_num, j+1, question) for j in range(B)])

    return hash_sig

def get_min_hash(sig_num, min_hash_num, question):

    '''

    IMPORTANT: remember to splits words only ONCE per question
    '''


    #express words in question as a set, to remove duplicates
    words = set(question.strip().split(' '))
    hash_codes = []

    a = RANDOM_NUM_DICT[(sig_num,min_hash_num,'a')]
    b = RANDOM_NUM_DICT[(sig_num,min_hash_num,'b')]

    for word in words:
        word_encode = word.encode('utf-8')
        # fuse the nv.fnv_1a algorithm to hash a string to a 64-bit number
        word_64 = hash(word_encode, bits=64)

        hash_codes.append(generate_hash(a, b, word_64))

    return min(hash_codes)

def main():
    f = open('./question_150k.tsv', encoding='utf8')

    #make ditionary of random values for the 14*6 hash functions used in this algorithm
    for i in range(S):
        for j in range(B):
            RANDOM_NUM_DICT[(i + 1, j + 1,'a')] = random_number()
            RANDOM_NUM_DICT[(i + 1, j + 1, 'b')] = random_number()

    #print(RANDOM_NUM_DICT)

    #list of lines with the end "\n" stripped off
    lines = [line.rstrip('\n') for line in f]

    # questions start on line 2
    for i in lines[1:]:

        (qid, question) = i.split('\t')
        hash_sig = [build_hash_sig(j + 1, question) for j in range(S)]

        '''
        COMPARE hash_sig to every other questions' hash_signature.
        As long as >= 1 is equal, then their signatures are equal
        '''

if __name__ == '__main__':
    main()
