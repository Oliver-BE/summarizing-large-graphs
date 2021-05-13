"""
Defines the three heuristics used in the paper that select a model to summarize
the graph given a set of candidate structures.
"""

# TODO: import error_cost, make sure forrmats line up

def Plain (candidates):
	"""
	The baseline heuristic. 
	Returns a graph summary by including all of the candidate structures in our Model.
	Args:
		candidates: a dictionary of candidate structures (tuples) and their associated costs (double)
					(key: cost, value: candidate)
	Returns:
		a model, which is a containing the selected structures
	"""
	Model = set()
	# add the candidate to the model
	for candidate in candidates.values():
		Model.add(candidate)
	return Model

def Top_K (candidates, k):
	"""
	Selects the top k candidate structures.
	Args:
		candidates: a dictionary of candidate structures (tuples) and their associated costs (double)
					(key: cost, value: candidate)
		k: the number of candidate structures to select (from the top)
	Returns:
		a model, which is a set of selected structures
	"""
	Model = set()
	# sort the candidates dictionary by cost
	sorted_keys = sortByQuality(candidates)
	count = 0
	# go through each candidate in order (using the sorted keys)
	for cost in sorted_keys:
		if (count < k):
			Model.add(candidates[cost])
			count += 1
		else:
			break
	return Model

def GreedyNForget (candidates):
	"""
	Iterates sequentially through candidates and if total encoded cost of graph M 
	does not increase, keep it; otherwise remove it.
	Args:
		candidates: a dictionary of candidate structures (tuples) and their associated costs (double)
					(key: cost, value: candidate)
	Returns:
		a model, which is a set containing the selected structures
	""" 
	Model = set()
	# sort the dictionary by cost
	sorted_keys = sortByQuality(candidates)
	# add the first candidates
	Model.add(candidates[sorted_keys[0]])
	modelCost = getTotalEncodingCost(Model, sorted_keys[0])
	
	i = 0
	for cost in sorted_keys:
		# we've already added the first candidate
		if i == 0:
			i = 1
			next
		# get current candidate based on the key (cost)
		current_candidate = candidates[cost]
		
		# our new model is the old model with the current candidate added
		Model.add(current_candidate)
		model_cost_new = getTotalEncodingCost(Model, cost)

		if model_cost_new <= modelCost:
			modelCost = model_cost_new
		else:
			Model.remove(current_candidate)  

	return Model


def getTotalEncodingCost(model, MDL_cost, A):
	# error_cost is from one of the error files (converts model into adjacency matrix and computes error by taking
	# exclusive or with original adjacency matrix A)
	return MDL_cost + error_cost(model, A)
    
def sortByQuality(candidates):
	"""
	Sort a dictionary by key where key is the encoding cost from lowest to highest encoding cost.
	Returns a sorted list of keys.
	"""
	return sorted(candidates.keys())

def createAdjMatrix2(adj, V):
    # Initialize a matrix
    matrix = [[0 for j in range(V)]
                 for i in range(V)]
     
    for i in range(V):
        for j in adj[i]:
            matrix[i][j] = 1
     
	 
    return matrix




def error_cost(model, A):
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
		
		# fix everything below here
		# Issue: need some way to know which edges exist in the subgraph

		subgraph_type = subgraph.getType()

		if subgraph_type == "fc":

		elif subgraph_type == "nc":

		elif subgraph_type == "fb":
		
		elif subgraph_type == "nb":

		elif subgraph_type == "ch":

		elif subgraph_type == "st":

		"""
		for i in range(minNode, maxNode + 1):
			x = subgraph[i]
			for j in range(minNode, maxNod):
				if i == j:
					continue
				y = subgraph[j]
				
				# Note: formatting edge to always show nodes in increasing order; does not affect edge detection
				# since we assume the graph is undirected.
				# This modification allows us to better track which edges are covered and which are modelling errors.
				tempX = min(x, y)
				tempY = max(x, y)
				x = tempX
				y = tempY
				# If the edge (x, y) hasn't already been considered
				if (x, y) not in covered:

					# If the edge (x, y) exists in A, remove an unmodelled error
					if A[x][y] == 1:
						unmodelled -= 1
					# If the edge doesn't exist, we've introduced a modelling error
					else:
						modelled += 1
						modelledErrors.add((x, y))
					covered.add((x,y))
				# If the edge has already been considered
				else:
					# If the edge exists in A but the model does not have 
					if A[x][y] == 1 and (x, y) in modelledErrors:
		"""

def coverClique(subgraph, covered, modelledErrors):

	return
def coverBipartite(subgraph, covered, modelledErrors):
	return
def coverChain(subgraph, covered, modelledErrors):
	return
def coverStar(subgraph, covered, modelledErrors):