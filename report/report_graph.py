import networkx as nx
import src.setup as setup
import argparse
import matplotlib.pyplot as plt
from pyvis.network import Network

def make_graph(A):
    graph = nx.convert_matrix.from_numpy_matrix(A)
    nx.draw(graph, node_size=5, with_labels=False, node_color="blue", width=1, edge_color="lightgrey", node_shape="o", linewidths=1, alpha=0.5)
    plt.show()
    # net = Network(notebook=True)
    # net.from_nx(graph)
    # net.show("graph.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the dataset.")
    args = parser.parse_args()  

    A = setup.createAdjMatrix(args.path)
    make_graph(A)

