from formula import Formula
from sat_solver import SatSolver
from enums.operation import Operation


formula = Formula(Operation.AND)
formula.add_elements_from_file("examples/sudoku-rules.txt")
formula.add_elements_from_file("examples/sudoku-example.txt")
# print(formula)

sat_solver = SatSolver(formula)
solved = sat_solver.solve()
print(solved)