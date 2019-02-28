from formula import Formula
from sat_solver import SatSolver
from sudoku_decoder import SudokuDecoder
from enums.operation import Operation
from enums.split_method import SplitMethod
import time
import constants
from csv_saver import CSVSaver

### configuration

# how many games we want the decoder to load. None will load all
max_games = 3

# use this to change the split method
split_method = SplitMethod.DEFAULT

# how many runs of the current configuration we want. This makes sense only if the game is random
runs = 2 

# change this to load other game files
game_file_name = "examples/test-sudokus/1000 sudokus.txt"
# game_file_name = "examples/test-sudokus/damnhard.sdk.txt"

### run

decoder = SudokuDecoder(game_file_name, max_games)
total_games = len(decoder.games) * runs
number_of_solved = 0
i = 1

currently_passed_time = 0

print (f'Starting to solve games using {str(split_method.name)} splitting method:')

splits_by_run = []
backtracks_by_run = []

for _ in range(runs):
    splits = []
    backtracks = []

    for game in decoder.games:
        formula = Formula(Operation.AND)
        formula.add_game(game)
        formula.add_elements_from_file("examples/sudoku-rules.txt")

        sat_solver = SatSolver(formula, split_method) 
        solved = sat_solver.solve()
        if solved:
            number_of_solved += 1

        currently_passed_time += sat_solver.metrics[constants.GAMETIME_KEY]
        splits.append(sat_solver.metrics[constants.SPLITS_KEY])
        backtracks.append(sat_solver.metrics[constants.BACKTRACKS_KEY])

        avg_time = currently_passed_time / i
        time_left = ((total_games - i) * avg_time) / 60
        print (f'\r{i}/{total_games} || solved: {number_of_solved}/{i} || avg.time: {avg_time} || approximately left: {time_left} minutes     ', end='')
        i += 1

    splits_by_run.append(splits)
    backtracks_by_run.append(backtracks)

print(f'\nFinished. Total time - {currently_passed_time} seconds')

print(f'\rSaving statistics data... 1/2', end='')
csv_splits_saver = CSVSaver(f'data/splits_{split_method.name}.csv', splits_by_run)
csv_splits_saver.save_to_file(f'splits - {split_method.name}')

print(f'\rSaving statistics data... 2/2', end='')
csv_backtracks_saver = CSVSaver(f'data/backtracks_{split_method.name}.csv', backtracks_by_run)
csv_backtracks_saver.save_to_file(f'backtracks - {split_method.name}')

print(f'\rSaving statistics data... Done')