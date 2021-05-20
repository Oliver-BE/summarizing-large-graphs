import networkx as nx
import src.setup as setup
import src.slashburn as sb
import src.MDL_error as mdle
import argparse
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network

def make_graph(A):
    graph = nx.convert_matrix.from_numpy_matrix(A)
    # set seed so that graph is drawn in same way each time
    my_pos = nx.spring_layout(graph, seed = 100)
    nx.draw(graph, pos = my_pos, node_size=5, with_labels=True, node_color="blue", width=1, edge_color="lightgrey", node_shape="o", linewidths=1, alpha=0.5)
    plt.show()
    # net = Network(notebook=True)
    # net.from_nx(graph)
    # net.show("graph.html") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the dataset.")
    parser.add_argument("-sb", help="Choose whether or not to run SlashBurn before creating graph.",
                                action="store_true")
    parser.add_argument("-minsize", help="The minimum size of a subgraph that will be considered when generating subgraphs. Default value is 3.",
                        type=int, default=3)                               
    args = parser.parse_args()  

    A = setup.createAdjMatrix(args.path)
    
    if args.sb:
        subgraphs = sb.run_slashburn(A, args.minsize)

        print(f"{len(subgraphs)} subgraphs found from slashburn")
        
        # combine all subgraphs into "one" subgraph for sake of printing
        final_subgraph = set()
        for subgraph in subgraphs:
            for node in subgraph:
                final_subgraph.add(node)
        
        final_subgraph = list(final_subgraph) 
        
        A_sb = mdle.createSubAdjacencyMatrix(final_subgraph, A)
        A_sb = np.asarray(A_sb, dtype=np.int32) 
    
        make_graph(A_sb)

    else:
        make_graph(A)