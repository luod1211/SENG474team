'''
Title: question_1.py
Date: March 3rd, 2019
Authors: Luke Rowe, Luo Dai
Version: Final

This program finds all the "dead ends" in a dataset(nodes with no outgoing edges
or all outgoing edges are dead ends), then out puts the final dead ends in a file
'''

import time
from collections import deque
import numpy as np

'''
This function extracts the data from the lines of the txt file and create the sets for nodes, outgoing and incoming edges

param(s): lines: list: list of lines(strings) from the txt files
ret: nodes: all the nodes in the dataset
     Np: incoming edges for each node
     Nm: outgoing edges for each node
'''


def preprocess(lines):
    # set of nodes in the link structure
    nodes = {}
    # dictionary of lists where Np[i] is a list of nodes that link to i
    Np = {}
    # dictionary of lists where N-[i] is a list of nodes that i links to
    Nm = {}

    for i in lines[4:]:
        if len(i.split('\t')) == 2:
            (from_node, to_node) = i.split('\t')
            from_node = int(from_node)
            to_node = int(to_node)

            # append from_node to N^+[to_node]
            if to_node in Np.keys():
                Np[to_node].append(from_node)
            else:
                Np[to_node] = [from_node]

            # append to_node to N^-[from_node]
            if from_node in Nm.keys():
                Nm[from_node].append(to_node)
            else:
                Nm[from_node] = [to_node]

    # take the union of the keys in the Nm and Np dictionary
    # to get the set of nodes
    nodes = set(Np).union(set(Nm))
    for i in set(Np).difference(set(Nm)):
        Nm[i] = []
    for i in set(Nm).difference(set(Np)):
        Np[i] = []

    return nodes, Nm, Np


'''
This function takes in the set of nodes and connecting edges, and find all the dead ends in the data

param(s): nodes: all the nodes in the dataset
          Np: incoming edges for each node
          Nm: outgoing edges for each node
ret: dead_ends: the node ids of all the dead ends in the data
'''


def find_dead_ends(nodes, Nm, Np):
    # dictionary of out-degrees
    D = {}
    # queue of temporary dead ends
    q = deque([])

    # find out-degree of each node
    for node in nodes:
        D[node] = len(Nm[node])
        if D[node] == 0:
            q.append(node)
    dead_ends = set()

    while len(q) != 0:
        i = q.popleft()
        # this condition bottlenecks the algorithm (linear search is BAD)
        if i not in dead_ends:
            dead_ends.add(i)
            for j in Np[i]:
                D[j] = D[j] - 1
                if D[j] == 0:
                    q.append(j)

    return dead_ends


'''
main function to start the program
'''


def main():
    t0 = time.perf_counter()
    f = open("./web-Google_10k.txt", "r")
    # list of lines of the input file
    lines = [line.rstrip('\n') for line in f]
    nodes, Nm, Np = preprocess(lines)

    output = open("./deadends_10k.tsv", "w")
    output.write(str(find_dead_ends(nodes, Nm, Np)))
    print(time.perf_counter() - t0)

    t0 = time.perf_counter()
    f = open("./web-Google.txt", "r")
    # list of lines of the input file
    lines = [line.rstrip('\n') for line in f]
    nodes, Nm, Np = preprocess(lines)

    output = open("./deadends_800k.tsv", "w")
    output.write(str(find_dead_ends(nodes, Nm, Np)))
    print(time.perf_counter() - t0)


if __name__ == "__main__":
    main()
