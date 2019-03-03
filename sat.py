from formula import Formula
from sat_solver import SatSolver
from enums.operation import Operation
from enums.split_method import SplitMethod
import constants
from file_saver import FileSaver
import numpy as np
import utils
import argparse

input_file = ".\\examples\\custom-example.txt"

if __name__ == '__main__':
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="simple script to demonstrate argparse usage"
    )

    # Add the positional parameter
    parser.add_argument('-S', help="The strategy to be used")
    parser.add_argument('input_file', help="The input file containing the SAT problem")

    # Parse the arguments
    arguments = parser.parse_args()

    if not arguments.input_file:
        raise Exception("Invalid input file")

utils.lambda_value = 0.3
utils.beta_value = 0.65

split_method = SplitMethod.DEFAULT
if arguments.S == 2:
    split_method = SplitMethod.MOM
elif arguments.S == 3:
    split_method = SplitMethod.OWN_HEURISTIC

formula = Formula(Operation.AND)
formula.add_elements_from_file(arguments.input_file)

sat_solver = SatSolver(formula, split_method) 
solved, values = sat_solver.solve()

file_saver = FileSaver()
file_saver.save_values_in_dimacs(values, f'{arguments.input_file}.out')