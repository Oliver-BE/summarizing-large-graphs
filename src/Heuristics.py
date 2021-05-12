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
		candidates: a dictionary of candidate structures (values) and their associated costs (keys)
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
		candidates: a dictionary of candidate structures (values) and their associated costs (keys)
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
		candidates: a dictionary of candidate structures (values) and their associated costs (keys)
					 which has already been sorted by decreasing encoding cost (quality) 
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


def getTotalEncodingCost(model, MDL_cost):
	# error_cost is from one of the error files
	return MDL_cost + error_cost(model)
    
def sortByQuality(candidates):
	"""
	Sort a dictionary by key where key is the encoding cost from lowest to highest encoding cost.
	Returns a sorted list of keys.
	"""
	return sorted(candidates.keys()) 