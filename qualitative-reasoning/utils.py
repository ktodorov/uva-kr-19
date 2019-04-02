import networkx as nx
import matplotlib.pyplot as plt
from typing import List

from node import Node

def create_representation_graph(
    nodes : List[Node],
    font_color: str = 'black', 
    node_size: int = 500,
    file_path: str = None):
    
    G=nx.DiGraph()
    
    # add all nodes
    G.add_nodes_from([node.label for node in nodes])
    
    node_color_map = []

    # add the edges between the nodes
    # also populate the node_color_map
    for node in nodes:
        for node_connection in node.connections:
            G.add_edge(node.label, node_connection)
        
        node_color_map.append(node.color)

    nx.draw(
        G, 
        font_color = font_color, 
        node_color = node_color_map, 
        with_labels = True, 
        node_size = node_size)

    if file_path:
        plt.savefig(file_path)
    else:
        plt.show()