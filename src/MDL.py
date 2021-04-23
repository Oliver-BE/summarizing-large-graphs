import csv
import numpy as np

from collections import defaultdict
from scipy.sparse import coo_matrix


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

