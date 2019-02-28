from formula import Formula
from enums.split_method import SplitMethod
from exceptions.unsatisfiable_error import UnsatisfiableError
import utils
import copy
import time
from collections import defaultdict
import constants

class SatSolver:
    def __init__(self, formula: Formula, split_method: SplitMethod):
        self.formula = formula
        self.split_method = split_method
        self.metrics = {}

    def solve(self) -> bool:
        if self.formula.is_empty():
            return True

        self.metrics = self.create_metrics_container()

        current_values = defaultdict(lambda: None)
        result, game_time = utils.measure_function(lambda: self.solve_using_values(current_values))
        self.metrics[constants.GAMETIME_KEY] = game_time

        # self.print_metrics()

        # print(f'utils.timer1 - {utils.timer1}')
        # print(f'utils.timer2 - {utils.timer2}')
        # print(f'utils.timer3 - {utils.timer3}')
        # print(f'utils.timer4 - {utils.timer4}')

        return result

    def solve_using_values(self, values): #################
        # apply current values to the literals
        _, timer = utils.measure_function(lambda: self.formula.apply_values(values))
        self.metrics[constants.TIMER1_KEY] += timer

        # if the formula is already correct, we stop here
        is_correct, timer = utils.measure_function(self.formula.is_correct)
        self.metrics[constants.TIMER2_KEY] += timer
        if is_correct:
            self.print_end_result(values)
            return True
        
        # simplify the formula
        _, timer = utils.measure_function(self.formula.simplify)
        self.metrics[constants.TIMER3_KEY] += timer

        # take all unit clauses - those that can be only one value
        # and assign them a value
        unit_clauses, timer = utils.measure_function(self.formula.get_unit_clauses)
        self.metrics[constants.TIMER4_KEY] += timer

        if unit_clauses:
            # if we have any unit clauses that are the same literal but require
            # opposite values, we abort the current iteration as it is invalid
            valid_unit_clauses, timer = utils.measure_function(lambda: self.validate_unit_clauses(unit_clauses))
            if not valid_unit_clauses:
                self.formula.reset_elements()
                self.metrics[constants.BACKTRACKS_KEY] += 1
                return False

            self.metrics[constants.TIMER5_KEY] += timer
            self.metrics[constants.UNIT_CLAUSES_KEY] += len(unit_clauses)

            new_values = self.create_new_values(values, unit_clauses)

            # try to solve with the new values
            # if we fail, we must not forget to reset the elements 
            # which were changed during the current iteration
            result = self.solve_using_values(new_values)
            if not result:
                self.formula.reset_elements()
                self.metrics[constants.BACKTRACKS_KEY] += 1
            
            return result

        # get all pure literals and assign them values
        # then try to solve with the new values
        pure_literals = self.formula.get_pure_literals()
        if pure_literals:
            self.metrics[constants.PURE_LITERALS_KEY] += len(pure_literals)
            new_values = self.create_new_values(values, pure_literals)
            result = self.solve_using_values(new_values)
            if not result:
                self.formula.reset_elements()
                self.metrics[constants.BACKTRACKS_KEY] += 1
            
            return result

        return self.split_formula(values)

    def get_literal_using_jeroslow(self):
        all_literals = self.formula.get_all_literals_binary(True, 1)
        
        most_occurred_literals = all_literals.most_common(1)
        if most_occurred_literals:
            return most_occurred_literals[0][0]

        return None

    def get_most_occurred_literal(self):
        all_literals = self.formula.get_all_literals_by_sign(True)
        
        k = 100
        max_score = 0
        max_element = None

        for literal_number, literal_occurrences in all_literals.items():
            if literal_number < 0:
                continue
            
            negative_number_occurrences = 0
            negative_number = ((-1) * literal_number)
            if negative_number in all_literals.keys():
                negative_number_occurrences = all_literals[negative_number]
            
            current_score = (literal_occurrences + negative_number_occurrences) * 2**k + (literal_occurrences * negative_number_occurrences)
            if current_score > max_score:
                max_element = literal_number

        return max_element

    def get_first_available_literal(self, values):
        for key, value in values.items():
            if value == None:
                return key

    def validate_end_result(self, truth_clauses):
        for i in range(1, 10):
            for j in range(1, 10):
                self.validate_end_result_clause(truth_clauses, i, j)

    def validate_unit_clauses(self, unit_clauses):
        for unit_clause1 in unit_clauses:
            for unit_clause2 in unit_clauses:
                if (unit_clause1.get_number() == unit_clause2.get_number() and
                    unit_clause1.get_sign() != unit_clause2.get_sign()):
                    return False

        return True

    def create_new_values(self, values, literals):
        new_values = copy.deepcopy(values)
        for single_literal in literals:
            literal_string = single_literal.get_number()
            new_values[literal_string] = single_literal.get_sign()

        return new_values
            
    def split_formula(self, values):
        self.metrics[constants.SPLITS_KEY] += 1
        # if we have no remaining literals, then we have solved the task
        first_non_set_literal = self.get_literal_for_splitting(values)

        if not first_non_set_literal:
            if self.formula.is_correct():
                self.print_end_result(values)
                return True
            else:
                self.formula.reset_elements()
                self.metrics[constants.BACKTRACKS_KEY] += 1
                return False

        new_values = copy.deepcopy(values)

        # if we have no other options, we split
        # take the first literal which does not have a value
        # and try to solve with True as its value. If this fails try to solve with False
        # If this also fails, we abort the current iteration as it is unsolvable

        new_values[first_non_set_literal] = True
        if self.solve_using_values(new_values):
            return True

        new_values[first_non_set_literal] = False
        if self.solve_using_values(new_values):
            return True

        self.formula.reset_elements()
        self.metrics[constants.BACKTRACKS_KEY] += 1
        return False

    def get_literal_for_splitting(self, values):
        if self.split_method == SplitMethod.DEFAULT:
            first_non_set_literal = self.get_first_available_literal(values)
        elif self.split_method == SplitMethod.MOM:
            first_non_set_literal = self.get_most_occurred_literal()
        elif self.split_method == SplitMethod.JEROSLOW:
            first_non_set_literal = self.get_literal_using_jeroslow()
        
        return first_non_set_literal

    def validate_end_result_clause(self, all_clauses, position_x, position_y):
        matches = 0
        for clause in all_clauses:
            str_clause = str(clause)
            if str_clause[0] == str(position_x) and str_clause[1] == str(position_y):
                matches += 1

        assert matches != 0, f'Invalid end result! No result for position [{position_x}, {position_y}]'
        assert matches == 1, f'Invalid end result! More than one result for position [{position_x}, {position_y}]'

    def print_end_result(self, values):
        end_result = []
        for key in sorted(values):
            if values[key]:
                end_result.append(key)
                # print (f'{key} 0')
        
        # assert that our result is OK
        # self.validate_end_result(end_result)

    def create_metrics_container(self):
        result = {
            constants.SPLITS_KEY: 0,
            constants.BACKTRACKS_KEY: 0,
            constants.UNIT_CLAUSES_KEY: 0,
            constants.PURE_LITERALS_KEY: 0,
            constants.TIMER1_KEY: 0,
            constants.TIMER2_KEY: 0,
            constants.TIMER3_KEY: 0,
            constants.TIMER4_KEY: 0,
            constants.TIMER5_KEY: 0
        }

        return result

    def print_metrics(self):
        print("----------------------------------")
        print("metrics result:")
        print(f' - number of splits: {self.metrics[constants.SPLITS_KEY]}')
        print(f' - number of backtracks: {self.metrics[constants.BACKTRACKS_KEY]}')
        print(f' - number of unit clauses: {self.metrics[constants.UNIT_CLAUSES_KEY]}')
        print(f' - number of pure literals: {self.metrics[constants.PURE_LITERALS_KEY]}')
        print()
        
        # timers metrics
        print(f' - timer1: {self.metrics[constants.TIMER1_KEY]} seconds')
        print(f' - timer2: {self.metrics[constants.TIMER2_KEY]} seconds')
        print(f' - timer3: {self.metrics[constants.TIMER3_KEY]} seconds')
        print(f' - timer4: {self.metrics[constants.TIMER4_KEY]} seconds')
        print(f' - timer5: {self.metrics[constants.TIMER5_KEY]} seconds')

        print(f' - total game solving time: {self.metrics[constants.GAMETIME_KEY]} seconds')
        
        print("----------------------------------")