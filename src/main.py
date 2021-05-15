import argparse 
import src.setup as setup
import src.slashburn as sb
import src.graph_classification as gc

def runVoG():
    # step 0: read in dataset and create adjacency matrix
    A = setup.createAdjMatrix(args.path) 
    # step 1: graph decomposition with slashburn
    subgraphs = sb.run_slashburn(A)
    # step 2: identifying graph substructure types
    # key: string (label), value: subgraph (set of lists)
    labels = dict()
    candidates = dict()
    for subgraph in subgraphs:
        temp = set()
        V, cost, label = gc.getGraphTypeAndCost(subgraph, A)
        if label in labels:
            labels[label].add(V)
        else:
            temp.add(V)
            labels[label] = temp  
        if cost in candidates:
            candidates[cost].add(V)
        else:
            candidates[cost] = temp
    # step 3: calculate MDL costs (including encoding error)
    # step 4: calculate best model using heuristics

def runVoG_verbose(): 
    # step 0: read in dataset and create adjacency matrix
    A = setup.createAdjMatrix(args.path)  
    print("Adjacency matrix A:", flush=True)
    for row in A:
        print(row, flush=True) 
    print(flush=True)

    # step 1: graph decomposition with slashburn
    print("Running SlashBurn graph decomposition...", flush=True)
    subgraphs = sb.run_slashburn(A) 
    print("Subgraphs generated from SlashBurn:", flush=True)
    print(subgraphs, "\n")

    # step 2: identifying graph substructure types
    labels = dict()
    candidates = dict()
    for subgraph in subgraphs:
        temp = []
        V, cost, label = gc.getGraphTypeAndCost(subgraph, A)
        print(f"V: {V}, cost: {cost}, label: {label}")
        if label in labels:
            labels[label].append(V)
        else:
            temp.append(V)
            labels[label] = temp
        temp = []    
        if cost in candidates:
            candidates[cost].append(V)
        else:
            temp.append(V)
            candidates[cost] = temp 
    
    print(labels)
    print(candidates)
    # step 3: calculate MDL costs
    # step 4: calculate best model using heuristics and encoding error


if __name__ == "__main__":
    # deal with command line inputs
    parser = argparse.ArgumentParser() 
    parser.add_argument("path", help = "Path to the dataset")
    parser.add_argument("-v", help = "Verbose (adds additional helpful print statements)",
                        action = "store_true")
    args = parser.parse_args()  

    # verbose version of VoG (print statements excluded)
    if args.v:
        runVoG_verbose()
    # no print statements (runs faster)
    else:
        runVoG()
        
# TODO: add parameter to determine the minimum size of a subgraph we consider as a structure
# VoG has this parameter set to 10 nodes (and 3 for the Wikipedia graph) -- see Section 5.1