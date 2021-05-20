"""
This file defines the three heuristics used in the paper that select a model to summarize
the graph given a set of candidate structures.
"""
from math import log
# from src.MDL_error import MDL_error_cost 

def Plain (candidates, A, starApproxs, E):
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

			candidate_hub = -1
			for hub in starApproxs:
				for cand in starApproxs[hub]:
					if cand == candidate:
						candidate_hub = hub
			E.add(candidate, A, hub) 
	return Model, E

def Top_K (candidates, k, A, starApproxs, E):
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
	for benefit in sorted_keys:
		for candidate in candidates[benefit]:
			if (count < k):
				Model.append(candidate)
				
				candidate_hub = -1
				for hub in starApproxs:
					for cand in starApproxs[hub]:
						if cand == candidate:
							candidate_hub = hub
				E.add(candidate, A, hub)
				count += 1
			else:
				break
	return Model, E

def GreedyNForget (candidates, A, starApproxs, E):
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

	candidate_hub = -1
	for hub in starApproxs:
		for cand in starApproxs[hub]:
			if cand == candidates[sorted_keys[0]][0]:
				candidate_hub = hub
	E.add(candidates[sorted_keys[0]][0], A, hub)


	#modelCost = getTotalEncodingCost(Model, sorted_keys[0], A, excluded)
	modelCost = sorted_keys[0] + E.currentErrorCost()
	
	i = 0
	for benefit in sorted_keys:
		for candidate in candidates[benefit]:
			# we've already added the first candidate
			if i == 0:
				i = 1
				continue
			# get current candidate based on the key (benefit)
			current_candidate = candidate 
			
			# our new model is the old model with the current candidate added
			Model.append(current_candidate)

			for hub in starApproxs:
				for cand in starApproxs[hub]:
					if cand == candidates[sorted_keys[0]][0]:
						candidate_hub = hub

			newError = E.errorAfterAdd(candidate, A, hub)

			#model_cost_new = getTotalEncodingCost(Model, benefit, A, excluded)
			model_cost_new = benefit + newError

			if model_cost_new <= modelCost:
				modelCost = model_cost_new
				E.add(candidate, A, hub)
			else:
				Model.remove(current_candidate)  

	return Model, E

def sortByQuality(candidates):
	"""
	Sort a dictionary by key where key is the encoding benefit from highest to lowest benefit.
	Returns a sorted list of keys.
	"""
	return sorted(candidates.keys(), reverse=True)

# def getTotalEncodingCost(model, MDL_cost, A, excluded):
# 	# MDL_error_cost is from the MDL_error file (converts model into adjacency matrix and computes error by taking
# 	# exclusive or with original adjacency matrix A)
# 	return MDL_cost + MDL_error_cost(model, A, excluded)
