from graphviz import Digraph
import matplotlib.pyplot as plt
from typing import List

from quantity import Quantity
from quantity_dependency import QuantityDependency
from qualitative_state import QualitativeState

def get_state_string(state: QualitativeState):
    result = ''
    for quantity in state.get_quantities():
        result = result + f'({quantity.quantity.label}, {quantity.value.label}, {quantity.gradient}), '

    return result

def create_representation_graph(
        states: List[str],
        edges: List[tuple],
        font_size: int = 10,
        font_color: str = 'black',
        node_size: int = 500,
        file_path: str = None):

    G = Digraph(comment='The Qualitative Model')

    for state in states:
        G.node(state)

    for edge in edges:
        G.edge(edge[0], edge[1])

    # nx.draw(
    #     G,
    #     font_size=font_size,
    #     font_color=font_color,
    #     # node_color=node_color_map,
    #     with_labels=True,
    #     node_size=node_size)

    G.render('test-output/round-table.gv', view=True)
    # if file_path:
    #     plt.savefig(file_path)
    # else:
    #     plt.show()


def get_quantity_states(quantity: Quantity) -> List[str]:
    quantity_states = []
    for quantity_space in quantity.spaces:
        for quantity_gradient in quantity.gradients:
            quantity_states.append((quantity, quantity_space, quantity_gradient))

    return quantity_states
