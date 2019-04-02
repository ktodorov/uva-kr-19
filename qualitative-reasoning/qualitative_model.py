from typing import List

from quantity import Quantity
from quantity_dependency import QuantityDependency
from enums.dependency_type import DependencyType
import utils
import itertools


class QualitativeModel:
    def __init__(self, quantities: List[Quantity], dependencies: List[QuantityDependency]):
        self.quantities = quantities
        self.dependencies = {}

        # initialize the dependencies dictionary
        for quantity in self.quantities:
            self.dependencies[quantity.label] = []

    def add_quantity_dependency(self, quantity1: Quantity, quantity2: Quantity, dependency_type: DependencyType):
        if not (quantity1 in self.quantities):
            raise Exception(
                "Quantity1 is not part of this qualitative model. Add it to the quantities before assigning dependency")

        if not (quantity2 in self.quantities):
            raise Exception(
                "Quantity2 is not part of this qualitative model. Add it to the quantities before assigning dependency")

        new_dependency = (quantity2.label, dependency_type)
        if new_dependency in self.dependencies[quantity1.label]:
            raise Exception("This dependency is already registered")

        self.dependencies[quantity1.label].append(new_dependency)

    def generate_all_combinations(self) -> List[List[str]]:
        states_per_quantity = []
        for quantity in self.quantities:
            quantity_states = utils.get_quantity_states(quantity)
            if len(quantity_states) > 0:
                states_per_quantity.append(quantity_states)

        all_combinations = list(itertools.product(*states_per_quantity))
        return all_combinations

    def visualize_states(self):
        all_combinations = self.generate_all_combinations()

        # for i, start_state in enumerate(all_combinations):
        #     for j, end_state in enumerate(all_combinations):
        #         if i == j:
        #             continue

        #         for k in range(len(start_state)):
                    # if start_state[k][1] != end_state[k][2]:
                        