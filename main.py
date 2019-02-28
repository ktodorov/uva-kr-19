from formula import Formula
from sat_solver import SatSolver
from sudoku_decoder import SudokuDecoder
from enums.operation import Operation
from enums.split_method import SplitMethod
import time
import constants

decoder = SudokuDecoder("examples/test-sudokus/1000 sudokus.txt", 3)
# decoder = SudokuDecoder("examples/test-sudokus/damnhard.sdk.txt")

split_method = SplitMethod.pMOM # use this to change the split method

total_games = len(decoder.games)
number_of_solved = 0
i = 1

currently_passed_time = 0

print (f'Starting to solve games using {str(split_method)}:')

for game in decoder.games:
    formula = Formula(Operation.AND)
    formula.add_game(game)
    formula.add_elements_from_file("examples/sudoku-rules.txt")

    sat_solver = SatSolver(formula, split_method) 
    solved = sat_solver.solve()
    if solved:
        number_of_solved += 1

    currently_passed_time += sat_solver.metrics[constants.GAMETIME_KEY]

    avg_time = currently_passed_time / i
    time_left = ((total_games - i) * avg_time) / 60
    print (f'\r{i}/{total_games} || solved: {number_of_solved}/{i} || avg.time: {avg_time} || approximately left: {time_left} minutes     ', end='')
    i += 1

print(f'total time - {currently_passed_time}')
