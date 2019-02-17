from formula import Formula
from sat_solver import SatSolver
from sudoku_decoder import SudokuDecoder
from enums.operation import Operation

decoder = SudokuDecoder("examples/test-sudokus/1000 sudokus.txt")
# decoder = SudokuDecoder("examples/test-sudokus/damnhard.sdk.txt")

for i, game in enumerate(decoder.games):
    print(i)

    formula = Formula(Operation.AND)
    formula.add_elements_from_file("examples/sudoku-rules.txt")
    formula.add_game(game)
    # formula.add_elements_from_file("examples/sudoku-example.txt")
    # print(formula)

    sat_solver = SatSolver(formula)
    solved = sat_solver.solve()
    print(solved)

    break # for now, stick to one game only