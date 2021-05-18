import sys
import numpy as np
import math

def createAdjMatrix (fileName):
    """
    Code from StackOverflow https://stackoverflow.com/questions/47663030/how-to-convert-text-file-to-adjancency-matrix-in-python
    Reads in a file and returns the resulting adjacency matrix as a numpy list of lists.
    """
    print(f"Reading in {fileName}...")
    f = open(fileName, 'r') 
    graph = {}
    # max number of nodes
    n = 0 
    line_num = 0
    for i in f.readlines():
        if line_num % 7500 == 0:
            print(".", end="", flush=True)
        nodes = " ".join(i.split())
        nodes = nodes.split(" ") 
        n1 = int(nodes[0])
        n2 = int(nodes[1])
        n = max(n, n1, n2) 
        if n1 not in list(graph):
            graph[n1] = []
        adjacencyList = graph[n1]
        adjacencyList.append(n2)
        graph[n1] = adjacencyList
        if n2 not in list(graph):
            graph[n2] = []
        adjacencyList2 = graph[n2]
        adjacencyList2.append(n1)
        line_num += 1
    
    print(f"\nDone reading in {fileName}, creating adjacency matrix A...")
    # num cells in overall adjacency matrix
    num_cells = n * n
    five_percent = math.floor(num_cells * 0.05) 
    cell_num = 0

    adjacencyMatrix = []
    for i in range(n + 1):
        row = [] 
        for j in range(n + 1):
            cell_num += 1
            if cell_num % five_percent == 0:
                print(".", end="", flush=True)
            if i in graph and j in graph[i]:
                # check for self loop
                if i == j:   
                    row.append(0)
                else:
                    row.append(1)
            else:
                row.append(0)
        adjacencyMatrix.append(row)

    print("\nAdjacency matrix generated")
    adjacencyMatrix = np.asarray(adjacencyMatrix, dtype=np.int32) 
    return adjacencyMatrix