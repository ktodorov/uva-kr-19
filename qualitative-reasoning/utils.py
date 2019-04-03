import networkx as nx
import matplotlib.pyplot as plt
from typing import List

from quantity import Quantity
from quantity_dependency import QuantityDependency


def create_representation_graph(
        quantities: List[Quantity],
        dependencies: List[QuantityDependency],
        font_size: int = 10,
        font_color: str = 'black',
        node_size: int = 500,
        file_path: str = None):

    G = nx.DiGraph()

    # add all quantities
    G.add_nodes_from([quantity.label for quantity in quantities])

    node_color_map = [quantity.color for quantity in quantities]

    # add the edges between the quantities
    # also populate the node_color_map
    for dependency in dependencies:
        G.add_edge(dependency.start.label, dependency.end.label)
        # for quantity_connection in quantity.connections:
        #     G.add_edge(quantity.label, quantity_connection)

        # quantity_color_map.append(quantity.color)

    nx.draw(
        G,
        font_size=font_size,
        font_color=font_color,
        node_color=node_color_map,
        with_labels=True,
        node_size=node_size)

    if file_path:
        plt.savefig(file_path)
    else:
        plt.show()


def get_quantity_states(quantity: Quantity) -> List[str]:
    quantity_states = []
    for quantity_space in quantity.spaces:
        for quantity_gradient in quantity.gradients:
            # quantity_states.append(f'{quantity.label}_{quantity_space.label}')
            quantity_states.append((quantity, quantity_space, quantity_gradient))

    return quantity_states
