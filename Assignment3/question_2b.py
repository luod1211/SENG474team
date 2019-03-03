'''
Assignment 3 Programming SENG 474
File: question_2b.py
Authors: Luke Rowe, Luo Dai
Version: Final

This program runs the page rank algorithm on a dataset of 800000 nodes
'''


import time
from collections import deque
import numpy as np

# number used to avoid division by 0
SMALL_NUM = 0.0001

'''
This function prepares data structures to hold data about the link structure 
without dead ends removed.

param(s): lines: list: list of lines from the input file
ret:    nodes: set: set of nodes in the original link structure
        edges: set of tuples: set of ordered tuples (from_node,to_node) containing the 
        edges in the link structure
        Np: dict: dictionary indexed by node_id containing the node_id's of the nodes
        that link to the node_id of the key
        Nm: dict: dictionary indexed by node_id containing the node_id's of the nodes
        that the key links to
'''
def preprocess(lines):
    # set of nodes in the link structure
    nodes = set()
    edges = set()
    #dictionary of lists where Np[i] is a list of nodes that link to i
    Np = {}
    # dictionary of lists where N-[i] is a list of nodes that i links to
    Nm = {}

    for i in lines[4:]:
        if len(i.split('\t')) == 2:
            # convert from tuple of strings to tuple of ints
            (from_node, to_node) = tuple(map(int, i.split('\t')))
            edges.add((from_node, to_node))

            # append from_node to N^+[to_node]
            if to_node in Np.keys():
                Np[to_node].add(from_node)
            else:
                Np[to_node] = set([from_node])

            # append to_node to N^-[from_node]
            if from_node in Nm.keys():
                Nm[from_node].add(to_node)
            else:
                Nm[from_node] = set([to_node])

    # take the union of the keys in the Nm and Np dictionary
    # to get the set of nodes
    nodes = set(Np).union(set(Nm))
    for i in set(Np).difference(set(Nm)):
        Nm[i] = set([])
    for i in set(Nm).difference(set(Np)):
        Np[i] = set([])

    return nodes, edges, Nm, Np

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

'''
This function removes dead_ends from the data structures containing the graph

param(s): nodes: set: set of nodes in the original graph
          edges: set of tuples: set of ordered tuples (from_node,to_node) containing the 
          edges in the original graph
          dead_ends: set: set of dead end nodes in the graph
ret: nodes: set: set of nodes in the updated graph
     edges: set of tuples: set of ordered tuples (from_node,to_node) containing the 
     edges in the updated graph
     Np: dict: dictionary indexed by node_id containing the node_id's of the nodes
     that link to the node_id of the key in the updated graph
     Nm: dict: dictionary indexed by node_id containing the node_id's of the nodes
     that the key links to in the updated graph
'''
def update_graph(nodes, edges, dead_ends):
    # Nm, Np for graph without dead_ends
    Nm = {}
    Np = {}

    # remove the dead ends from the graph
    nodes.difference_update(dead_ends)

    # make copy of edges to iterate through
    edges_copy = edges.copy()

    # remove edges containing dead ends
    for (from_node, to_node) in edges_copy:
        if (to_node in dead_ends) or (from_node in dead_ends):
            edges.remove((from_node, to_node))

    # Nm and Np creates according to graph with no dead ends
    for (from_node, to_node) in edges:
        # append from_node to N^+[to_node]
        if to_node in Np.keys():
            Np[to_node].add(from_node)
        else:
            Np[to_node] = set([from_node])

        # append to_node to N^-[from_node]
        if from_node in Nm.keys():
            Nm[from_node].add(to_node)
        else:
            Nm[from_node] = set([to_node])

    # there may be nodes with no incoming edges that needs to be added to Np
    for i in set(Nm).difference(set(Np)):
        Np[i] = set([])

    # set the dead_end nodes to have no incoming or outgoing edges
    # so that we can compute pagerank scores of non_dead_end nodes and
    # still traverse through dead_end nodes
    for node in dead_ends:
        Np[node] = set([])
        Nm[node] = set([])

    return nodes, edges, Nm, Np

'''
This function computes and returns the page rank scores for nodes in the updated graph.

param(s): v: ndarray: array containing page rank scores for each node in original graph
          D: ndarray: array containing outdegrees for each node in the updated_graph
          find_array_idx: dict: maps a node_id to the array index corresponding to that node
          find_node_id: dict: maps an array index to the node_id corresponding to that index
          N_with_de: int: number of nodes with dead ends
          N: int:  number of nodes with dead_ends removed
ret: v: ndarray: arrray of updated pageranks scores (for non-dead_end nodes)
'''
def page_rank(v, D, Np, find_array_idx, find_node_id, N_with_de, N):
    beta = 0.85
    T = 10

    # T= 10 epochs
    for epoch in range(T):
        # copy previous pagerank vector
        v_before = v.copy()
        # vector containing term inside the summation (of pagerank equation)
        inside_sum = v_before / D;
        #update v element-wise (to save memory)
        for i in range(N_with_de):
            sum = 0
            #sum over the edges that links to node_id and sum the "inside_sum" term
            for node_id in Np[find_node_id[i]]:
                sum += inside_sum[find_array_idx[node_id]]

            v[i] = beta * sum + (1/N) * (1 - beta)

    return v

'''
This function computes and returns the page rank scores for the dead end nodes of the graph.

param(s): v: ndarray: array containing page rank scores for each node in original graph
          D_with_de: ndarray: array containing outdegrees for each node in the orig graph
          dead_ends : set: set of dead ends in the graph
          N_with_de: int number of nodes with dead ends
          find_array_idx: dict: maps a node_id to the array index corresponding to that node
ret: v: ndarray: arrray of updated pageranks scores (for dead_end nodes)       
'''
def page_rank_dead_ends(v, D_with_de, dead_ends, Np_with_de, find_array_idx):
    # assign dead_end page rank scores to 0 (as they were assigned arbitary values
    # in the computation of non_dead_end pagerank scores)
    for node in dead_ends:
        v[find_array_idx[node]] = 0

    # vector containing term inside the summation (of equation)
    inside_sum = v / D_with_de

    # compute page rank score in reverse removal order
    for node in reversed(list(dead_ends)):
        sum = 0
        for node_id in Np_with_de[node]:
            sum += inside_sum[find_array_idx[node_id]]
        v[find_array_idx[node]] = sum

        #make change to "inside_sum" array instead of recomputing entire array to save computation time
        inside_sum[find_array_idx[node]] = sum / D_with_de[find_array_idx[node]]

    return v


def main():
    f = open("./web-Google.txt", "r")
    output = open("./PR_800k.tsv", "w")
    # list of lines of the input file
    lines = [line.rstrip('\n') for line in f]
    # "with_de" means "with dead ends"
    nodes, edges, Nm_with_de, Np_with_de = preprocess(lines)

    # find the dead ends in the graph
    dead_ends = find_dead_ends(nodes, Nm_with_de, Np_with_de)

    # keep copy of the nodes with dead ends included
    nodes_with_de = nodes.copy()
    N_with_de = len(nodes_with_de)

    # remove the dead ends from the graph
    nodes, edges, Nm, Np = update_graph(nodes,edges,dead_ends)
    N = len(nodes)

    # we initialize all variables in one pass through nodes to save computation time
    #initial page rank score
    init_score = 1 / N
    #vector of page rank scores
    v  = np.zeros(N_with_de)
    # vector of out-degrees for graph without dead_end nodes
    D = np.zeros(N_with_de)
    # vector of out-degrees for original link structure
    D_with_de = np.zeros(N_with_de)
    # dictionary that maps node ids to its corresponding array index
    find_array_idx = {}
    # dictionary that maps array indexes to its corresponding node id
    find_node_id = {}

    i = 0
    for node in nodes_with_de:
        D[i] = len(Nm[node])
        # set from 0 to 0.0001 to avoid future division by zero
        if D[i] == 0: D[i] = SMALL_NUM
        D_with_de[i] = len(Nm_with_de[node])
        if D_with_de[i] == 0: D_with_de[i] = SMALL_NUM

        v[i] = float(init_score)

        # assign array index/node_id mappings
        find_array_idx[node] = i
        find_node_id[i] = node
        i += 1

    # compute page-rank scores for all the non-dead_end nodes
    v = page_rank(v, D, Np, find_array_idx, find_node_id, N_with_de, N)
    v = page_rank_dead_ends(v, D_with_de, dead_ends, Np_with_de, find_array_idx)

    output_list = [None]*N_with_de
    i = 0
    for node_id in nodes_with_de:
        output_list[i] = (node_id, v[find_array_idx[node_id]])
        i+=1

    #list of nodes,pagerank score in descending order by pagerank score
    output_list = sorted(output_list, key=lambda x: x[1], reverse=True)

    #write to tsv file
    output.write("PageRank" + "\t" + "Ids\n")
    for i in range(N_with_de):
        output.write(str(output_list[i][1]) + "\t" + str(output_list[i][0]) + "\n")

if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(time.perf_counter() - t0)