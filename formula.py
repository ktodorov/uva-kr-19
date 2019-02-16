from enums.operation import Operation
from literal import Literal

class Formula:

    def __init__(self, operation):
        self.elements = []
        self.operation = operation
        
    def initialize_from_file(self, file_name):
        file = open(file_name, "r")
        next(file) # skip first line

        # read every clause until we get 0, then go to the next line
        for line in file:
            current_line_formula = line.split("0")[0] # TODO: Maybe change this?

            new_formula = Formula(Operation.OR)
            new_formula.initialize_from_string(current_line_formula)
            self.elements.append(new_formula)

    def initialize_from_string(self, text):
        # print(f'calling initialize_from_string with {text}')
        formula_strings = text.split(" ")

        for formula_string in formula_strings:
            if formula_string == '':
                continue

            if formula_string.isdigit():
                literal = Literal(formula_string)
                self.elements.append(literal)
            else:
                new_formula = Formula(Operation.OR)
                new_formula.initialize_from_string(formula_string)
                self.elements.append(new_formula)

    def is_correct(self):
        for element in self.elements:
            if type(element) is Formula:
                if not element.is_correct():
                    return False
            elif type(element) is Literal:
                if not element.is_true():
                    return False
        
        return True

    def print(self):
        print("(", end='')
        for i, element in enumerate(self.elements):
            if type(element) is Formula:
                element.print()
            elif type(element) is Literal:
                element.print()

            if i < len(self.elements) - 1:
                print(" OR " if self.operation == Operation.OR else " AND ", end ='')

        print(")", end='')
        
        return True