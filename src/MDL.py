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
	# finds optimal encoding cost
	cliqueCost = cliqueEncoding(V, A)
	starCost = starEncoding(V, A)
	# Ignoring bipartite and chain estimations for now; NP hard tasks
	return min(cliqueCost, starCost)
	
def cliqueEncoding(V, A):
	excluded = set()
	for x in V:
		for y in V:
			if A[x][y] == 0:
				excluded.add(min(x, y), max(x, y))
	cliqueCost = encodingCostFullClique(V, A)
	cliqueErrorCost = mdle.cliqueError(V, A, excluded)
	return cliqueCost + cliqueErrorCost

def starEncoding(V, A):
	excluded = set()
	hub = 0
	degHub = 0
	for x in V:
		degX = gc.getDegree(x, V, A)
		if degX > degHub:
			hub = x
			degHub = degX
	for x in V:
		if A[x][hub] == 0:
			excluded.add((min(x, hub), max(x, hub)))
	starCost = encodingCostStar(V, A, len(V) - 1)
	starErrorCost = mdle.starError(V, A, excluded, hub)
	return starCost + starErrorCost
	


def encodingCostFullClique(V, A):
	# the number of nodes in the entire, original input graph G (which is represented by A)
	num_nodes_G = len(A)
	cardinality_fc = gc.getNumNodes(V)
	num_nodes = LN(cardinality_fc)
	node_ids = math.log(math.comb(num_nodes_G, cardinality_fc))
	desc_len = num_nodes + node_ids
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
	nodeIds_a_b = math.log(math.factorial(num_nodes_G)/(math.factorial(cardinality_a)*(math.factorial(cardinality_b))))

	desc_len = cardinality_a_resp_b + nodeIds_a_b
	return desc_len







# def get_encoded_length_by_graph_type(V, A):
# 	"""
# 	This function is used to get the length in bits of a specific 
# 	graph structure type (referred to as L(s) in the paper).
# 	Args:
# 		V is a list of vertices that form a subgraph.
#     	A is the adjacency matrix for the entire graph (which contains V).
# 	Returns:
# 		The description length (in bits)
# 	"""
# 	# the number of nodes in the entire, original input graph G (which is represented by A)
# 	num_nodes_G = len(A)
# 	desc_len = 0
# 	# this gives us the graph type from our vocabulary {fc, nc, fb, nb, ch, st}
# 	graph_type = getGraphType(V, A)

# 	# full clique
# 	if graph_type == "fc":
# 		cardinality_fc = getNumNodes(V)

# 		num_nodes = LN(cardinality_fc)
# 		node_ids = math.log(math.comb(num_nodes_G, cardinality_fc))
	
# 		desc_len = num_nodes + node_ids
		
# 	# near clique
# 	elif graph_type == "nc":
# 		cardinality_nc = getNumNodes(V)
# 		# area_nc is the number of all possible edges (num_nodes choose 2 in a clique)
# 		# TODO: confirm this
# 		area_nc = math.comb(cardinality_nc, 2)

# 		num_nodes = LN(cardinality_nc)
# 		node_ids = math.log(math.comb(num_nodes_G, cardinality_nc))
# 		num_edges = math.log(area_nc)
		
# 		# TODO: clarify if present_edges is actually just the number of edges 
# 		nc_present_edges = getNumEdges(V)
# 		# if a near-clique has z nodes and w edges, then the number of missing edges is z(z-1)/2 - w
# 		nc_missing_edges = area_nc - nc_present_edges
# 		l1 = -math.log(nc_present_edges / (nc_present_edges + nc_missing_edges))
# 		l0 = -math.log(nc_missing_edges / (nc_present_edges + nc_missing_edges))
# 		edges = nc_present_edges * l1 + nc_missing_edges * l0 
		
# 		desc_len = num_nodes + node_ids + num_edges + edges
		
# 	# full bi-partite core
# 	elif graph_type == "fb":
# 		cardinality_a = V.numNodesLeft
# 		cardinality_b = V.numNodesRight

# 		cardinality_a_resp_b = LN(cardinality_a) + LN(cardinality_b)
# 		nodeIds_a_b = math.log(math.factorial(num_nodes_G)/(math.factorial(cardinality_a)*(math.factorial(cardinality_b))))
		
# 		desc_len = cardinality_a_resp_b + nodeIds_a_b

# 	# near bi-partite core
# 	elif graph_type == "nb":
# 		cardinality_a = V.numNodesLeft
# 		cardinality_b = V.numNodesRight
		
# 		cardinality_a_resp_b = LN(cardinality_a) + LN(cardinality_b)
# 		nodeIds_a_b = math.log(math.factorial(num_nodes_G)/(math.factorial(cardinality_a)*(math.factorial(cardinality_b))))

# 		# area_nb is the number of all possible edges (numNodesLeft * numNodesRight)
# 		# TODO: check this
# 		area_nb = cardinality_a * cardinality_b
# 		num_edges = math.log(area_nb)

# 		# TODO: find number of present edges by using adjacency matrix
# 		nb_present_edges = "todo"
# 		nb_missing_edges = area_nb - nb_present_edges
# 		l1 = -math.log(nb_present_edges / (nb_present_edges + nb_missing_edges))
# 		l0 = -math.log(nb_missing_edges / (nb_present_edges + nb_missing_edges))  
# 		edges = nb_present_edges * l1 + nb_missing_edges * l0

# 		desc_len = cardinality_a_resp_b + nodeIds_a_b + num_edges + edges
			
# 	# chain
# 	elif graph_type == "ch":
# 		cardinality_ch = getNumNodes(V)
# 		num_nodes = LN(cardinality_ch - 1)
		
# 		node_ids = 0
# 		for i in range(cardinality_ch + 1):
# 			node_ids += math.log(num_nodes_G - i)
		
# 		desc_len = num_nodes + node_ids
                
# 	# star
# 	elif graph_type == "st":
# 		cardinality_st = V.numSpokes
# 		num_spokes = LN(cardinality_st - 1)
# 		hub_node_id = math.log(num_nodes_G)
# 		spoke_nodes_id = math.log(math.comb(num_nodes_G - 1, cardinality_st - 1))
		
# 		desc_len = num_spokes + hub_node_id + spoke_nodes_id
	
# 	# if none of the above types, try as all of them
# 	elif graph_type == "none":
# 		pass

# 	return desc_len