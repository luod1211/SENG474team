import time
from collections import deque
import numpy as np

def preprocess(lines):
    # set of nodes in the link structure
    nodes = {}
    #dictionary of lists where Np[i] is a list of nodes that link to i
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

    print("Stage 2")

    while len(q) != 0:
        i = q.popleft()
        # this condition bottlenecks the algorithm (linear search is BAD)
        if i not in dead_ends:
            dead_ends.add(i)
            for j in Np[i]:
                D[j] = D[j] - 1
                if D[j] == 0:
                    q.append(j)
    print("Stage 3")
    return dead_ends

def main():
    f = open("./web-Google.txt", "r")
    # list of lines of the input file
    lines = [line.rstrip('\n') for line in f]
    nodes, Nm, Np = preprocess(lines)

    print("Stage 1")
    print(find_dead_ends(nodes, Nm, Np))

if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(time.perf_counter() - t0)