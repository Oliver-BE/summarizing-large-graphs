"""
This will eventually run our overall VoG algorithm.
"""
import argparse

def runVoG():
    # deal with command line inputs
    parser = argparse.ArgumentParser() 
    parser.add_argument("path", help = "Path to the dataset")
    parser.add_argument("-v", help = "Verbose (adds additional helpful print statements",
                        action = "store_true")
    args = parser.parse_args() 

    # only print if verbose tag activated
    if args.v:
        print(f"Path to the dataset: {args.path} \n")
        
    # step 1: graph decomposition with slashburn
    # slashburn()
    # step 2: identifying graph substructure types
    # step 3: calculate MDL costs
    # step 4: calculate best model using heuristics
    pass

if __name__ == "__main__":
    runVoG()
    