from formula import Formula
from exceptions.unsatisfiable_error import UnsatisfiableError
import utils
import copy
import time
from collections import defaultdict

class SatSolver:
    def __init__(self, formula: Formula):
        self.formula = formula
        self.timer1 = 0
        self.timer2 = 0
        self.timer3 = 0
        self.timer4 = 0

    def solve(self) -> bool:
        if self.formula.is_empty():
            return True

        current_values = defaultdict(lambda: None)

        result = self.solve_using_values(current_values)

        print(f'timer1 - {self.timer1}')
        print(f'timer2 - {self.timer2}')
        print(f'timer3 - {self.timer3}')
        print(f'timer4 - {self.timer4}')

        return result

    def solve_using_values(self, values):
        # apply current values to the literals
        start = time.time()
        self.formula.apply_values(values)
        end = time.time()
        self.timer1 += (end - start)

        # if the formula is correct, we stop here
        start = time.time()
        if self.formula.is_correct():
            self.print_end_result(values)
            return True

        end = time.time()
        self.timer2 += (end - start)
        
        # simplify the formula
        self.formula.simplify()

        # take all unit clauses - those that can be only one value
        # and assign them a value
        start = time.time()
        unit_clauses = self.formula.get_unit_clauses()
        end = time.time()
        self.timer3 += (end - start)

        if unit_clauses:
            start = time.time()
            
            # if we have any unit clauses that are the same literal but require
            # opposite values, we abort the current iteration as it is invalid
            if (any(
                any(
                    l2.get_number() == l1.get_number() and 
                    l2.get_sign() != l1.get_sign() 
                    for l2 
                    in unit_clauses)
                for l1 
                in unit_clauses)):
                self.formula.reset_elements()
                return False

            end = time.time()
            self.timer4 += (end - start)

            new_values = copy.deepcopy(values)
            for single_literal in unit_clauses:
                literal_string = single_literal.get_number()
                new_values[literal_string] = single_literal.get_sign()
                
            # try to solve with the new values
            # if we fail, we must not forget to reset the elements 
            # which were changed during the current iteration
            result = self.solve_using_values(new_values)
            if not result:
                self.formula.reset_elements()
            
            return result

        # get all pure literals and assign them values
        # then try to solve with the new values
        pure_literals = self.formula.get_pure_literals()
        if pure_literals:
            new_values = copy.deepcopy(values)
            
            for pure_literal in pure_literals:
                new_values[pure_literal.get_number()] = pure_literal.get_sign() 

            result = self.solve_using_values(new_values)
            if not result:
                self.formula.reset_elements()
            
            return result

        # if we have no remaining literals, then we have solved the task
        first_non_set_literal = self.get_first_available_literal(values)
        if not first_non_set_literal:
            if self.formula.is_correct():
                self.print_end_result(values)
                return True
            else:
                self.formula.reset_elements()
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
        return False

    def get_first_available_literal(self, values):
        for key, value in values.items():
            if value == None:
                return key

    def validate_end_result(self, truth_clauses):
        for i in range(1, 10):
            for j in range(1, 10):
                self.validate_end_result_clause(truth_clauses, i, j)
                
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
                print (f'{key} 0')
        
        # assert that our result is OK
        self.validate_end_result(end_result)