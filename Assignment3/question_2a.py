import time
from collections import deque
import numpy as np

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

    print("stage -0.5")

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

    for i in set(Nm).difference(set(Np)):
        Np[i] = set([])

    print("stage 3")

    return nodes, edges, Nm, Np



def page_rank(nodes, Nm, Np):
    print()

def main():
    f = open("./web-Google.txt", "r")
    # list of lines of the input file
    lines = [line.rstrip('\n') for line in f]
    nodes, edges, Nm, Np = preprocess(lines)

    #print("Nm: ", Nm, "\nNp: ", Np)
    #print("edges before: ", edges)

    print("stage 0")

    dead_ends = find_dead_ends(nodes, Nm, Np)

    print("stage 1")

    nodes, edges, Nm, Np = update_graph(nodes,edges,dead_ends)

    #print("edges after: ", edges)
    #print("Nm after: ", Nm, "\nNp after: ", Np)

    # v[i] should be of the form [nodeid, pagerankscorenodeid]

    page_rank(nodes, Nm, Np)

if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(time.perf_counter() - t0)