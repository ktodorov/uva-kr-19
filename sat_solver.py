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
        start = time.time()
        self.formula.apply_values(values)
        end = time.time()
        self.timer1 += (end - start)

        elements_to_remove = self.formula.simplify()
        self.formula.remove_elements(elements_to_remove)

        start = time.time()
        try:
            if self.formula.is_correct():
                # for key in sorted(values):
                #     if values[key]:
                #         print (f'{key} 0')
                return True
        except UnsatisfiableError:
            self.formula.add_elements(elements_to_remove)
            return False

        end = time.time()
        self.timer2 += (end - start)

        start = time.time()
        unit_clauses = self.formula.get_unit_clauses()
        end = time.time()
        self.timer3 += (end - start)

        if unit_clauses:
            start = time.time()
            
            # Literals.Any(l => Literals.Any(l2 => l2.number == l1.number && l2.negation != l1.negation))
            if (any(
                any(
                    l2.get_number() == l1.get_number() and 
                    l2.get_sign() != l1.get_sign() 
                    for l2 
                    in unit_clauses)
                for l1 
                in unit_clauses)):
                # raise UnsatisfiableError()
                self.formula.add_elements(elements_to_remove)
                return False

            end = time.time()
            self.timer4 += (end - start)

            new_values = copy.deepcopy(values)
            for single_literal in unit_clauses:
                literal_string = single_literal.get_number()
                new_values[literal_string] = single_literal.get_sign()
                
                # if single_literal in literals:
                #     literals.remove(single_literal)

            result = self.solve_using_values(new_values)
            if not result:
                self.formula.add_elements(elements_to_remove)
            
            return result

        # pure literals
        pure_literals = self.formula.get_pure_literals()
        if pure_literals:
            new_values = copy.deepcopy(values)
            
            for pure_literal in pure_literals:
                new_values[pure_literal.get_number()] = pure_literal.get_sign() 

            result = self.solve_using_values(new_values)
            if not result:
                self.formula.add_elements(elements_to_remove)
            
            return result

        first_non_set_literal = self.get_first_available_literal(values)
        if not first_non_set_literal:
            self.formula.add_elements(elements_to_remove)
            return False

        new_values = copy.deepcopy(values)

        # split

        new_values[first_non_set_literal] = True
        try:
            if self.solve_using_values(new_values):
                return True
        except UnsatisfiableError:
            pass

        new_values[first_non_set_literal] = False
        try:
            if self.solve_using_values(new_values):
                return True
        except UnsatisfiableError:
            pass

        self.formula.add_elements(elements_to_remove)
        return False

    def get_first_available_literal(self, values):
        for key, value in values.items():
            if value == None:
                return key

        # raise UnsatisfiableError()