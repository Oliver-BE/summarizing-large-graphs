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
  Args:
    V is a list of vertices that form a subgraph.
    A is the adjacency matrix for the entire graph (which contains V).
  Returns:
    True if the list of vertices form a full bipartite core, false if not.
    A full bipartite core is defined as a bipartite graph that has a full set of connections
    between both of the two sets A and B forming the graph.
  """
  queue = deque() 
  set_A = set()
  set_B = set()

  # arbitrarily choose start node as first node in subgraph and add to A
  start_node = V[0]
  set_A.add(start_node)
  queue.append(start_node) 
  # a counter for all edges added
  edges_seen = 0

  # while queue not empty
  while len(queue) > 0:
    n1 = queue.popleft()
    # go through all vertices and find all neighbors of first vertex in queue
    for vertex in V:
      # if vertex is a neighbor and not itself
      if A[n1][vertex] == 1 and n1 != vertex:
        # for every neighbor, increment edges seen (this will double count, we deal with later)
        edges_seen += 1 
        # if we already haven't added this neighbor
        if vertex not in set_A and vertex not in set_B: 
          # then add the vertex to the opposite set and add to queue
          if n1 in set_A: 
            set_B.add(vertex)
            queue.append(vertex) 
          elif n1 in set_B: 
            set_A.add(vertex)
            queue.append(vertex) 
        # otherwise, if n1 has a neighbor in the same set as it, then false
        elif ((n1 in set_A) and (vertex in set_A)) or ((n1 in set_B) and (vertex in set_B)): 
          return False
    
  num_possible_edges = len(set_A) * len(set_B)
  # we are double counting above, so divide by two here
  edges_seen /= 2
  # at this point, we have a biparttie graph, we need make sure it's fully connected
  if edges_seen == num_possible_edges:
    return True
  # otherwise, it's bipartite but not fully connected, so false
  else:
    return False

test_V_bc = [3, 1, 2, 0, 4]
test_A_bc_true = np.array([[1, 0, 1, 1, 1], \
                          [0, 1, 1, 1, 1], \
                          [1, 1, 1, 0, 0], \
                          [1, 1, 0, 1, 0], \
                          [1, 1, 0, 0, 1]], dtype=np.int32)
# this is not fully connected but is bipartite                           
test_A_bc_false = np.array([[1, 0, 1, 1, 1], \
                            [0, 1, 1, 1, 0], \
                            [1, 1, 1, 0, 0], \
                            [1, 1, 0, 1, 0], \
                            [1, 0, 0, 0, 1]], dtype=np.int32)
                            
print("bipartite:")
print(isBipartiteCore(test_V_bc, test_A_bc_true))
print(isBipartiteCore(test_V_bc, test_A_bc_false))

            
                 

