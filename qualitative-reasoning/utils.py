from graphviz import Digraph
import matplotlib.pyplot as plt
from typing import List
import re

from quantity import Quantity
from quantity_dependency import QuantityDependency
from qualitative_state import QualitativeState

def get_state_string(state: QualitativeState):
    result = ''
    for quantity in state.get_quantities():
        result = result + f'({quantity.quantity.label}, {quantity.value.label}, {quantity.gradient}), '

    return result

def find_differences(state_1, state_2):
    differences = []
    state_1 = re.findall(r'\[([^]]*)\]', state_1)
    state_2 = re.findall(r'\[([^]]*)\]', state_2)

    if len(state_1) and len(state_2) != 3:
        print(state_1)
        print(state_2)

    #finds index of difference
    diff = [i for i in range(len(state_1)) if state_1[i] != state_2[i]]

    for i in range(len(diff)):
        if diff[i] == 0:
            #finds index of differences in inflow
            d = [k for k in range(3) if state_1[0][k] != state_2[0][k]]

            for j in range(len(d)):
                if d[j] == 0:
                    differences.append('IN value')
                if d[j] == 2:
                    differences.append('IN gradient')
        if diff[i] == 1:
            #finds index of differences in outflow
            d = [k for k in range(3) if state_1[1][k] != state_2[1][k]]

            for j in range(len(d)):
                if d[j] == 0:
                    differences.append('OUT value')
                if d[j] == 2:
                    differences.append('OUT gradient')
        if diff[i] == 2:
            #finds index of difference in volume
            d = [k for k in range(3) if state_1[2][k] != state_2[2][k]]

            for j in range(len(d)):
                if d[j] == 0:
                    differences.append('V value')
                if d[j] == 2:
                    differences.append('V gradient')

    return differences

def create_representation_graph(
        states: List[QualitativeState],
        edges: List[tuple],
        visited_edges: List,
        file_path: str):

    graph = Digraph(comment='The Qualitative Model')
    graph.node_attr.update(color='skyblue', style='filled')

    for i, state in enumerate(states):
        # graph.node("State {}\n".format(i+1) + state.get_string_representation()) #changed this!!!!!!!!!!!!
        # graph.node(state.get_string_representation())
        graph.node(state)

    # differences = find_differences(visited_edges[0][0], visited_edges[0][1])

    # print(differences)

    for i, edge in enumerate(edges):
        # graph.edge("State {}\n".format(i+1) + edge[0].get_string_representation(), "State {}\n".format(i+2) + edge[1].get_string_representation())
        # graph.edge(edge[0].get_string_representation(), edge[1].get_string_representation())
        if edge in visited_edges:
            differences = find_differences(edge[0], edge[1])
            graph.edge(edge[0],edge[1], color='red', label= str(differences)) ###################
        else:
            graph.edge(edge[0], edge[1], color = 'black')


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
