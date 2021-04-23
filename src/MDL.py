import csv
import numpy as np
import math

from collections import defaultdict
from scipy.sparse import coo_matrix

"""
Questions:
On page 5, what is the difference between l1 and l0 in the enconding for near cliques?
An equation for l1 is given, but one for l0 is not. (The paper states that l1 is "analogue for l0".)
Also, we are a bit confused on what it means to identify which edges are present and which
are not using "optimal prefix codes." What does it mean in this context to have a missing edge? 
(Is this simply a 0 in the adjaceny matrix? And if so, is the number of present edges simply the number
of edges that we can find by doing |area(nc)|?)

Does the area(nc) just mean the total size of the adjaceny matrix?

Is n in L(s) the total number of nodes in the initial input graph G? This is what it seems like
based on the notation table (Table 1) but we wanted to confirm.
"""

"""
Overall structure:

Input: A model family M (set of models), a graph G, and a vocabulary Omega
        Omega = {full clique, near clique, full bi-partite core, near bi-partite core, chains, stars} 
        For the sake of conciseness we will refer to the above as: {fc, nc, fb, nb, ch, st} respectively  
              
Output: Smallest model m for which L(M) + L(E) is minimized where L(M) and L(E) are the 
        numbers of bits that describe the structures, and the error matrix E respectively.

Another way: 

Crude4
, Two-part Version of MDL Principle (Informally Stated)
Let H(1)
, H(2)
, . . . be a list of candidate models (e.g., H(k)
is the set of k-th degree
polynomials), each containing a set of point hypotheses (e.g., individual polynomials). The best point hypothesis H ∈ H(1) ∪ H(2) ∪ . . . to explain the data D is the
one which minimizes the sum L(H) + L(D|H), where
• L(H) is the length, in bits, of the description of the hypothesis; and
• L(D|H) is the length, in bits, of the description of the data when encoded
with the help of the hypothesis.
The best model to explain D is the smallest model containing the selected H.



ex:  if M.numFullCliques > 0 :
      model_cost += M.numFullCliques * log(M.numFullCliques / float(M.numStructs), 2);

trying to check model cost 

2 different model costs 

model cost1: the sum of the different encodings of structures. Take sum of number of structure times the log of the number of that structure/total structures
then loop through each structure and add the length of that structure (i..e LfullClique(struc,M,G,E)). 


model cost2/error cost: length of error type  

want to return total_cost (model+error), error cost, model cost, and Error(G)

minimize model + model2


also a greedy version of MDL that we can worry about later. 

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
		area_nc = graph.numEdges

		num_nodes = LN(cardinality_nc)
		node_ids = math.log(math.comb(num_nodes_G, cardinality_nc))
		num_edges = math.log(area_nc)

		# edges = ||nc||l1 + ||nc||'l0
		# l1 = − log((||nc||/(||nc|| + ||nc||)) 
		
		desc_len = num_nodes + node_ids + num_edges # + edges
		
	# full bi-partite core
	elif graph_type == "fb":
		cardinality_a = graph.numNodes_A
		cardinality_b = graph.numNodes_B
		nodeIds_a_b = math.log(math.comb(num_nodes_G)//(math.factorial(cardinality_a)*(math.factorial(cardinality_b))))
		desc_len = cardinality_a+cardinality_b+nodeIds_a_b

	# near bi-partite core
	elif graph_type == "nb":
		cardinality_a = graph.numNodes_A # property needs to be defined
		cardinality_b = graph.numNodes_B # property needs to be defined
                cardinality_a_resp_b = LN(cardinality_a) + LN(cardinality_b)
		# nodeIds_a_b = # TBD once nC(a, b) notation determined
		# num_edges = math.log(area_nc)
		# edges = # TBD once form of l_0 function confirmed
		# desc_len = cardinality_a+cardinality_b+nodeIds_a_b+num_edges+edges
		
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
        

