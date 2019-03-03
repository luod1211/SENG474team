import time
from collections import deque
import numpy as np

# number used to avoid division by 0
SMALL_NUM = 0.0001

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
            # convert from tuple of strings to list of ints
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

    print("stage -1")

    # take the union of the keys in the Nm and Np dictionary
    # to get the set of nodes
    nodes = set(Np).union(set(Nm))
    for i in set(Np).difference(set(Nm)):
        Nm[i] = set([])
    for i in set(Nm).difference(set(Np)):
        Np[i] = set([])

    return nodes, edges, Nm, Np

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

    # we initialize dead_ends to a dictionary for fast tests for containment
    # and preservation of order (since python dictionaries are ordered (after 3.6))
    dead_ends = {}

    while len(q) != 0:
        i = q.popleft()
        # this condition bottlenecks the algorithm (linear search is BAD)
        if i not in dead_ends.keys():
            dead_ends[i] = None
            for j in Np[i]:
                D[j] = D[j] - 1
                if D[j] == 0:
                    q.append(j)

    # return the keys of the dead_ends in removal order
    return dead_ends.keys()

def update_graph(nodes, edges, dead_ends):
    Nm = {}
    Np = {}

    # remove the dead ends from the graph
    nodes.difference_update(dead_ends)

    # make copy of edges to iterate through
    edges_copy = edges.copy()

    for (from_node, to_node) in edges_copy:
        if (to_node in dead_ends) or (from_node in dead_ends):
            edges.remove((from_node, to_node))

    print("stage 2")

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

    # there may be nodes with no incoming edge that needs to be added to Np
    for i in set(Nm).difference(set(Np)):
        Np[i] = set([])

    # set dead_end nodes have no incoming, outgoing edges
    #so that we can compute pagerank scores of non_dead_end nodes and
    #still traverse through dead_end nodes
    for node in dead_ends:
        Np[node] = set([])
        Nm[node] = set([])

    print("stage 3")

    return nodes, edges, Nm, Np

def page_rank(v, D, Np, find_array_idx, find_node_id, N_with_de, N):
    beta = 0.85
    T = 10

    # T= 10 epochs
    for epoch in range(T):
        print("epoch: ", epoch)
        # copy previous pagerank vector
        v_before = v.copy()
        # vector containing term inside the summation (of equation)
        inside_sum = v_before / D;
        #update v element-wise (to save memory)
        for i in range(N_with_de):
            sum = 0
            #sum over the edges that links to node_id and sum the "inside_sum" term
            for node_id in Np[find_node_id[i]]:
                sum += inside_sum[find_array_idx[node_id]]

            v[i] = beta * sum + (1/N) * (1 - beta)

    return v

def page_rank_dead_ends(v, D_with_de, dead_ends, Np_with_de, find_array_idx):
    # assign dead_end page rank scores to 0 (as they were assigned arbitary values
    # in computation of non_dead_end page_rank scores
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
    f = open("./web-Google_10k.txt", "r")
    # list of lines of the input file
    lines = [line.rstrip('\n') for line in f]
    nodes, edges, Nm_with_de, Np_with_de = preprocess(lines)

    print("stage 0")

    # find the dead ends in the graph
    dead_ends = find_dead_ends(nodes, Nm_with_de, Np_with_de)
    print("stage 1")
    # keep copy of the nodes with dead ends included
    nodes_with_de = nodes.copy()
    N_with_de = len(nodes_with_de)

    # remove the dead ends from the graph
    nodes, edges, Nm, Np = update_graph(nodes,edges,dead_ends)
    N = len(nodes)

    # we initialize variables in one for loop to save computation time
    #initial page rank score
    init_score = 1 / N
    #vector of page rank scores
    v  = np.zeros(N_with_de)
    # vector of out-degrees for graph without dead_end nodes
    D = np.zeros(N_with_de)
    # vector of out-degrees for original link graph
    D_with_de = np.zeros(N_with_de)
    # dictionary that maps node ids to its corresponding array index
    find_array_idx = {}
    # dictionary that maps array indexes  to its corresponding node id
    find_node_id = {}

    i = 0
    for node in nodes_with_de:
        D[i] = len(Nm[node])
        # set from 0 to 0.0001 to avoid division by zero in the future
        if D[i] == 0: D[i] = SMALL_NUM
        D_with_de[i] = len(Nm_with_de[node])
        if D_with_de[i] == 0: D_with_de[i] = SMALL_NUM

        # set v to the initial scores
        v[i] = float(init_score)

        # assign array index/node_id mappings
        find_array_idx[node] = i
        find_node_id[i] = node
        i += 1

    # compute page-rank score for all the non-dead_end nodes
    v = page_rank(v, D, Np, find_array_idx, find_node_id, N_with_de, N)
    v = page_rank_dead_ends(v, D_with_de, dead_ends, Np_with_de, find_array_idx)

    # TO_DO: sort te page rank scores (USE INDEXING DICTIONARIES)
    v[::-1].sort()

    # TO_DO: output to tsv file
    print(v[0:10])


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(time.perf_counter() - t0)