from enums.operation import Operation
from literal import Literal
import utils
from base_element import BaseElement
from exceptions.unsatisfiable_error import UnsatisfiableError

class Formula(BaseElement):

    def __init__(self, operation):
        self.elements = []
        self.operation = operation
        
    def add_elements_from_file(self, file_name):
        file = open(file_name, "r")
        next(file) # skip first line

        # read every clause until we get 0, then go to the next line
        for line in file:
            current_line_formula = line.split("0")[0] # TODO: Maybe change this?

            new_formula = Formula(Operation.OR)
            new_formula.add_elements_from_string(current_line_formula)
            self.elements.append(new_formula)

    def add_elements_from_string(self, text):
        # print(f'calling add_elements_from_string with {text}')
        formula_strings = text.split(" ")

        for formula_string in formula_strings:
            if formula_string == '':
                continue

            if utils.is_digit(formula_string):
                literal = Literal(formula_string)
                self.elements.append(literal)
            else:
                new_formula = Formula(Operation.OR)
                new_formula.add_elements_from_string(formula_string)
                self.elements.append(new_formula)

    def is_correct(self) -> bool:
        if all(element.has_value() and not element.is_correct() for element in self.elements):
            raise UnsatisfiableError()

        result = False
        if self.operation == Operation.AND:
            result = all(element.is_correct() for element in self.elements)
        elif self.operation == Operation.OR:
            result = any(element.is_correct() for element in self.elements)

        return result

    def has_value(self) -> bool:
        result = all(element.has_value() for element in self.elements)
        return result

    def is_empty(self) -> bool:
        if len(self.elements) == 0:
            return True
        
        return False

    def contains_empty_clause(self, levels_further = 1) -> bool:
        if levels_further == 0 or self.is_empty():
            return False

        for element in self.elements:
            if element.is_empty():
                return True
            
            if levels_further > 1:
                inner_empty_clauses = element.contains_empty_clause(levels_further - 1)
                if inner_empty_clauses:
                    return True

    def simplify(self):
        # if self.operation == Operation.OR:
        #     return

        current_level_elements = {}
        elements_to_remove = []

        # iterate over formula's elements
        # if we have the same element but opposite signs -> 
        # if we have OR: remove this element from current formula
        # if we have AND: formula is unsatisfiable
        
        for element in self.elements:
            if type(element) is Formula:
                element.simplify()
            
            element_string = element.get_literal_string()
            if element_string in elements_to_remove:
                continue

            if element_string in current_level_elements.keys():
                for current_level_element in current_level_elements[element_string]:
                    if current_level_element.get_sign() != element.get_sign():
                        if self.operation == Operation.AND:
                            raise UnsatisfiableError()

                        elements_to_remove.append(element_string)
                        break
            
            else:
                current_level_elements[element_string] = [element]

        # remove all duplicated or empty elements 
        self.elements = [
            element 
                for element 
                in self.elements 
            if element.get_literal_string() not in elements_to_remove 
                and not element.is_empty()]
            
    def get_literal_string(self) -> str:
        result_string = ""
        for element in self.elements:
            result_string += element.get_literal_string()
        
        return result_string

    def get_sign(self) -> bool:
        result = True

        for element in self.elements:
            result &= element.get_sign()

        return result

    def get_all_literals(self) -> dict:
        result = dict()

        for element in self.elements:
            if type(element) is Literal:
                element_string = element.get_literal_string()
                result[element_string] = result.get(element_string, 0) + 1
            elif type(element) is Formula:
                formula_literals = element.get_all_literals()
                # add all elements from inner formula to current one
                for key, value in formula_literals.items():
                    result[key] = result.get(key, 0) + value

        return result

    def get_single_literals(self) -> list:
        if self.operation == Operation.AND:
            result = []
            for element in self.elements:
                if type(element) is Formula:
                    result.extend(element.get_single_literals())
                elif type(element) is Literal:
                    result.append(element)
            
            return result
        elif self.operation == Operation.OR:
            if any(element.is_correct() for element in self.elements):
                return []
            else:
                empty_literals = list(filter(lambda element: 
                    # type(element) is Literal and 
                    not element.has_value(), self.elements))

                return empty_literals

    def apply_values(self, values):
        for element in self.elements:
            if type(element) is Formula:
                element.apply_values(values)
            elif type(element) is Literal:
                element_string = element.get_literal_string()
                if element_string in values.keys():
                    element.set_value(values[element_string])
                else:
                    element.reset_value()

    def try_solve(self, values) -> bool:
        
        # first check if it is now solved
        # if not, check if there are left any single literals
        # if there are, get them all and check if there are duplicates with different signs
        #   if there are - no solution
        #   if there are not - set all to true
        # repeat until solution or no solution

        while True:
            self.apply_values(values)

            if self.is_correct():
                print(values)
                return True
            
            single_literals = self.get_single_literals()
            if not single_literals:
                return False
            
            # Literals.Any(l => Literals.Any(l2 => l2.number == l1.number && l2.negation != l1.negation))
            if (any(
                any(
                    l2.get_number() == l1.get_number() and 
                    l2.get_sign() != l1.get_sign() 
                    for l2 
                    in single_literals)
                for l1 
                in single_literals)):
                return False

            for single_literal in single_literals:
                value_to_set = True
                if not single_literal.get_sign():
                    value_to_set = False

                values[single_literal.get_literal_string()] = value_to_set
    
    def get_number(self) -> int:
        if not self.elements:
            raise Exception("Invalid operation. Attempted to get number from formula with no elements.")

        if len(self.elements) > 1:
            raise Exception("Invalid operation. Attempted to get number from formula with more than one literal.")

        return self.elements[0].get_number()

    def __str__(self):
        result = "("

        for i, element in enumerate(self.elements):
            result += str(element)

            if i < len(self.elements) - 1:
                result += " OR " if self.operation == Operation.OR else " AND "

        result += ")"
        return result