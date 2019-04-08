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
        states: List[QualitativeState],
        edges: List[tuple],
        file_path: str):

    graph = Digraph(comment='The Qualitative Model')
    graph.node_attr.update(color='skyblue', style='filled')

    for state in states:
        graph.node(state.get_string_representation())

    for edge in edges:
        graph.edge(edge[0].get_string_representation(), edge[1].get_string_representation())

    graph.render(file_path, view=True)

def get_quantity_states(quantity: Quantity) -> List[str]:
    quantity_states = []
    for quantity_space in quantity.spaces:
        for quantity_gradient in quantity.gradients:
            quantity_states.append((quantity, quantity_space, quantity_gradient))

    return quantity_states

def tuples_contain_element(tuples: List[tuple], element: any, tuple_index: int) -> bool:
    for tuple_element in tuples:
        if tuple_element[tuple_index] == element:
            return True

    return False