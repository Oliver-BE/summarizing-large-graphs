"""
This file contains graph classification algorithms as well as graph helper methods
(such as getting the degree of a node, or the number of edges in a graph).
"""
import math
import numpy as np
from collections import deque
import src.MDL as mdl

def getDegree(node, A, V):
    """
	Args:
		node is the node to get the degree of 
		A is the adjacency matrix for the entire graph (which contains V).
    	V is a list of vertices that form a subgraph.
    Returns:
    	The degree of a specific node.
	"""
    degree = 0
    for neighbor in V:
        if neighbor != node and A[neighbor][node] == 1:
            degree += 1
    return degree	


def getNumEdges(V, A):
    """
	Args:
    	V is a list of vertices that form a subgraph.
    	A is the adjacency matrix for the entire graph (which contains V).
    Returns: 
        The number of edges present in V according to A
    """
    # make into a set for quick lookups
    V = set(V)
    num_edges = 0
    for i in range(len(A)):
        for j in range(len(A)):
            # if this cell is part of our subgraph and there's an edge
            if (i != j) and (i in V and j in V) and (A[i][j] == 1):
                num_edges += 1
    # because we double count in an adjacency matrix
    return num_edges/2

def getEdges(V, A):
    """
    Args:
        V is a list of vertices that form a subgraph.
    	A is the adjacency matrix for the entire graph (which contains V).
    Returns:
        A list of all edges in V
    """
    edges = set()
    for x in V:
        for y in V:
            if x != y and A[x][y] == 1:
                edges.add((min(x, y), max(x, y)))
    
    return edges

def getNumNodes(V):
    """
	Args:
    	V is a list of vertices that form a subgraph.
    Returns: 
        The number of nodes in V (simply the length of V)
    """
    return len(V)


def isChain(V, A):
    """
	Args:
    	V is a list of vertices that form a subgraph.
    	A is the adjacency matrix for the entire graph (which contains V).
    Returns:
    	The encoding cost if the list of vertices form a chain, -1 if not.
	"""
    # first check is if all nodes have two neighbors except two (which have one)
    cost = mdl.encodingCostChain(V, A)
    oneCount = 0 
    startVertex = 0
    endVertex = 0 
    for vertex in V:
        if getDegree(vertex, A, V) == 1:
            oneCount +=1
            if startVertex == 0: 
                startVertex = vertex
            else:
                endVertex = vertex 
        elif getDegree(vertex,A, V) != 2:
            return (False, cost)

    if oneCount != 2:
        return (False, cost)
	
	# next go through from startVertex and see if you get to endVertex
    visited = set()
    testV = startVertex
    while testV != endVertex:
	    currentV = testV
	    for neighbor in V:
		    if A[testV][neighbor] == 1 and neighbor not in visited:
			    visited.add(testV)
			    testV = neighbor
			    break
		
	    if testV == currentV:
		    return (False, cost)
	
    # return mdl.encodingCostChain(V, A)
    return (True, cost)
    

def isStar(V, A):
    """
	Args:
    	V is a list of vertices that form a subgraph.
    	A is the adjacency matrix for the entire graph (which contains V).
    Returns:
       The encoding cost if the list of vertices form a star, -1 if not.
	"""
    # Identify single hub; make sure every other vertex has degree 1
    numSpokes = len(V) - 1
    cost = mdl.encodingCostStar(V, A, numSpokes)
    hubCount = 0
    for vertex in V:
        if getDegree(vertex, A, V) == len(V) - 1:
            hubCount += 1
        elif getDegree(vertex, A, V) != 1:
            return (False, cost)
    
    if hubCount == 1:
        return (True, cost)
    else:
        return (False, cost)
    
        
def isClique(V, A):
    """
    Args:
    	V is a list of vertices that form a subgraph.
    	A is the adjacency matrix for the entire graph (which contains V).
    Returns:
    	A tuple (Boolean, Integer)
    	(Boolean): True if the list of vertices form a clique, false if not.
        (Integer): Number of spokes from the hub
    """
    cost =  mdl.encodingCostFullClique(V, A)
    # go through the entire list of vertices and make sure each has a match
    for vertex in V:
        for vertex_2 in V:
            if vertex != vertex_2 and A[vertex][vertex_2] != 1:
                return (False, cost)
                
    return (True, cost)

def isNearClique(V, A, thresh):
    """
    Args:
    	V: is a list of vertices that form a subgraph.
    	A: is the adjacency matrix for the entire graph (which contains V).
        thresh: the threshold for percent number of edges needed to form a "near clique" 
    Returns:
    	A tuple (Boolean, Integer)
    	(Boolean): True if the list of vertices form a clique, false if not.
        (Integer): Number of spokes from the hub
    """
    cost =  mdl.encodingCostNearClique(V, A)
    num_edges = 0
    # all possible edges is num_nodes choose 2 in a clique
    num_possible_edges = math.comb(getNumNodes(V), 2) 

    for vertex in V:
        for vertex_2 in V:
            if vertex != vertex_2 and A[vertex][vertex_2] == 1:
                num_edges += 1

    # because we double count in an adjacency matrix
    num_edges /= 2 

    if num_edges / num_possible_edges >= thresh:
        return (True, cost)
    else:
        return (False, cost)
    

def isBipartiteCore(V, A):
    """ 
    Args:
    	V is a list of vertices that form a subgraph.
    	A is the adjacency matrix for the entire graph (which contains V).
    Returns:
        A tuple (Boolean, Integer, Integer)
    	(Boolean): True if the list of vertices form a full bipartite core, false if not.
    	           A full bipartite core is defined as a bipartite graph that has a full set of connections
    	           between both of the two sets A and B forming the graph.
        (Integer): Number of nodes in set A
        (Integer): Number of nodes in set B
    """
    bp = True
    queue = deque() 
    set_A = set()
    set_B = set()

    # arbitrarily choose start node as first node in subgraph and add to A
    start_node = V[0]
    set_A.add(start_node)
    queue.append(start_node) 
    # a counter for all edges added
    edges_seen = 0
    boolean = True
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
                    boolean = False
                    
    numNodesLeft = len(set_A)
    numNodesRight = len(set_B)
    num_possible_edges = len(set_A) * len(set_B)
    cost = mdl.encodingCostFullBipartiteCore(V, A, numNodesLeft, numNodesRight)

	# we are double counting above, so divide by two here
    edges_seen /= 2
	# at this point, we have a bipartite graph, we need make sure it's fully connected
    if edges_seen == num_possible_edges:
        return (boolean, cost)
	# otherwise, it's bipartite but not fully connected, so false
    else:
        boolean = False
        return (boolean, cost)  
                    
def getGraphTypeAndCost(V, A, excluded, thresh):
    """ 
    This function is used to get the type of a graph and the length in bits of the
	graph structure type (referred to as L(s) in the paper).
    Args:
    	V: a list of vertices that form a subgraph.
    	A: the adjacency matrix for the entire graph (which contains V).
        excluded: 
        thresh:
    Returns:
        A tuple containing the subgraph, the MDL encoding cost, and the graph type represented as a string
         (or "na" if no match is found).
    """
    # key: graph type, value: encoding cost
    Costs = dict()
    star, Costs["st"] = isStar(V, A) 
    chain, Costs["ch"] = isChain(V, A)
    clique, Costs["fc"] = isClique(V, A)
    # TODO: this check is fine for now, but for the "na" case we will have to come back and recalculate isNearClique
    if not clique:
        nearclique, Costs["nc"] = isNearClique(V, A, thresh)
    bipartitecore, Costs["fb"] = isBipartiteCore(V, A) 

    if star:
        return (V, Costs["st"], "st", excluded)
    elif clique:
        return (V, Costs["fc"], "fc", excluded)
    elif nearclique:
        return (V, Costs["nc"], "nc", excluded)
    elif chain:
        return (V, Costs["ch"], "ch", excluded)
    elif bipartitecore:
        return (V, Costs["fb"], "fb", excluded)
    else:
        cost, excluded = mdl.optimalCost(V, A, excluded)
        return (V, cost, "na", excluded)