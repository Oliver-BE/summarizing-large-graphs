import sys
# run by doing python fixundirected oldfile.txt > newfile.txt
"""
with open(sys.argv[1], "rt") as infile:
    edges = set()
    for line in infile:
        edge = frozenset(line.split()) 
        if edge not in edges:
            edges.add(edge)
            line = " ".join(line.split())
            sys.stdout.write(line)
            sys.stdout.write("\n")
        # else:
        #     sys.stderr.write(f"Repeated: {line}")
"""

def createAdjMatrix (fileName):
    f = open(fileName, 'r')
    graph = {}
    n = 0
    for i in f.readlines():
        nodes = i.split(" ")
        n1 = int(nodes[0])
        n2 = int(nodes[1])
        if n < n1 and n1 > n2:
            n = n1
        if n < n2 and n2 > n1:
            n = n2
        if n1 not in list(graph):
            graph[n1] = []
        adjacencyList = graph[n1]
        adjacencyList.append(n2)
        graph[n1] = adjacencyList
        if n2 not in list(graph):
            graph[n2] = []
        adjacencyList2 = graph[n2]
        adjacencyList2.append(n1)

    adjacencyMatrix = []
    for i in range(1,n+1):
        row = []
        for j in range(1,n+1):
            if i in list(graph) and j in graph[i]:
                row.append(1)
            else:
                row.append(0)
        adjacencyMatrix.append(row)

    for i in range(n):
        row = ""
        for j in range(n):
            row += str(adjacencyMatrix[i][j])+" "

        print(row)

graph = 'testgraph.txt'
createAdjMatrix(graph)