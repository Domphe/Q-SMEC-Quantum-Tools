import networkx as nx
import matplotlib.pyplot as plt

def visualize_workflow():
    G = nx.DiGraph()
    G.add_edges_from([
        ("Input Geometry", "HF"),
        ("HF", "MP2"),
        ("MP2", "CCSD(T)"),
        ("Input Geometry", "DFT"),
        ("DFT", "TD-DFT")
    ])
    nx.draw_networkx(G, with_labels=True)
    plt.savefig("workflow_graphs/benchmark_workflow.png")
    print("Saved workflow graph to workflow_graphs/benchmark_workflow.png")

if __name__ == "__main__":
    visualize_workflow()