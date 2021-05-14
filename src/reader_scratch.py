from setup import createAdjMatrix
from slashburn import *
import argparse 
from MDL_error import *
# testing error
def test_scratch(): 

    A = createAdjMatrix(args.path) 
    G = run_slashburn(A)
    LErrorNaivePrefix(G, M, E)





    
    

