from formula import Formula
from sat_solver import SatSolver
from sudoku_decoder import SudokuDecoder
from enums.operation import Operation
import time

decoder = SudokuDecoder("examples/test-sudokus/1000 sudokus.txt")
# decoder = SudokuDecoder("examples/test-sudokus/damnhard.sdk.txt")

start = time.time()
total_games = len(decoder.games)
number_of_solved = 0
i = 1

# decoder.games = decoder.games[2:]

for game in decoder.games:
    formula = Formula(Operation.AND)
    formula.add_game(game)
    formula.add_elements_from_file("examples/sudoku-rules.txt")

    sat_solver = SatSolver(formula) 
    solved = sat_solver.solve()
    if solved:
        number_of_solved += 1
    # break

    currently_passed_time = time.time() - start
    avg_time = currently_passed_time / (i)
    time_left = ((total_games - i) * avg_time) / 60
    print (f'\r{i}/{total_games} || solved: {number_of_solved}/{i} || avg.time: {avg_time} || approximately left: {time_left} minutes     ', end='')
    i += 1

end = time.time()
total = (end - start)

print(f'total time - {total}')