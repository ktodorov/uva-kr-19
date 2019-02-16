from formula import Formula
from enums.operation import Operation

formula = Formula(Operation.AND)
formula.initialize_from_file("examples/sudoku-example.txt")
# print(formula.is_correct())
formula.print()