import argparse 
import src.setup as setup
import src.slashburn as sb
import src.graph_classification as gc
import src.heuristics as h

def generateCandidates(A, subgraphs):
    # key: string (label), value: subgraph (set of lists)
    labels = dict()
    candidates = dict()
    excluded = set()
    for subgraph in subgraphs:
        temp = []
        V, cost, label, excluded = gc.getGraphTypeAndCost(subgraph, A, excluded)
        if args.v:
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
    
    return labels, candidates, excluded

def runVoG(): 
    # step 0: read in dataset and create adjacency matrix
    A = setup.createAdjMatrix(args.path) 
    # step 1: graph decomposition with slashburn
    subgraphs = sb.run_slashburn(A, args.minsize)
    # step 2 and 3: identifying graph substructure types and calculate MDL costs 
    labels, candidates, excluded = generateCandidates(A, subgraphs) 
    # step 4: generate models using heuristics
    model_plain = h.Plain(candidates)
    model_top_k = h.Top_K(candidates, args.k) 
    model_greedy = h.GreedyNForget(candidates, A) 

def runVoG_verbose(): 
    # step 0: read in dataset and create adjacency matrix
    print(f"Creating adjacency matrix from {args.path}...")
    A = setup.createAdjMatrix(args.path)  
    print("Adjacency matrix A:")
    for row in A:
        print(row) 
    print()

    # step 1: graph decomposition with slashburn
    print("Running SlashBurn graph decomposition...") 
    subgraphs = sb.run_slashburn(A, args.minsize) 
    print("Subgraphs generated from SlashBurn:")
    print(subgraphs, "\n")

    # step 2 and 3: identifying graph substructure types and calculate MDL costs
    print("Identifying graph substructure types and calculating MDL costs...")
    labels = dict()
    candidates = dict()
    excluded = set()
    labels, candidates, excluded = generateCandidates(A, subgraphs) 
    
    print(f"Labelled candidates: {labels}", flush=True)
    print(f"Unlabelled candidates: {candidates}", flush=True)
    print(f"Excluded edges: {excluded}", flush=True)
    print(flush=True)
    
    # step 4: generate models using heuristics
    print("Generating models...")
    model_plain = h.Plain(candidates)
    model_top_k = h.Top_K(candidates, args.k) 
    model_greedy = h.GreedyNForget(candidates, A, excluded)
    
    print(f"Plain: {model_plain}")
    print(f"Top K: {model_top_k}")
    print(f"Greedy 'N Forget: {model_greedy}")


if __name__ == "__main__":
    # deal with command line inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the dataset.")
    parser.add_argument("-k", help="The argument 'k' used in the Top K model-selection heuristic. Default value is 10.",
                        type=int, default=10)
    parser.add_argument("-minsize", help="The minimum size of a subgraph that will be considered when generating subgraphs. Default value is 3.",
                        type=int, default=3)                        
    parser.add_argument("-v", help="Verbose - adds additional helpful print statements.",
                        action="store_true")                        
    args = parser.parse_args()  

    # verbose version of VoG (print statements excluded)    
    if args.v:
        runVoG_verbose()
    # no print statements (runs faster)
    else:
        runVoG()
        
# TODO: add parameter to determine the minimum size of a subgraph we consider as a structure
# VoG has this parameter set to 10 nodes (and 3 for the Wikipedia graph) -- see Section 5.1