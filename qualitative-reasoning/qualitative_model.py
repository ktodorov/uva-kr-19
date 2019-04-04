from typing import List

from quantity import Quantity
from quantity_dependency import QuantityDependency
from enums.dependency_type import DependencyType
import utils
import itertools


class QualitativeModel:
    def __init__(self, quantities: List[Quantity], dependencies: List[QuantityDependency]):
        self.quantities = quantities
        self.incoming_dependencies = {}
        self.outgoing_dependencies = {}
        self.constraint_dependencies = {}

        # initialize the dependencies dictionaries
        for quantity in self.quantities:
            self.incoming_dependencies[quantity.label] = {}
            self.outgoing_dependencies[quantity.label] = {}
            self.constraint_dependencies[quantity.label] = {}

        for dependency in dependencies:
            if dependency.type == DependencyType.Constraint:
                if dependency.start.label not in self.constraint_dependencies[dependency.end.label].keys():
                    self.constraint_dependencies[dependency.end.label][dependency.start.label] = [
                    ]

                self.constraint_dependencies[dependency.end.label][dependency.start.label].append(
                    (dependency.start_space, dependency.end_space))
            else:
                self.outgoing_dependencies[dependency.start.label][dependency.end.label] = dependency.type
                self.incoming_dependencies[dependency.end.label][dependency.start.label] = dependency.type

    def generate_all_combinations(self) -> List[List[str]]:
        states_per_quantity = []
        for quantity in self.quantities:
            quantity_states = utils.get_quantity_states(quantity)
            if len(quantity_states) > 0:
                states_per_quantity.append(quantity_states)

        all_combinations = list(itertools.product(*states_per_quantity))
        filtered_combinations = self.filter_states(all_combinations)
        return filtered_combinations

    def filter_states(self, all_states):

        states_to_remove = self.find_invalid_constraint_states(
            all_states)

        for index in reversed(states_to_remove):
            all_states.pop(index)

        states_to_remove = self.find_invalid_positive_influence_states(
            all_states)

        for index in reversed(states_to_remove):
            all_states.pop(index)

        states_to_remove = self.find_invalid_negative_influence_states(
            all_states)

        for index in reversed(states_to_remove):
            all_states.pop(index)

        states_to_remove = self.find_invalid_positive_proportionality_states(
            all_states)

        for index in reversed(states_to_remove):
            all_states.pop(index)

        states_to_remove = self.find_invalid_negative_proportionality_states(
            all_states)

        for index in reversed(states_to_remove):
            all_states.pop(index)
            
        states_to_remove = self.find_invalid_value_to_derivative_states(
            all_states)

        for index in reversed(states_to_remove):
            all_states.pop(index)

        return all_states

    def visualize_states(self):
        all_combinations = self.generate_all_combinations()

        # self.print_combinations(all_combinations)

        nodes = []
        edges = []

        for i, start_state in enumerate(all_combinations):
            start_string = utils.get_state_string(start_state)
            nodes.append(start_string)

            for j, end_state in enumerate(all_combinations):
                if i == j:
                    continue

                if self.transition_exists(start_state, end_state):
                    end_string = utils.get_state_string(end_state)
                    edges.append((start_string, end_string))

        # print(len(edges))
        utils.create_representation_graph(nodes, edges)

    # Constraint check

    def find_invalid_constraint_states(self, states) -> List[int]:
        states_to_remove = []

        # remove the constraints
        for i, state in enumerate(states):
            if not self.is_valid_constraint_state(state):
                states_to_remove.append(i)

        return states_to_remove

    def is_valid_constraint_state(self, state) -> bool:
        for j, quantity in enumerate(state):
            for constraint_state_label, constraint_spaces, in self.constraint_dependencies[quantity[0].label].items():
                # check if we have the constraint_state_label with the constraint_space currently and
                # if yes, the quantity should be with the same value
                for k, quantity2 in enumerate(state):
                    if j == k or quantity2[0].label != constraint_state_label:
                        continue

                    for constraint_tuple in constraint_spaces:
                        if quantity2[1].label != constraint_tuple[0].label:
                            continue

                        if quantity[1].label != constraint_tuple[1].label:
                            return False

        return True

    # I+ check

    def find_invalid_positive_influence_states(self, states) -> List[int]:
        states_to_remove = []

        for i, state in enumerate(states):
            if not self.is_valid_positive_influence_state(state):
                states_to_remove.append(i)

        return states_to_remove

    def is_valid_positive_influence_state(self, state):
        for j, quantity in enumerate(state):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type == DependencyType.PositiveInfluence:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeInfluence:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type != DependencyType.PositiveInfluence:
                    continue

                for k, quantity2 in enumerate(state):
                    if j == k or quantity2[0].label != start_state_label:
                        continue

                    if quantity[1].label == '+':
                        if quantity2[2] != '+':
                            return False
                    elif quantity[1].label == '-':
                        if quantity2[2] != '-':
                            return False

        return True

    # I- check

    def find_invalid_negative_influence_states(self, states) -> List[int]:
        states_to_remove = []

        for i, state in enumerate(states):
            if not self.is_valid_negative_influence_state(state):
                states_to_remove.append(i)

        return states_to_remove

    def is_valid_negative_influence_state(self, state):
        for j, quantity in enumerate(state):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type == DependencyType.PositiveInfluence:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeInfluence:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type != DependencyType.NegativeInfluence:
                    continue

                for k, quantity2 in enumerate(state):
                    if j == k or quantity2[0].label != start_state_label:
                        continue

                    if quantity[1].label == '+':
                        if quantity2[2] != '-':
                            return False
                    elif quantity[1].label == '-':
                        if quantity2[2] != '+':
                            return False

        return True

    # P+ check

    def find_invalid_positive_proportionality_states(self, states) -> List[int]:
        states_to_remove = []

        for i, state in enumerate(states):
            if not self.is_valid_positive_proportionality_state(state):
                states_to_remove.append(i)

        return states_to_remove

    def is_valid_positive_proportionality_state(self, state):
        for j, quantity in enumerate(state):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type == DependencyType.PositiveProportionality:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeProportionality:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type != DependencyType.PositiveProportionality:
                    continue

                for k, quantity2 in enumerate(state):
                    if j == k or quantity2[0].label != start_state_label:
                        continue

                    # print(f'comparing {quantity[0].label} with {quantity2[0].label} [{quantity[2]} == {quantity2[2]}')
                    if quantity[2] != quantity2[2]:
                        return False

        return True

    # P- check

    def find_invalid_negative_proportionality_states(self, states) -> List[int]:
        states_to_remove = []

        for i, state in enumerate(states):
            if not self.is_valid_negative_proportionality_state(state):
                states_to_remove.append(i)

        return states_to_remove

    def is_valid_negative_proportionality_state(self, state):
        for j, quantity in enumerate(state):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type == DependencyType.PositiveProportionality:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeProportionality:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity[0].label].items():
                if dependency_type != DependencyType.NegativeProportionality:
                    continue

                for k, quantity2 in enumerate(state):
                    if j == k or quantity2[0].label != start_state_label:
                        continue

                    if quantity[2] == '+':
                        if quantity2[2] != '-':
                            return False
                    elif quantity[2] == '-':
                        if quantity2[2] != '+':
                            return False
                    elif quantity[2] == '0':
                        if quantity2[2] != '0':
                            return False

        return True

    def find_invalid_value_to_derivative_states(self, states) -> List[int]:
        states_to_remove = []

        for i, state in enumerate(states):
            if not self.is_valid_value_to_derivative_state(state):
                states_to_remove.append(i)

        return states_to_remove

    def is_valid_value_to_derivative_state(self, state):
        for quantity in state:
            value_index = quantity[0].spaces.index(quantity[1])
            # print(value_index)
            # if the index is the first one this means it's the lowest possible value.
            # Then we shouldn't have '-' derivative
            # if the index is the last one this means it's the lowest possible value.
            # Then we shouldn't have '+' derivative

            if value_index == 0 and quantity[2] == '-':
                return False
            elif value_index == len(quantity[0].spaces) - 1 and quantity[2] == '+':
                return False

        return True

    def transition_exists(self, start_state, end_state):
        # If we have quantity which is not constrained -
        # it cannot change with more than two steps in one transition
        for i, start_quantity in enumerate(start_state):
            if not self.constraint_dependencies[start_quantity[0].label]:
                if ((start_quantity[1].label == '0' and end_state[i][1].label == 'max') or
                        start_quantity[1].label == 'max' and end_state[i][1].label == '0'):

                    return False

            if (start_quantity[1].label != end_state[i][1].label and start_quantity[2] == '0'):
                if not self.incoming_dependencies[start_quantity[0].label]:
                    return False
                else:
                    pass # ????

        return True

    def print_combinations(self, all_combinations):
        print('---------------------------------------------')
        print(f'total combinations: {len(all_combinations)}')
        print('---------------------------------------------')

        for combination in all_combinations:
            print('(', end='')

            for quantity in combination:
                print(
                    f'({quantity[0].label}, {quantity[1].label}, {quantity[2]}), ', end='')

            print(')')
