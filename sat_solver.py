from formula import Formula
from exceptions.unsatisfiable_error import UnsatisfiableError
import copy

class SatSolver:
    def __init__(self, formula: Formula):
        self.formula = formula

    def solve(self) -> bool:
        if self.formula.is_empty():
            return True

        try:
            self.formula.simplify()
        except UnsatisfiableError:
            return False

        all_literals = self.formula.get_all_literals()
        current_values = {}
        return self.solve_using_values(list(all_literals.keys()), current_values)

    def solve_using_values(self, literals, values):
        try:
            if self.formula.try_solve(values):
                return True
        except UnsatisfiableError:
            return False

        if len(literals) == 0:
            return False
            
        first_literal = literals[0]
        new_values = copy.deepcopy(values)
        new_values[first_literal] = True
        if self.solve_using_values(literals[1:], new_values):
            return True
        
        new_values[first_literal] = False
        if self.solve_using_values(literals[1:], new_values):
            return True

        return False