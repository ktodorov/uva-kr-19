from formula import Formula
from sat_solver import SatSolver
from enums.operation import Operation
from enums.split_method import SplitMethod
from file_saver import FileSaver
import utils
import argparse

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

utils.lambda_value = 0.45
utils.beta_value = 0.5

split_method = SplitMethod.DEFAULT
if arguments.S == "2":
    split_method = SplitMethod.MOM
elif arguments.S == "3":
    split_method = SplitMethod.TK

formula = Formula(Operation.AND)
formula.add_elements_from_file(arguments.input_file)

sat_solver = SatSolver(formula, split_method) 
solved, values = sat_solver.solve()

output_file_name = f'{arguments.input_file}.out'
file_saver = FileSaver()
if solved:
    file_saver.save_values_in_dimacs(values, output_file_name)
else:
    file_saver.save_values_in_dimacs({}, output_file_name)