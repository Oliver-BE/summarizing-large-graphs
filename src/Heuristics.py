"""
This file defines the three heuristics used in the paper that select a model to summarize
the graph given a set of candidate structures.
"""
from math import log
from src.MDL_error import MDL_error_cost 

def Plain (candidates):
	"""
	The baseline heuristic. 
	Returns a graph summary by including all of the candidate structures in our Model.
	Args:
		candidates: a dictionary of candidate structures (list of lists) and their associated costs (double)
					(key: cost, value: candidate)
	Returns:
		a model, which is a containing the selected structures
	"""
	Model = []
	# add the candidate to the model
	for subgraphs in candidates.values():
		for candidate in subgraphs:
			Model.append(candidate)
	return Model

def Top_K (candidates, k):
	"""
	Selects the top k candidate structures.
	Args:
		candidates: a dictionary of candidate structures (list of lists) and their associated costs (double)
					(key: cost, value: candidate)
		k: the number of candidate structures to select (from the top)
	Returns:
		a model, which is a set of selected structures
	"""
	Model = []
	# sort the candidates dictionary by cost
	sorted_keys = sortByQuality(candidates)
	count = 0
	# go through each candidate in order (using the sorted keys)
	for cost in sorted_keys:
		for candidate in candidates[cost]:
			if (count < k):
				Model.append(candidates[cost])
				count += 1
			else:
				break
	return Model

def GreedyNForget (candidates, A, excluded):
	"""
	Iterates sequentially through candidates and if total encoded cost of graph M 
	does not increase, keep it; otherwise remove it.
	Args:
		candidates: a dictionary of candidate structures (list of lists) and their associated costs (double)
					(key: cost, value: candidate)
		A: adjacency matrix for the entire graph
	Returns:
		a model, which is a set containing the selected structures
	""" 
	Model = []
	# sort the dictionary by cost
	sorted_keys = sortByQuality(candidates)
	# add the first candidates
	Model.append(candidates[sorted_keys[0]][0])
	modelCost = getTotalEncodingCost(Model, sorted_keys[0], A, excluded)
	
	i = 0
	for cost in sorted_keys:
		for candidate in candidates[cost]:
			# we've already added the first candidate
			if i == 0:
				i = 1
				next
			# get current candidate based on the key (cost)
			current_candidate = candidates[cost]
			
			# our new model is the old model with the current candidate added
			Model.append(current_candidate)
			model_cost_new = getTotalEncodingCost(Model, cost, A, excluded)

			if model_cost_new <= modelCost:
				modelCost = model_cost_new
			else:
				Model.remove(current_candidate)  

	return Model

def sortByQuality(candidates):
	"""
	Sort a dictionary by key where key is the encoding cost from lowest to highest encoding cost.
	Returns a sorted list of keys.
	"""
	return sorted(candidates.keys())

def getTotalEncodingCost(model, MDL_cost, A, excluded):
	# MDL_error_cost is from the MDL_error file (converts model into adjacency matrix and computes error by taking
	# exclusive or with original adjacency matrix A)
	return MDL_cost + MDL_error_cost(model, A, excluded)