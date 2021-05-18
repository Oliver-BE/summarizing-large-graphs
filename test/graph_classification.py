# make sure you run this file from the base directory (summarizing-large-graphs)
import numpy as np
import src.graph_classification as gc 
import src.MDL_error as mdle

# ------------ CHAIN ------------
print("Testing Chains:")
chain_test_V = [0, 2, 4, 3, 1]
# this sould be a chain
chain_test_A_correct = np.array([[0, 1, 0, 0, 0], \
                                 [1, 0, 1, 0, 0], \
                                 [0, 1, 0, 1, 0], \
                                 [0, 0, 1, 0, 1], \
                                 [0, 0, 0, 1, 0]], dtype=np.int32)
                                 
chain_test_A_incorrect = np.array([[0, 1, 0, 0, 0], \
                                   [1, 0, 1, 1, 0], \
                                   [0, 1, 0, 0, 0], \
                                   [0, 1, 0, 0, 1], \
                                   [0, 0, 0, 1, 0]], dtype=np.int32)

chain_test_V_2 = [0, 2, 3, 1]
chain_test_A_incorrect_2 = np.array([[0, 1, 1, 1], \
                                  [1, 0, 1, 1], \
                                  [1, 1, 0, 1], \
                                  [1, 1, 1, 0]], dtype=np.int32)

print(f"V: {chain_test_V}")
print("Should be true:", gc.isChain(chain_test_V, chain_test_A_correct))
print("Should be false:", gc.isChain(chain_test_V, chain_test_A_incorrect))
print("Should be false:", gc.isChain(chain_test_V_2, chain_test_A_incorrect_2), "\n") 

# ------------ FULL CLIQUE ------------
print("Testing Cliques:")
clique_test_V_correct = [3, 1, 0, 2]
clique_test_A_correct = np.array([[0, 1, 1, 1], \
                                  [1, 0, 1, 1], \
                                  [1, 1, 0, 1], \
                                  [1, 1, 1, 0]], dtype=np.int32)

clique_test_V_incorrect = [3, 1, 0, 2, 4]
clique_test_A_incorrect = np.array([[0, 1, 1, 1, 0], \
                                    [1, 0, 1, 1, 1], \
                                    [1, 1, 0, 1, 0], \
                                    [1, 1, 1, 0, 0], \
                                    [0, 1, 0, 0, 0]], dtype=np.int32)

print("Should be true:", gc.isClique(clique_test_V_correct, clique_test_A_correct))
print("Should be false:", gc.isClique(clique_test_V_incorrect, clique_test_A_incorrect), "\n")

# ------------ STAR ------------
print("Testing Stars:")
star_test_V = [3, 1, 4, 0, 2]
star_test_A_correct = np.array([[0, 1, 1, 1, 1], \
                                [1, 0, 0, 0, 0], \
                                [1, 0, 0, 0, 0], \
                                [1, 0, 0, 0, 0], \
                                [1, 0, 0, 0, 0]], dtype=np.int32)

star_test_A_incorrect = np.array([[0, 1, 0, 1, 1], \
                                  [1, 0, 1, 0, 0], \
                                  [0, 1, 0, 0, 0], \
                                  [1, 0, 0, 0, 0], \
                                  [1, 0, 0, 0, 0]], dtype=np.int32)

print("Should be true:", gc.isStar(star_test_V, star_test_A_correct))
print("Should be false:", gc.isStar(star_test_V, star_test_A_incorrect), "\n") 

# ------------ FULL BI-PARTITE CORE ------------
print("Testing FULL BI-PARTITE CORE:")
fb_test_V = [3, 1, 2, 0, 4]
fb_test_A_correct = np.array([[1, 0, 1, 1, 1], \
                              [0, 1, 1, 1, 1], \
                              [1, 1, 1, 0, 0], \
                              [1, 1, 0, 1, 0], \
                              [1, 1, 0, 0, 1]], dtype=np.int32)

# this is should not fully connected, but is bipartite                           
fb_test_A_incorrect = np.array([[1, 0, 1, 1, 1], \
                                [0, 1, 1, 1, 0], \
                                [1, 1, 1, 0, 0], \
                                [1, 1, 0, 1, 0], \
                                [1, 0, 0, 0, 1]], dtype=np.int32)
                            
print("Should be true:", gc.isBipartiteCore(fb_test_V, fb_test_A_correct))
print("Should be false:", gc.isBipartiteCore(fb_test_V, fb_test_A_incorrect), "\n")

# ------------ NEAR CLIQUE ------------
print("Testing NEAR CLIQUE:")
nc_test_V_correct = [3, 1, 0, 2]
nc_test_A_correct = np.array([[0, 1, 1, 1], \
                                  [1, 0, 0, 1], \
                                  [1, 0, 0, 1], \
                                  [1, 1, 1, 0]], dtype=np.int32)

nc_test_V_incorrect = [1, 4, 6, 3, 7, 2, 0, 5]
nc_test_A_incorrect = np.array([[0, 1, 0, 0, 0, 0, 1, 0], \
                              [1, 0, 1, 1, 0, 0, 0, 0], \
                              [0, 1, 0, 0, 0, 0, 0, 1], \
                              [0, 1, 0, 0, 1, 0, 0, 0], \
                              [0, 0, 0, 1, 0, 1, 0, 0], \
                              [0, 0, 0, 0, 1, 0, 0, 0], \
                              [1, 0, 0, 0, 0, 0, 0, 0], \
                              [0, 0, 1, 0, 0, 0, 0, 0]], dtype=np.int32)

print("Should be true:", gc.isNearClique(nc_test_V_correct, nc_test_A_correct, 0.8))
print("Should be false:", gc.isNearClique(nc_test_V_incorrect, nc_test_A_incorrect, 0.9))
print("Should return (6, 5):", mdle.getChainEndpoints(nc_test_V_incorrect, nc_test_A_incorrect))