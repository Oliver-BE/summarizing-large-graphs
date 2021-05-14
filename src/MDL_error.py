# Base of code taken from MDL_error https://github.com/GemsLab/VoG_Graph_Summarization
from math import log,factorial
import src.MDL 
import src.error

### Encoding the Error

'''
def LErrorNaiveBinom(G, M, E) :
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    cost = LU(posNumEdges - E.numCellsExcluded, E.numUnmodelledErrors + E.numModellingErrors)
    if config.optVerbosity > 1 : print ' - L_nb(E)', cost
    return cost
'''
def LErrorNaivePrefix(G, M, E) : #Why do we need the M if it's never called? 
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    cost = LnU(posNumEdges - E.numCellsExcluded, E.numModellingErrors + E.numUnmodelledErrors)
    #if config.optVerbosity > 1 : print ' - L_np(E)', cost
    return cost



'''
def LErrorTypedBinom(G, M, E) :
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    
    # First encode the modelling errors
    #print 'First encode the modelling errors'
    #print 'E.numCellsCovered, E.numCellsExcluded, E.numModellingErrors;'
    #print E.numCellsCovered, E.numCellsExcluded, E.numModellingErrors;
    costM = LU(E.numCellsCovered - E.numCellsExcluded, E.numModellingErrors)
    if config.optVerbosity > 1 : print ' - L_tb(E+)', costM

    # Second encode the unmodelled errors
    #print 'Second encode the unmodelled errors' (excluded cells are always covered!)
    #print posNumEdges - E.numCellsCovered, E.numUnmodelledErrors;
    costU = LU(posNumEdges - E.numCellsCovered, E.numUnmodelledErrors)
    if config.optVerbosity > 1 : print ' - L_tb(E-)', costU
    return costM + costU
'''
def LErrorTypedPrefix(G, M, E) :
    # possible number of edges in an undirected, non-self-connected graph of N nodes
    posNumEdges = (G.numNodes * G.numNodes - G.numNodes) / 2
    costM = LnU(E.numCellsCovered - E.numCellsExcluded, E.numModellingErrors)
    # if config.optVerbosity > 1 : print ' - L_tp(E+)', costM
    costU = LnU(posNumEdges - E.numCellsCovered, E.numUnmodelledErrors)
    # if config.optVerbosity > 1 : print ' - L_tp(E-)', costU
    #print E.numCellsCovered, E.numCellsExcluded, E.numModellingErrors, posNumEdges, E.numUnmodelledErrors;
    return costM + costU


def LnU(n,k):
    #print 'LnU', n, k
    if n==0 or k==0 or k==n:
        return 0;    
    x = -log(k / float(n),2)
    y = -log((n-k)/float(n),2)
    return (k * x + (n-k) * y)

    # Encoded length of `n` 0/1 entries with `k` 1s (aka, Uniform)


'''
def LU(n,k) :
    if n==0 or k==0 :
        return 0;   
    return log(choose(n,k),2)
'''

#### 

def createAdjacencyMatrix(adj, V):
    # Initialize a matrix
    matrix = [[0 for j in range(V)]
                 for i in range(V)]
     
    for i in range(V):
        for j in adj[i]:
            matrix[i][j] = 1

    return matrix

def MDL_error_cost(model, A):
	covered = set()
	modelledErrors = set()
	# By default, the number of unmodelled errors is the number of edges
	# and the number of modelled errors is 0.
	# Compute no. edges
	unmodelled = 0
	for i in range(len(A)):
		for j in range((i+1), len(A)):
			if A[i][j] == 1:
				unmodelled += 1
	
	modelled = 0
	for subgraph in model:
		
		# NOTE: assuming that subgraph has property nodes, a list of its nodes, and property edges, a list of all its edges

		for x in subgraph.nodes:
			for y in subgraph.nodes:
				
				# Consider only edges in the subgraph. This allows us to create a 
				# blanket method for dealing with different types of subgraphs
				if (x, y) not in subgraph.edges:
					continue

				# If edge is not yet covered:
				if (min(x, y), max(x, y)) not in covered:

					# Then, if the edge (x, y) exists in A, remove an unmodelled error:
					if A[x][y] == 1:

						unmodelled -= 1

					# If the edge doesn't exist in A, we've introduced a modelling error:
					else:

						modelled += 1
						modelledErrors.add((min(x, y), max(x, y)))
					# Add (x, y) to the list of covered edges
					# Edges are added as (smallest node, largest node) because we assume the graph
					# is undirected, and this method makes things easier.
					covered.add((min(x, y), max(x, y)))

				# If the edge has been covered:
				else:

					# If the edge exists in A, but the model does not contain it, remove a modelling error
					if A[x][y] == 1 and (min(x, y), max(x, y)) in modelledErrors:

						modelled -= 1

					# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
					elif A[x][y] == 0 and (min(x, y), max(x, y)) not in modelledErrors:

						modelled += 1

	# Once the number of modelled and unmodelled errors have been computed, compute the error cost

	# Error cost computed using typed prefix method from paper (see function LErrorTypedPrefix(G, M, E))

	return ErrorPrefix(len(A), len(covered), 0, modelled, unmodelled) # TODO: The 0 here should technically be the count of 'excluded' edges, needs to be handled later

def ErrorPrefix(num_nodes, num_covered, num_excluded, modelled, unmodelled):
	posNumEdges = (num_nodes * num_nodes - num_nodes) / 2
	costM = LnU(num_covered - num_excluded, modelled)
	costU = LnU(posNumEdges - num_covered, unmodelled)
	return costM + costU


def LnU(n,k):
    #print 'LnU', n, k
    if n==0 or k==0 or k==n:
        return 0;    
    x = -log(k / float(n),2)
    y = -log((n-k)/float(n),2)
    return (k * x + (n-k) * y)

    # Encoded length of `n` 0/1 entries with `k` 1s (aka, Uniform)


def cliqueError(V, A, excluded):
	modelled = 0
	unmodelled = len(V)
	covered = set()
	modelledErrors = set()
	for x in V:
		for y in V:
			
			# Only for nonexcluded edge compute errors
			if (min(x, y), max(x, y)) not in excluded:
				# If edge is not yet covered:
				if (min(x, y), max(x, y)) not in covered:

					# Then, if the edge (x, y) exists in A, remove an unmodelled error:
					if A[x][y] == 1:

						unmodelled -= 1

					# If the edge doesn't exist in A, we've introduced a modelling error:
					else:

						modelled += 1
						modelledErrors.add((min(x, y), max(x, y)))
					# Add (x, y) to the list of covered edges
					# Edges are added as (smallest node, largest node) because we assume the graph
					# is undirected, and this method makes things easier.
					covered.add((min(x, y), max(x, y)))

				# If the edge has been covered:
				else:

					# If the edge exists in A, but the model does not contain it, remove a modelling error
					if A[x][y] == 1 and (min(x, y), max(x, y)) in modelledErrors:

						modelled -= 1

					# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
					elif A[x][y] == 0 and (min(x, y), max(x, y)) not in modelledErrors:

						modelled += 1
	return ErrorPrefix(len(A), len(covered), len(excluded), modelled, unmodelled)

def starError(V, A, excluded, hub):
	modelled = 0
	unmodelled = len(V)
	covered = set()
	modelledErrors = set()

	for x in V:
		if (min(x, hub), max(x, hub)) not in excluded:
				# If edge is not yet covered:
				if (min(x, hub), max(x, hub)) not in covered:

					# Then, if the edge (x, y) exists in A, remove an unmodelled error:
					if A[x][hub] == 1:

						unmodelled -= 1

					# If the edge doesn't exist in A, we've introduced a modelling error:
					else:

						modelled += 1
						modelledErrors.add((min(x, hub), max(x, hub)))
					# Add (x, y) to the list of covered edges
					# Edges are added as (smallest node, largest node) because we assume the graph
					# is undirected, and this method makes things easier.
					covered.add((min(x, hub), max(x, hub)))

				# If the edge has been covered:
				else:

					# If the edge exists in A, but the model does not contain it, remove a modelling error
					if A[x][hub] == 1 and (min(x, hub), max(x, hub)) in modelledErrors:

						modelled -= 1

					# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
					elif A[x][hub] == 0 and (min(x, hub), max(x, hub)) not in modelledErrors:

						modelled += 1

	return ErrorPrefix(len(A), len(covered), len(excluded), modelled, unmodelled)