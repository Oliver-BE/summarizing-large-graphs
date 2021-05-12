from setup import createAdjMatrix
from slashburn import *
import argparse 

def runVoG():
    # step 0: read in dataset and create adjacency matrix
    A = createAdjMatrix(args.path) 
    # step 1: graph decomposition with slashburn
    subgraphs = run_slashburn(A)
    # step 2: identifying graph substructure types
    # step 3: calculate MDL costs (including encoding error)
    # step 4: calculate best model using heuristics

def runVoG_verobse(): 
    # step 0: read in dataset and create adjacency matrix
    A = createAdjMatrix(args.path)  
    print("Adjacency matrix A:", flush=True)
    for row in A:
        print(row, flush=True) 
    print(flush=True)

    # step 1: graph decomposition with slashburn
    print("Running SlashBurn graph decomposition...", flush=True)
    subgraphs = run_slashburn(A) 
    print("Subgraphs generated from SlashBurn:", flush=True)
    print(subgraphs)

    # step 2: identifying graph substructure types
    # step 3: calculate MDL costs (including encoding error)
    # step 4: calculate best model using heuristics


if __name__ == "__main__":
    # deal with command line inputs
    parser = argparse.ArgumentParser() 
    parser.add_argument("path", help = "Path to the dataset")
    parser.add_argument("-v", help = "Verbose (adds additional helpful print statements)",
                        action = "store_true")
    args = parser.parse_args()  

    # verbose version of VoG (print statements excluded)
    if args.v:
        runVoG_verobse()
    # no print statements (runs faster)
    else:
        runVoG()

# TODO: add parameter to determine the minimum size of a subgraph we consider as a structure
# VoG has this parameter set to 10 nodes (and 3 for the Wikipedia graph) -- see Section 5.1