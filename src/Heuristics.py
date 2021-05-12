"""
Defines the three heuristics used in the paper that select a model to summarize
the graph given a set of candidate structures.
"""

def Plain (candidates):
	"""
	The baseline heuristic. 
	Returns a graph summary by including all of the candidate structures in our Model.
	Args:
		candidates: a dictionary of candidate structures (keys) and their associated costs (values)
	Returns:
		a model, which is a list of selected structures
	"""
  Model = []
	# add the candidate to the model
	for candidate in candidates.keys():
		Model.append(candidate)
	return Model

def Top_K (candidates, k):
	"""
	Selects the top k candidate structures.
	Args:
		candidates: a dictionary of candidate structures (keys) and their associated costs (values)
		            which has already been sorted by decreasing encoding cost (quality)
		k: the number of candidate structures to select (from the top)
	Returns:
		a model, which is a list of selected structures
	"""
	Model = []
	count = 0 
	for candidate in candidates.keys()
		if (count < k):
			Model.append(candidate)
			count += 1
		else:
			break
	return Model

def GreedyNForget (candidates):
	"""
	Iterates sequentially through candidates and if total encoded cost of graph M 
	does not increase, keep it; otherwise remove it.
	Args:
		candidates: a dictionary of candidate structures (keys) and their associated costs (values)
							which has already been sorted by decreasing encoding cost (quality) 
	Returns:
		a model, which is a list of selected structures
	"""
	# TODO: Figure out if we need the encoding cost of the entire graph
	Model = []
	totalCost = 0
	modelCost = 0
	# loop through (key, value)
	for candidate, cost in candidates.items():
		if (modelCost + cost < totalCost):
			modelCost += cost
			Model.append(candidate)
	return Model

    

# def sortByQuality(candidates):
# 	"""
# 	Sorting by encoding cost, where lowest encoding cost = highest quality
# 	"""
# 	for candidate in candidates:
# 		quality[getCost(candidate)].append(candidate) # need to create, basically just adds error cost and encoding cost
# 	return sorted(d, key=d.get)
# 	# sorted(quality.keys()) # Sorting from lowest encoding cost to highest encoding cost

