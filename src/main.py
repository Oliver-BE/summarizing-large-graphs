import argparse 
import src.setup as setup
import src.slashburn as sb
import src.graph_classification as gc
import src.heuristics as h
import src.error as err

"""
This file runs VoG. Note that you will likely want to pipe the results of the running main.py
into a text file for further evaluation. 
"""

def generateCandidates(A, subgraphs, thresh):
    # key: string (label), value: subgraph (set of lists)
    labels = dict()
    candidates = dict() 
    starApproxs = dict()
    count = 0
    for subgraph in subgraphs:
        if args.v:
            if count % 100 == 0:
                print(f"{count} candidates generated", flush=True)

        V, cost, label, noise, hub = gc.getGraphTypeAndCost(subgraph, A, thresh)
        benefit = noise - cost

        if args.v: 
            print(f"benefit: {benefit} label: {label}")

        temp = []
        if label in labels:
            labels[label].append(V)
        else:
            temp.append(V)
            labels[label] = temp
        
        temp = [] 
        if benefit in candidates:
            candidates[benefit].append(V)
        else:
            temp.append(V)
            candidates[benefit] = temp
        
        temp = []
        if hub in starApproxs:
            starApproxs[hub].append(V)
        else:
            temp.append(V)
            starApproxs[hub] = temp

        count += 1

    return labels, candidates, starApproxs

def runVoG(): 
    # step 0: read in dataset and create adjacency matrix
    A = setup.createAdjMatrix(args.path) 
    # step 1: graph decomposition with slashburn 
    subgraphs = sb.run_slashburn(A, args.minsize)  
    # step 2 and 3: identifying graph substructure types and calculate MDL costs 
    labels, candidates, starApproxs = generateCandidates(A, subgraphs, args.thresh)
    E1 = err.Error(A)
    E2 = err.Error(A)
    E3 = err.Error(A) 
    # step 4: generate models using heuristics
    model_plain, E1 = h.Plain(candidates, A, starApproxs, E1)
    print(f"Plain: {model_plain}")
    print(f"Error: {E1.currentErrorCost()}\n")
    model_top_k, E2 = h.Top_K(candidates, args.k, A, starApproxs, E2)
    print(f"Top K: {model_top_k}")
    print(f"Error: {E2.currentErrorCost()}\n")
    model_greedy, E3 = h.GreedyNForget(candidates, A, starApproxs, E3)
    print(f"Greedy 'N Forget: {model_greedy}")
    print(f"Error: {E3.currentErrorCost()}") 

def runVoG_verbose(): 
    # step 0: read in dataset and create adjacency matrix 
    A = setup.createAdjMatrix(args.path)  
    print("Adjacency matrix A:")
    for row in A:
        print(row) 
    print()

    # step 1: graph decomposition with slashburn
    print("Running SlashBurn graph decomposition...") 
    subgraphs = sb.run_slashburn(A, args.minsize) 
    print("Subgraphs generated from SlashBurn:")
    print(subgraphs)
    print(f"Number of subgraphs generated: {len(subgraphs)} \n")

    # step 2 and 3: identifying graph substructure types and calculate MDL costs
    print("Identifying graph substructure types and calculating MDL costs...") 
    labels, candidates, starApproxs = generateCandidates(A, subgraphs, args.thresh)  

    print("\nNumber of structures by graph type:")
    for label in labels.keys():
        print(f"Label: {label}, number of structures: {len(labels[label])}")

    print()
    E1 = err.Error(A)
    E2 = err.Error(A)
    E3 = err.Error(A)
    # step 4: generate models using heurisfdtics
    print("Generating models...")
    model_plain, E1 = h.Plain(candidates, A, starApproxs, E1)
    print(f"Plain: {model_plain}")
    print(f"Error: {E1.currentErrorCost()}\n")
    model_top_k, E2 = h.Top_K(candidates, args.k, A, starApproxs, E2)
    print(f"Top K: {model_top_k}")
    print(f"Error: {E2.currentErrorCost()}\n")
    model_greedy, E3 = h.GreedyNForget(candidates, A, starApproxs, E3)
    print(f"Greedy 'N Forget: {model_greedy}")
    print(f"Error: {E3.currentErrorCost()}") 

if __name__ == "__main__":
    # deal with command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the dataset.")
    parser.add_argument("-k", help="The argument 'k' used in the Top K model-selection heuristic. Default value is 10.",
                        type=int, default=10)
    parser.add_argument("-minsize", help="The minimum size of a subgraph that will be considered when generating subgraphs. Default value is 3.",
                        type=int, default=3)   
    parser.add_argument("-thresh", help="The threshold for percent number of edges needed to form a near clique. Default value is 0.9.",
                        type=float, default=0.9)                       
    parser.add_argument("-v", help="Verbose - adds additional helpful print statements.",
                        action="store_true")                        
    args = parser.parse_args()  

    # verbose version of VoG (print statements excluded)    
    if args.v:
        runVoG_verbose()
    # no print statements (runs faster)
    else:
        runVoG()