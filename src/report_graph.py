import networkx as nx
import src.setup as setup
import argparse
import matplotlib.pyplot as plt

def make_graph(A):
    graph = nx.convert_matrix.from_numpy_matrix(A)
    nx.draw(graph)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the dataset.")
    args = parser.parse_args()  

    A = setup.createAdjMatrix(args.path)
    make_graph(A)

