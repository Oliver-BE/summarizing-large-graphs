import numpy as np
from collections import deque

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
test_A = np.array([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], dtype=np.int32)
np.set_printoptions(threshold=np.inf)
print(test_A)
test_V = [3, 1, 2, 0, 4]

print(isClique(test_V, test_A))

def isBipartiteCore(V, A):
    """
    Adapted from the pseduocode here: https://www.baeldung.com/cs/graphs-bipartite
    Args:
      V is a list of vertices that form a subgraph.
      A is the adjacency matrix for the entire graph (which contains V).
    Returns:
      True if the list of vertices form a bipartite core, false if not.
    """
    queue = deque() 
    set_A = set()
    set_B = set()

    # arbitrarily choose start node as first node in subgraph and add to A
    start_node = V[0]
    set_A.add(start_node)
    queue.append(start_node) 
    
    # while queue not empty
    while len(queue) > 0:
        n1 = queue.popleft()
        # go through all vertices and find all neighbors of first vertex in queue
        for vertex in V:
            # if vertex is a neighbor and not itself
            if A[n1][vertex] == 1 and n1 != vertex:
                # if we already haven't added this neighbor
                if vertex not in set_A and vertex not in set_B:
                    # then add the vertex to the opposite set and add to queue
                    if n1 in set_A:
                        set_B.add(vertex)
                        queue.append(vertex)
                    elif n1 in set_B:
                        set_A.add(vertex)
                        queue.append(vertex)
                    # if n1 has a neighbor in the same set as it, then false
                    if ((n1 in set_A) and (vertex in set_A)) or ((n1 in set_B) and (vertex in set_B)):
                        return False
    
    print(set_A)
    print(set_B)
    # if we make it through the entire queue, return true
    return True


test_V_bc = [3, 1, 2, 0, 4]
test_A_bc = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 0, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 1]], dtype=np.int32)

print(test_A_bc)
print("bipartite:")
print(isBipartiteCore(test_V_bc, test_A_bc))
            
                 

