# Base of code taken from MDL_error https://github.com/GemsLab/VoG_Graph_Summarization
from math import log,factorial
import src.MDL 
import src.graph_classification as gc

### Encoding the Error

def createAdjacencyMatrix(adj, V):
    # Initialize a matrix
    matrix = [[0 for j in range(V)]
                 for i in range(V)]
     
    for i in range(V):
        for j in adj[i]:
            matrix[i][j] = 1

    return matrix

def MDL_error_cost(model, A, excluded): 
	covered = set()
	ignored = set()
	modelledErrors = set()
	# By default, the number of unmodelled errors is the number of edges
	# and the number of modelled errors is 0.
	# Compute no. edges
	unmodelled = 0
	for i in range(len(A)):
		for j in range(i, len(A)):
			if A[i][j] == 1:
				unmodelled += 1 

	modelled = 0
	for subgraph in model: 
		approx = False
		for x in subgraph:
			for y in subgraph:  
				if (min(x, y), max(x, y)) in excluded:
					approx = True
		edges = gc.getEdges(subgraph, A)
		# NOTE: assuming that subgraph has property nodes, a list of its nodes, and property edges, a list of all its edges

		for x in subgraph:
			for y in subgraph:
				
				# Consider only edges in the subgraph. This allows us to create a 
				# blanket method for dealing with different types of subgraphs
				if (min(x, y), max(x, y)) not in edges and (min(x, y), max(x, y)) not in excluded:
					continue
				if (min(x, y), max(x, y)) in ignored:
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
					if approx:
						ignored.add((min(x, y), max(x, y)))

				# If the edge has been covered:
				else:

					# If the edge exists in A, but the model does not contain it, remove a modelling error
					if A[x][y] == 1 and (min(x, y), max(x, y)) in modelledErrors:

						modelled -= 1

					# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
					elif A[x][y] == 0 and (min(x, y), max(x, y)) not in modelledErrors:

						modelled += 1

					if approx:
						ignored.add((min(x, y), max(x, y)))

	# Once the number of modelled and unmodelled errors have been computed, compute the error cost

	# Error cost computed using typed prefix method from paper (see function LErrorTypedPrefix(G, M, E))

	return ErrorPrefix(len(A), len(covered), len(excluded), modelled, unmodelled) # TODO: The 0 here should technically be the count of 'excluded' edges, needs to be handled later

def ErrorPrefix(num_nodes, num_covered, num_excluded, modelled, unmodelled):
	posNumEdges = (num_nodes * num_nodes - num_nodes) / 2
	# if (num_covered - num_excluded) - modelled < 0  or (num_covered - num_excluded) - unmodelled< 0:
	# 	print(f"num_covered: {num_covered}, num_excluded: {num_excluded}, modelled: {modelled}, unmodelled: {unmodelled}")
	costM = LnU(num_covered - num_excluded, modelled)
	costU = LnU(posNumEdges - num_covered, unmodelled)
	return costM + costU


def LnU(n,k): 
    if n==0 or k==0 or k==n:
        return 0
    if n < k:
	     return 0 

    x = -log(k / float(n),2)
    y = -log((n-k)/float(n),2)
    return (k * x + (n-k) * y)

    # Encoded length of `n` 0/1 entries with `k` 1s (aka, Uniform)


def cliqueError(V, A, excluded):
	modelled = 0
	unmodelled = len(V)*len(V)/2
	covered = set()
	modelledErrors = set()
	ignored = set()
	for x in V:
		for y in V:
			
			if (min(x, y), max(x, y)) in ignored:
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
				
				if (min(x, y), max(x, y)) in excluded:
					ignored.add((min(x, y), max(x, y)))

			# If the edge has been covered:
			else:

				# If the edge exists in A, but the model does not contain it, remove a modelling error
				if A[x][y] == 1 and (min(x, y), max(x, y)) in modelledErrors:

					modelled -= 1

				# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
				elif A[x][y] == 0 and (min(x, y), max(x, y)) not in modelledErrors:

					modelled += 1

				if (min(x, y), max(x, y)) in excluded:
					ignored.add((min(x, y), max(x, y)))

	return ErrorPrefix(len(A), len(covered), len(ignored), modelled, unmodelled)

def starError(V, A, excluded, hub):
	modelled = 0
	unmodelled = len(V) - 1
	covered = set()
	modelledErrors = set()
	ignored = set()

	for x in V:
		# If edge is not yet covered:
		if (min(x, hub), max(x, hub)) in ignored:
				continue

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

			if (min(x, hub), max(x, hub)) in excluded:
					ignored.add((min(x, hub), max(x, hub)))

		# If the edge has been covered:
		else:

			# If the edge exists in A, but the model does not contain it, remove a modelling error
			if A[x][hub] == 1 and (min(x, hub), max(x, hub)) in modelledErrors:

				modelled -= 1

			# Otherwise, if the edge does not exist, but the model says it does, add a modelling error
			elif A[x][hub] == 0 and (min(x, hub), max(x, hub)) not in modelledErrors:

				modelled += 1

			if (min(x, hub), max(x, hub)) in excluded:
					ignored.add((min(x, hub), max(x, hub)))

	return ErrorPrefix(len(A), len(covered), len(ignored), modelled, unmodelled)