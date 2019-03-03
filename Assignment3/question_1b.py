'''
Title: question_1b.py
Authors: Luke Rowe, Luo Dai
Version: Final

This program finds all the "dead ends" in the 800k dataset(nodes with no outgoing edges
or all outgoing edges point to dead ends), then outputs the dead ends in a file: deadends_800k.tsv
'''

import time
from collections import deque
import numpy as np

'''
This function extracts the data from the lines of the txt file and create the sets for nodes, outgoing and incoming edges

param(s): lines: list: list of lines(strings) from the txt files
ret: nodes: set: all the nodes in the dataset
     Np: dict: incoming edges for each node
     Nm: dict: outgoing edges for each node
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
This function finds and returns the dead ends in the link structure
param(s): nodes: set: the set of nodes in the original link structure
          Np: dict: dictionary indexed by node_id containing the node_id's of the nodes
          that link to the node_id of the key
          Nm: dict: dictionary indexed by node_id containing the node_id's of the nodes
          that the key links to 
ret: set: set of removed node_ids in removal order
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

    # we make dead_end a dictionary so that we have fast tests for containment
    # and preservation of order (since python dictionaries are insertion ordered (after 3.7))
    dead_ends = {}

    while len(q) != 0:
        i = q.popleft()
        if i not in dead_ends.keys():
            dead_ends[i] = None
            for j in Np[i]:
                D[j] = D[j] - 1
                if D[j] == 0:
                    q.append(j)

    # return the keys of the dead_ends in removal order
    return dead_ends.keys()

def main():
    t0 = time.perf_counter()
    f = open("./web-Google.txt", "r")
    # list of lines of the input file
    lines = [line.rstrip('\n') for line in f]
    nodes, Nm, Np = preprocess(lines)

    output = open("./deadends_800k.tsv", "w")
    dead_ends = find_dead_ends(nodes, Nm, Np)
    for node in dead_ends:
        output.write(str(node) + "\n")
    print(time.perf_counter() - t0)


if __name__ == "__main__":
    main()