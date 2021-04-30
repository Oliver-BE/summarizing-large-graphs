# scratch file to implement graph classifications
import numpy as np
from collections import deque

def getDegree(node, A, V):
    """
    degree = 0
    for neighbor in A[:][node]:
        if neighbor in V:
            print(neighbor)
            print(V)
            if neighbor != node and A[neighbor][node] == 1:
                degree += 1
    return degree

    """
    degree = 0
    for neighbor in V:
        if neighbor != node and A[neighbor][node] == 1:
            degree += 1
    return degree
    

def isChain(V, A):
    #first check is if all nodes have two neighbors except two (Which have one)
    oneCount = 0 
    startVertex = 0
    endVertex = 0 
    for vertex in V:
         
        if getDegree(vertex, A, V) == 1:
            oneCount+=1
            if startVertex == 0: 
                startVertex = vertex
            else:
                endVertex = vertex 
        elif getDegree(vertex,A, V)!=2:
            return False

    if oneCount != 2:
        return False
    
#next go through from startVertex and see if you get to endVertex
    visited = []
    testV = startVertex
    while testV != endVertex:
        currentV = testV
        for neighbor in V:
             if A[testV][neighbor] == 1 and neighbor not in visited:
                visited.append(testV)
                testV = neighbor
                break
        
        if testV==currentV:
            return False
            
    return True
    
    


def isStar(V, A):
    # Identify single hub; make sure every other vertex has degree 1
    hubCount = 0
    for vertex in V:
        if getDegree(vertex, A, V) == len(V) - 1:
            hubCount += 1
        elif getDegree(vertex, A, V) != 1:
            return False
    
    if hubCount == 1:
        return True
    else:
        return False
            

def isClique(V, A):
    """
    Args:
      V is a list of vertices that form a subgraph.
      A is the adjacency matrix for the entire graph (which contains V).
    Returns:
      True if the list of vertices form a clique, false if not.
    """
    # go through the entire list of vertices and make sure each has a match
    for vertex in V:
        for vertex_2 in V:
            if vertex != vertex_2 and A[vertex][vertex_2] != 1:
                return False
    
    return True    

# Test Graph 
test_A = np.array([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]], dtype=np.int32)
np.set_printoptions(threshold=np.inf)

print(test_A)
test_V = [3, 1, 2, 0]

test_B = np.array([[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]])
test_Star = [1, 0, 2]
test_Chain = [0, 1, 2]

# true 
print(isClique(test_V, test_A))
print(isStar(test_Star, test_B))
print(isChain(test_Chain, test_B))

def isBipartiteCore(V, A):
    """
    Adapted from the pseduocode here: https://www.baeldung.com/cs/graphs-bipartite
    Args:
      V is a list of vertices that form a subgraph.
      A is the adjacency matrix for the entire graph (which contains V).
    Returns:
      True if the list of vertices form a bipartite core, false if not.
    """
    """
    queue = deque() 
    A = set()
    B = set()

    # arbitrarily choose start node as first node in subgraph and add to A
    start_node = V[0]
    A.add(start_node)
    queue.append(start_node) 
    
    # while queue not empty
    while len(queue) > 0:
        n1 = queue.popleft()
        # go through all vertices and find all neighbors of first vertex in queue
        for vertex in V:
            # if vertex is a neighbor 
            if A[n1][vertex] == 1:
                # then add the vertex to the opposite set and add to queue
                if n1 in A:
                    B.add(vertex)
                    # queue.append(vertex)
                else:
                    A.add(vertex)
                    queue.append(vertex)
                # if n1 has a neighbor in the same set as it, then false
                if ((n1 in A) and (vertex in A)) or ((n1 in B) and (vertex in B)):
                    return False
    
    # if we make it through the entire queue, return true
    return True
    """

test_V_bc = [3, 1, 2, 0, 4]
test_A_bc = np.array([[1, 0, 1, 1, 1], [0, 1, 1, 1, 1], [1, 1, 1, 0, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 1]], dtype=np.int32)

print("bipartite:")
print(isBipartiteCore(test_V_bc, test_A_bc))

            
                 

