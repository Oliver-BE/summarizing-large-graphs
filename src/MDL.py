import csv
import numpy as np
import math

from collections import defaultdict
from scipy.sparse import coo_matrix
import src.graph_classification as gc
import src.MDL_error as mdle

def LN(z):
	"""
	A function from https://github.com/GemsLab/VoG_Graph_Summarization/blob/master/MDL/mdl_base.py
	Gets the encoded size of an integer z >=1 as by Rissanen's 1983 Universal code for integers.
	This is referred to as L_N(), the MDL optimal encoding for integers >= 1 in the paper.
	"""
	if z <= 0:
		return 0	
	c = math.log(2.865064, 2)
	i = math.log(z, 2)
	while i > 0:
		c = c + i
		i = math.log(i, 2)
	return c

def optimalCost(V, A): 
	# finds optimal encoding cost of the implemented approximate structures
	cliqueCost = fullCliqueEncoding(V, A) 
	starCost, hub = starEncoding(V, A) 
	# nearCliqueCost = nearCliqueEncoding(V, A)
	# chainCost = chainEncoding(V, A, excluded) 
	# Ignoring full and near bipartite core estimations; NP hard ML classification task
	if cliqueCost <= starCost: #and cliqueCost <= nearCliqueCost: 
		return cliqueCost, -2
	elif starCost <= cliqueCost: #and starCost <= nearCliqueCost: 
		return starCost, hub
	else: 
		#return nearCliqueCost, -4
		pass
	
def fullCliqueEncoding(V, A):
	# Calculate encoding cost as a clique
	cliqueCost = encodingCostFullClique(V, A)
	cliqueErrorCost = mdle.cliqueError(V, A)
	return cliqueCost + cliqueErrorCost

def nearCliqueEncoding(V, A):
	# Calculate encoding cost as a near-clique
	# note for a near clique, we ignore the local error matrix so just return L(nc)
	return encodingCostNearClique(V, A)

def starEncoding(V, A):
	# Calculate encoding cost as a star
	hub = 0
	degHub = 0
	for x in V:
		degX = gc.getDegree(x, A, V)
		if degX > degHub:
			hub = x
			degHub = degX

	starCost = encodingCostStar(V, A, len(V) - 1)
	starErrorCost = mdle.starError(V, A, hub)
	return ((starCost + starErrorCost), hub)
	
def chainEncoding(V, A, priorExcluded):
	# Calculate encoding cost as a chain
	start, end = mdle.getChainEndpoints(V, A) 
	chainCost = encodingCostChain(V, A) 
	chainErrorCost = mdle.chainError(V, A, start, end, priorExcluded) 
	return chainCost + chainErrorCost


def encodingCostFullClique(V, A):
	# the number of nodes in the entire, original input graph G (which is represented by A)
	num_nodes_G = len(A)
	cardinality_fc = gc.getNumNodes(V)
	num_nodes = LN(cardinality_fc)
	node_ids = math.log(math.comb(num_nodes_G, cardinality_fc)) 
	return num_nodes + node_ids

def encodingCostNearClique(V, A):
	num_nodes_G = len(A)
	cardinality_nc = gc.getNumNodes(V)
	# area_nc is the number of all possible edges (num_nodes choose 2 in a clique)
	area_nc = math.comb(cardinality_nc, 2)

	num_nodes = LN(cardinality_nc)
	node_ids = math.log(math.comb(num_nodes_G, cardinality_nc))
	num_edges = math.log(area_nc)
		
	nc_present_edges = gc.getNumEdges(V, A)
	# if a near-clique has z nodes and w edges, then the number of missing edges is z(z-1)/2 - w
	nc_missing_edges = area_nc - nc_present_edges 

	l1 = -math.log(nc_present_edges / (nc_present_edges + nc_missing_edges))
	l0 = -math.log(nc_missing_edges / (nc_present_edges + nc_missing_edges))
	edges = nc_present_edges * l1 + nc_missing_edges * l0 
	
	desc_len = num_nodes + node_ids + num_edges + edges
	return desc_len

def encodingCostChain(V, A): 
	num_nodes_G = len(A) 
	cardinality_ch = gc.getNumNodes(V) 
	num_nodes = LN(cardinality_ch - 1)
	node_ids = 0
	for i in range(cardinality_ch): 
		node_ids += math.log(num_nodes_G - i)
	
	desc_len = num_nodes + node_ids
	return desc_len
	
def encodingCostStar(V, A, num_spokes):
	num_nodes_G = len(A)
	cardinality_st = num_spokes
	num_spokes = LN(cardinality_st - 1)
	hub_node_id = math.log(num_nodes_G)
	spoke_nodes_id = math.log(math.comb(num_nodes_G - 1, cardinality_st - 1))

	desc_len = num_spokes + hub_node_id + spoke_nodes_id
	return desc_len

def encodingCostFullBipartiteCore(V, A, numNodesLeft, numNodesRight):
	num_nodes_G = len(A)
	cardinality_a = numNodesLeft
	cardinality_b = numNodesRight

	cardinality_a_resp_b = LN(cardinality_a) + LN(cardinality_b)
	# utilizing log(a/b) = log(a) - log(b) and log(a*b) = log(a) + log(b) properties
	first = math.log(math.factorial(num_nodes_G))
	second = math.log(math.factorial(cardinality_a))  
	third = math.log(math.factorial(cardinality_b))
	nodeIds_a_b = first - (second + third)

	desc_len = cardinality_a_resp_b + nodeIds_a_b
	return desc_len


# def encodingCostNearBipartiteCore(V, A, numNodesLeft, numNodesRight):
# 	num_nodes_G = len(A)
# 	cardinality_a = numNodesLeft
# 	cardinality_b = numNodesRight
	
# 	cardinality_a_resp_b = LN(cardinality_a) + LN(cardinality_b)
# 	nodeIds_a_b = math.log(math.factorial(num_nodes_G)/(math.factorial(cardinality_a)*(math.factorial(cardinality_b))))

# 	# area_nb is the number of all possible edges (numNodesLeft * numNodesRight)
# 	area_nb = cardinality_a * cardinality_b
# 	num_edges = math.log(area_nb)
 
# 	nb_present_edges = gc.getNumEdges(V, A)
# 	nb_missing_edges = area_nb - nb_present_edges
# 	l1 = -math.log(nb_present_edges / (nb_present_edges + nb_missing_edges))
# 	l0 = -math.log(nb_missing_edges / (nb_present_edges + nb_missing_edges))  
# 	edges = nb_present_edges * l1 + nb_missing_edges * l0

# 	desc_len = cardinality_a_resp_b + nodeIds_a_b + num_edges + edges
# 	return desc_len