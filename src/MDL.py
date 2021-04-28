import csv
import numpy as np
import math

from collections import defaultdict
from scipy.sparse import coo_matrix

"""
MDL overall structure:

Input: A model family M (set of models), a graph G, and a vocabulary Omega
        Omega = {full clique, near clique, full bi-partite core, near bi-partite core, chains, stars} 
        For the sake of conciseness we will refer to the above as: {fc, nc, fb, nb, ch, st} respectively  
              
Output: Smallest model m for which L(M) + L(E) is minimized where L(M) and L(E) are the 
        numbers of bits that describe the structures, and the error matrix E respectively.
"""


def LN(z):
	"""
	A function from https://github.com/GemsLab/VoG_Graph_Summarization/blob/master/MDL/mdl_base.py
	Gets the encoded size of an integer >=1 as by Rissanen's 1983 Universal code for integers.
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


def get_enocoded_length_by_graph_type(graph, num_nodes_G):
	"""
	This function is used to get the length in bits of a specific 
	graph structure type (referred to as L(s) in the paper).
	Args:
		graph (graph structure): an input of type graph structure
		num_nodes_G(int): the number of nodes in the entire, original input graph G
	Returns:
		The description length (in bits)
	"""
	desc_len = 0
	# this gives us the graph type from our vocabulary {fc, nc, fb, nb, ch, st}
	graph_type = graph.getType()

	# since there's no case/switch functionality in python, we need a series of elif statements
	# full clique
	if graph_type == "fc":
		cardinality_fc = graph.numNodes

		num_nodes = LN(cardinality_fc)
		node_ids = math.log(math.comb(num_nodes_G, cardinality_fc))
	
		desc_len = num_nodes + node_ids
		
	# near clique
	elif graph_type == "nc":
		cardinality_nc = graph.numNodes
		# area_nc is the number of all possible edges (num_nodes choose 2 in a clique)
		# TODO: confirm this
		area_nc = math.comb(cardinality_nc, 2)

		num_nodes = LN(cardinality_nc)
		node_ids = math.log(math.comb(num_nodes_G, cardinality_nc))
		num_edges = math.log(area_nc)
		
		# TODO: clarify if present_edges is actually just the number of edges 
		nc_present_edges = graph.numEdges 
		# if a near-clique has z nodes and w edges, then the number of missing edges is z(z-1)/2 - w
		nc_missing_edges = area_nc - nc_present_edges
		l1 = -math.log(nc_present_edges / (nc_present_edges + nc_missing_edges))
		l0 = -math.log(nc_missing_edges / (nc_present_edges + nc_missing_edges))
		edges = nc_present_edges * l1 + nc_missing_edges * l0 
		
		desc_len = num_nodes + node_ids + num_edges + edges
		
	# full bi-partite core
	elif graph_type == "fb":
		cardinality_a = graph.numNodesLeft
		cardinality_b = graph.numNodesRight

		cardinality_a_resp_b = LN(cardinality_a) + LN(cardinality_b)
		nodeIds_a_b = math.log(math.factorial(num_nodes_G)/(math.factorial(cardinality_a)*(math.factorial(cardinality_b))))
		
		desc_len = cardinality_a_resp_b + nodeIds_a_b

	# near bi-partite core
	elif graph_type == "nb":
		cardinality_a = graph.numNodesLeft
		cardinality_b = graph.numNodesRight
		
		cardinality_a_resp_b = LN(cardinality_a) + LN(cardinality_b)
		nodeIds_a_b = math.log(math.factorial(num_nodes_G)/(math.factorial(cardinality_a)*(math.factorial(cardinality_b))))

		# TODO: equation for area_nb (num of all possible edges)
		area_nb = "todo"
		num_edges = math.log(area_nb)

		# TODO: find number of present edges 
		nb_present_edges = area_nb
		nb_missing_edges = area_nb - nb_present_edges
		l1 = -math.log(nb_present_edges / (nb_present_edges + nb_missing_edges))
		l0 = -math.log(nb_missing_edges / (nb_present_edges + nb_missing_edges))  
		edges = nb_present_edges * l1 + nb_missing_edges * l0

		desc_len = cardinality_a_resp_b + nodeIds_a_b + num_edges + edges
			
	# chain
	elif graph_type == "ch":
		cardinality_ch = graph.numNodes
		num_nodes = LN(cardinality_ch - 1)
		
		node_ids = 0
		for i in range(cardinality_ch + 1):
			node_ids += math.log(num_nodes_G - i)
		
		desc_len = num_nodes + node_ids
                
	# star
	elif graph_type == "st":
		cardinality_st = graph.numSpokes
		num_spokes = LN(cardinality_st - 1)

		hub_node_id = math.log(num_nodes_G)
		spoke_nodes_id = math.log(math.comb(num_nodes_G - 1, cardinality_st - 1))
		
		desc_len = num_spokes + hub_node_id + spoke_nodes_id

	return desc_len