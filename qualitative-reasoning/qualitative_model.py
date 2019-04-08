from typing import List

from quantity import Quantity
from quantity_dependency import QuantityDependency
from qualitative_state import QualitativeState
from quantity_state import QuantityState
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

        all_states = []
        for combination in all_combinations:
            qualitative_state = QualitativeState()
            for quantity_state in combination:
                qualitative_state.add_quantity(
                    quantity_state[0], quantity_state[1], quantity_state[2])

            all_states.append(qualitative_state)

        filtered_states = self.filter_states(all_states)
        return filtered_states

    def filter_states(self, all_states):
        filtered_states = [
            state
            for state in all_states
            if self.is_valid_constraint_state(state) and
            self.is_valid_value_to_derivative_state(state) and
            self.is_valid_positive_influence_state(state) and
            self.is_valid_negative_influence_state(state) and
            self.is_valid_positive_proportionality_state(state) and
            self.is_valid_negative_proportionality_state(state)]

        return filtered_states

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
                
                # return

        # print(len(edges))
        utils.create_representation_graph(
            nodes,
            edges,
            font_size=10,
            node_size=1500)

    # Constraint check

    def is_valid_constraint_state(self, state: QualitativeState) -> bool:
        for j, quantity_state in enumerate(state.get_quantities()):
            for constraint_state_label, constraint_spaces, in self.constraint_dependencies[quantity_state.quantity.label].items():
                # check if we have the constraint_state_label with the constraint_space currently and
                # if yes, the quantity should be with the same value
                for k, quantity_state2 in enumerate(state.get_quantities()):
                    if j == k or quantity_state2.quantity.label != constraint_state_label:
                        continue

                    for constraint_tuple in constraint_spaces:
                        if quantity_state2.value.label != constraint_tuple[0].label:
                            continue

                        if quantity_state.value.label != constraint_tuple[1].label:
                            return False

        return True

    # I+ check

    def is_valid_positive_influence_state(self, state: QualitativeState) -> bool:
        for j, quantity_state in enumerate(state.get_quantities()):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type == DependencyType.PositiveInfluence:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeInfluence:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type != DependencyType.PositiveInfluence:
                    continue

                for k, quantity_state2 in enumerate(state.get_quantities()):
                    if j == k or quantity_state2.quantity.label != start_state_label:
                        continue

                    if quantity_state.value.label == '+':
                        if quantity_state2.gradient != '+':
                            return False
                    elif quantity_state.value.label == '-':
                        if quantity_state2.gradient != '-':
                            return False

        return True

    # I- check

    def is_valid_negative_influence_state(self, state: QualitativeState) -> bool:
        for j, quantity_state in enumerate(state.get_quantities()):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type == DependencyType.PositiveInfluence:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeInfluence:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type != DependencyType.NegativeInfluence:
                    continue

                for k, quantity_state2 in enumerate(state.get_quantities()):
                    if j == k or quantity_state2.quantity.label != start_state_label:
                        continue

                    if quantity_state.value.label == '+':
                        if quantity_state2.gradient != '-':
                            return False
                    elif quantity_state.value.label == '-':
                        if quantity_state2.gradient != '+':
                            return False

        return True

    # P+ check

    def is_valid_positive_proportionality_state(self, state: QualitativeState) -> bool:
        for j, quantity_state in enumerate(state.get_quantities()):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type == DependencyType.PositiveProportionality:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeProportionality:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type != DependencyType.PositiveProportionality:
                    continue

                for k, quantity_state2 in enumerate(state.get_quantities()):
                    if j == k or quantity_state2.quantity.label != start_state_label:
                        continue

                    # print(f'comparing {quantity_state.quantity.label} with {quantity_state2.quantity.label} [{quantity[2]} == {quantity_state2.gradient}')
                    if quantity_state.gradient != quantity_state2.gradient:
                        return False

        return True

    # P- check

    def is_valid_negative_proportionality_state(self, state: QualitativeState) -> bool:
        for j, quantity_state in enumerate(state.get_quantities()):
            should_skip = {
                'positive': False,
                'negative': False
            }

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type == DependencyType.PositiveProportionality:
                    should_skip['positive'] = True
                elif dependency_type == DependencyType.NegativeProportionality:
                    should_skip['negative'] = True

            if should_skip['positive'] and should_skip['negative']:
                continue

            for start_state_label, dependency_type, in self.incoming_dependencies[quantity_state.quantity.label].items():
                if dependency_type != DependencyType.NegativeProportionality:
                    continue

                for k, quantity_state2 in enumerate(state.get_quantities()):
                    if j == k or quantity_state2.quantity.label != start_state_label:
                        continue

                    if quantity_state.gradient == '+':
                        if quantity_state2.gradient != '-':
                            return False
                    elif quantity_state.gradient == '-':
                        if quantity_state2.gradient != '+':
                            return False
                    elif quantity_state.gradient == '0':
                        if quantity_state2.gradient != '0':
                            return False

        return True

    def is_valid_value_to_derivative_state(self, state: QualitativeState) -> bool:
        for quantity_state in state.get_quantities():
            value_index = quantity_state.quantity.spaces.index(quantity_state.value)
            # if the index is the first one this means it's the lowest possible value.
            # Then we shouldn't have '-' derivative
            # if the index is the last one this means it's the lowest possible value.
            # Then we shouldn't have '+' derivative

            if value_index == 0 and quantity_state.gradient == '-':
                return False
            elif value_index == len(quantity_state.quantity.spaces) - 1 and quantity_state.gradient == '+':
                return False

        return True

    # def qualitative_states_are_equal(self, state1, state2):
    #     for i, quantity in enumerate(state1.get_quantities()):
    #         if (state1.qualitative_state_quantities[i].quantity.label != state2.qualitative_state_quantities[i].quantity.label
    #                 or state1.qualitative_state_quantities[i].value.label != state2.qualitative_state_quantities[i].value.label
    #                 or state1.qualitative_state_quantities[i].gradient != state2.qualitative_state_quantities[i].gradient):
    #             return False

    #     return True

    def transition_exists(self, start_state: QualitativeState, end_state: QualitativeState):
        possible_changes = self.get_possible_changes(start_state)
        if end_state not in possible_changes:
            return False

        # If we have quantity which is not constrained -
        # it cannot change with more than two steps in one transition
        # for i, start_quantity_state in enumerate(start_state.get_quantities()):
        #     if not self.constraint_dependencies[start_quantity_state.quantity.label]:
        #         # if ((start_quantity_state.value.label == '0' and end_state_quantities[i].value.label == 'max') or
        #         #         start_quantity_state.value.label == 'max' and end_state_quantities[i].value.label == '0'):

        #         #     return False
        #         if self.amount_of_changes(start_state, end_state, i) > 1:
        #             return False
        #     else:
        #         possible_change_states = self.get_possible_changes(start_quantity_state)
                # if self.amount_of_changes(start_state, end_state) > 1:
                    # if we have constraint, we check if the old value is not the constrained and the new independent is the one constraining
                    # for independent_quantity_label, dependency_tuples in self.constraint_dependencies[start_quantity_state.quantity.label].items():
                        # old_value = self.get_state_quantity_value(
                        #     start_state, independent_quantity_label)
                        # new_value = self.get_state_quantity_value(
                        #     end_state, independent_quantity_label)

                        # start_dependecy_labels = [
                        #     dependency_tuple.quantity.label for dependency_tuple in dependency_tuples]

                        # if old_value == new_value or new_value not in start_dependecy_labels:
                        #     return False

        # if (start_quantity_state.value.label != end_state_quantities[i].value.label and start_quantity_state.gradient == '0'):
        #     if not self.incoming_dependencies[start_quantity_state.quantity.label]:
        #         return False
        #     else:
        #         pass  # ????

        return True

    def get_possible_changes(self, state: QualitativeState) -> List[QualitativeState]:
        possible_states_by_quantity = []
        all_gradients_are_zero = True

        for i, quantity_state in enumerate(state.get_quantities()):
            possible_states_by_quantity.append([])
            possible_states_by_quantity[i].append(quantity_state)
            quantity_state_value_index = quantity_state.quantity.spaces.index(quantity_state.value)
            # if our gradient is + and we can move further up the values
            if quantity_state.gradient == '+' and quantity_state_value_index != len(quantity_state.quantity.spaces) - 1:
                all_gradients_are_zero = False
                new_gradient = quantity_state.gradient
                # if we have reached the end, the gradient must become neutral
                if quantity_state_value_index == len(quantity_state.quantity.spaces) - 2:
                    new_gradient = '0'

                new_value = quantity_state.quantity.spaces[quantity_state_value_index + 1]
                new_possible_state = QuantityState(
                    quantity_state.quantity, new_value, new_gradient)
                possible_states_by_quantity[i].append(new_possible_state)
            # if our gradient is 0 and we can move further down the values
            elif quantity_state.gradient == '0' and quantity_state_value_index != 0:
                new_possible_state = QuantityState(
                    quantity_state.quantity, quantity_state.value, '-')
                possible_states_by_quantity[i].append(new_possible_state)
            # if our gradient is - and we can move further down the values
            elif quantity_state.gradient == '-' and quantity_state_value_index != 0:
                all_gradients_are_zero = False
                new_gradient = quantity_state.gradient
                # if we have reached the end, the gradient must become neutral
                if quantity_state_value_index == 1:
                    new_gradient = '0'

                new_value = quantity_state.quantity.spaces[quantity_state_value_index - 1]
                new_possible_state = QuantityState(quantity_state.quantity, new_value, new_gradient)
                possible_states_by_quantity[i].append(new_possible_state)

        all_possible_combinations = list(itertools.product(*possible_states_by_quantity))
        
        # we remove the combination where the state stays the same
        if not all_gradients_are_zero:
            all_possible_combinations.pop(0)

        possible_states = []
        for possible_combination in all_possible_combinations:
            current_state = QualitativeState()
            for quantity_state in possible_combination:
                current_state.add_quantity_state(quantity_state)
            
            possible_states.append(current_state)
        
        return possible_states


    def amount_of_changes(self, state1: QualitativeState, state2: QualitativeState, index: int = None) -> int:
        result = 0
        state1_quantities = state1.get_quantities()
        state2_quantities = state2.get_quantities()

        for i in range(len(state1_quantities)):
            if index and index != i:
                continue

            state1_value_index = state1_quantities[i].quantity.spaces.index(state1_quantities[i].value)
            state2_value_index = state2_quantities[i].quantity.spaces.index(state2_quantities[i].value)
            result += abs(state1_value_index - state2_value_index)

            state1_gradient_index = state1_quantities[i].quantity.gradients.index(state1_quantities[i].gradient)
            state2_gradient_index = state2_quantities[i].quantity.gradients.index(state2_quantities[i].gradient)
            result += abs(state1_gradient_index - state2_gradient_index)

        return result

    def print_combinations(self, all_states: List[QualitativeState]):
        print('---------------------------------------------')
        print(f'total combinations: {len(all_states)}')
        print('---------------------------------------------')

        for qualitative_state in all_states:
            print(str(qualitative_state))