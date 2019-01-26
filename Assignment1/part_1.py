#!/
# usr/bin/env python3

from typing import Dict, List
from fnv import *
import uuid

def main():
    f = open('./question_4k.tsv', encoding='utf8')

    output = open('./question_sim_4k.tsv', "w")

    output.write("qid" + '\t' + "similar-qids\n")

    #list of lines with the end "\n" stripped off
    lines = [line.rstrip('\n') for line in f]

    #questions start on line 2
    for i in lines[1:]:

        if len(i.split('\t')) == 2:

            [qid_a,question_a] = i.split('\t')
            words_a = set(question_a.strip().split(' '))


            output.write(qid_a + '\t')
            result = ''
            for j in lines[1:]:

                if i is j:
                    continue

                if len(j.split('\t')) == 2:

                    [qid_b, question_b] = j.split('\t')
                    words_b = set(question_b.strip().split(' '))

                    sim = len(words_a.intersection(words_b)) / len(words_a.union(words_b))

                    if (sim >= 0.6):
                        result = result + qid_b + ','

            if result is not '':
                result = result.rstrip(",")

            if(int(qid_a) % 500 == 0) or (int(qid_a) % 500 == 1):
                print(qid_a)

            output.write(result + "\n")


    f.close()




        #    question_dict[int(i.split('\t')[0])] = i.split('\t')[1]

        #if i == lines[60]:
        #    print(question_dict)
            # returns 2 elements: id and the string corresponding to the id
            # then split by space to get the words in each line
            #words += i.split('\t')[1].split(' ') #(more Pythonic code)

    # calculate frequencies of words and store them inthe dictionary
    #words_freq = {}
    #for word in words:
     #   if word not in words_freq:
      #      words_freq[word] = 1

       # else: words_freq[word] += 1

    #print(words_freq['ways'])


def build_hash_table(line):
    hash_table = {}
    a_count = 0
    words_a = set(line.strip().split(' '))

    for word in words_a:
        a_count += 1
        #word = word.encode('utf-8')
        hash_table[word] = 0
    return (hash_table,a_count)


def random_number():
    rand64 = uuid.uuid4().int & (1 << 64) - 1
    return rand64

if __name__ == '__main__':
    main()