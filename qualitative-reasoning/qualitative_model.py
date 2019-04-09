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
        self.value_to_derivative_constraints = {}

        # initialize the dependencies dictionaries
        for quantity in self.quantities:
            self.incoming_dependencies[quantity.label] = {}
            self.outgoing_dependencies[quantity.label] = {}
            self.constraint_dependencies[quantity.label] = {}
            self.value_to_derivative_constraints[quantity.label] = {}

        for dependency in dependencies:
            if dependency.type == DependencyType.Constraint:
                if dependency.start.label not in self.constraint_dependencies[dependency.end.label].keys():
                    self.constraint_dependencies[dependency.end.label][dependency.start.label] = [
                    ]

                self.constraint_dependencies[dependency.end.label][dependency.start.label].append(
                    dependency)
            # elif dependency.type == DependencyType.ValueToDerivativeConstraint:
            #     if dependency.start.label not in self.value_to_derivative_constraints[dependency.end.label].keys():
            #         self.value_to_derivative_constraints[dependency.end.label][dependency.start.label] = [
            #         ]

            #     self.value_to_derivative_constraints[dependency.end.label][dependency.start.label].append(
            #         dependency)
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
        filtered_states = []

        for state in all_states:
            if (self.is_valid_constraint_state(state) and
                self.is_valid_value_to_derivative_state(state) and
                self.is_valid_positive_influence_state(state) and
                self.is_valid_negative_influence_state(state) and
                self.is_valid_positive_proportionality_state(state) and
                    self.is_valid_negative_proportionality_state(state)):
                filtered_states.append(state)

        return filtered_states

    def visualize_states(self):
        all_combinations = self.generate_all_combinations()
        nodes = []
        edges = []
        # print(len(all_combinations))
        # self.print_combinations(all_combinations)

        for i, start_state in enumerate(all_combinations):
            nodes.append(start_state)

            for j, end_state in enumerate(all_combinations):
                if i == j:
                    continue

                if self.transition_exists(start_state, end_state):
                    edges.append((start_state, end_state))

        utils.create_representation_graph(
            nodes,
            edges,
            file_path='results/qualitative_graph.gv')

    # Constraint check

    def is_valid_constraint_state(self, state: QualitativeState) -> bool:
        for j, dependent_state in enumerate(state.get_quantities()):
            for constraint_state_label, constraint_spaces in self.constraint_dependencies[dependent_state.quantity.label].items():
                # check if we have the constraint_state_label with the constraint_space currently and
                # if yes, the quantity should be with the same value
                for k, independent_state in enumerate(state.get_quantities()):
                    if j == k or independent_state.quantity.label != constraint_state_label:
                        continue

                    for constraint_dependency in constraint_spaces:
                        # if the independent variable does not have one of the values and gradients
                        # selected, it means the dependency is not in place, so we skip this
                        if ((constraint_dependency.start_quantity_values and
                             independent_state.value not in constraint_dependency.start_quantity_values) or
                                (constraint_dependency.start_quantity_gradients and
                                 independent_state.gradient not in constraint_dependency.start_quantity_gradients)):
                            continue

                        if ((constraint_dependency.end_quantity_values and
                             dependent_state.value not in constraint_dependency.end_quantity_values) or
                                (constraint_dependency.end_quantity_gradients and
                                 dependent_state.gradient not in constraint_dependency.end_quantity_gradients)):
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
            value_index = quantity_state.quantity.spaces.index(
                quantity_state.value)
            # if the index is the first one this means it's the lowest possible value.
            # Then we shouldn't have '-' derivative
            # if the index is the last one this means it's the lowest possible value.
            # Then we shouldn't have '+' derivative

            if value_index == 0 and quantity_state.gradient == '-':
                return False
            elif value_index == len(quantity_state.quantity.spaces) - 1 and quantity_state.gradient == '+':
                return False

        return True

    def transition_exists(self, start_state: QualitativeState, end_state: QualitativeState):
        possible_changes = self.get_possible_changes(start_state)
        if end_state not in possible_changes:
            return False

        return True

    def get_possible_changes(self, state: QualitativeState) -> List[QualitativeState]:

        possible_states_by_quantity = []
        all_gradients_are_zero = True

        for i, quantity_state in enumerate(state.get_quantities()):
            possible_states_by_quantity.append([])
            possible_states_by_quantity[i].append(quantity_state)
            quantity_state_value_index = quantity_state.quantity.spaces.index(
                quantity_state.value)

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
            # if the value and derivative of inflow is 0, the derivative of inflow can go to +
            elif quantity_state.gradient == '0' and quantity_state.value.label == '0' and quantity_state.quantity.label == 'Inflow':
                new_possible_state = QuantityState(
                    quantity_state.quantity, quantity_state.value, '+')
                possible_states_by_quantity[i].append(new_possible_state)
            # if our gradient is - and we can move further down the values
            elif quantity_state.gradient == '-' and quantity_state_value_index != 0:
                all_gradients_are_zero = False
                new_gradient = quantity_state.gradient
                # if we have reached the end, the gradient must become neutral
                if quantity_state_value_index == 1:
                    new_gradient = '0'

                new_value = quantity_state.quantity.spaces[quantity_state_value_index - 1]
                new_possible_state = QuantityState(
                    quantity_state.quantity, new_value, new_gradient)
                possible_states_by_quantity[i].append(new_possible_state)

        all_possible_combinations = list(
            itertools.product(*possible_states_by_quantity))

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

            state1_value_index = state1_quantities[i].quantity.spaces.index(
                state1_quantities[i].value)
            state2_value_index = state2_quantities[i].quantity.spaces.index(
                state2_quantities[i].value)
            result += abs(state1_value_index - state2_value_index)

            state1_gradient_index = state1_quantities[i].quantity.gradients.index(
                state1_quantities[i].gradient)
            state2_gradient_index = state2_quantities[i].quantity.gradients.index(
                state2_quantities[i].gradient)
            result += abs(state1_gradient_index - state2_gradient_index)

        return result

    def print_combinations(self, all_states: List[QualitativeState]):
        print('---------------------------------------------')
        print(f'total combinations: {len(all_states)}')
        print('---------------------------------------------')

        for qualitative_state in all_states:
            print(str(qualitative_state))

    # def create_exogenous_inflow_transition(self, all_states: List[QualitativeState]):
    #     zero_state = [state for state in all_states if
    #                   all(quantity_state.value.label == '0' and quantity_state.gradient == '0' for quantity_state for state.get_quantities())
    #                   ][0]

