from enums.operation import Operation
from literal import Literal
import utils
from base_element import BaseElement
from exceptions.unsatisfiable_error import UnsatisfiableError
import copy

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

            new_elements = self.get_elements_from_string(current_line_formula)
            
            # if we have more than one inner element, wrap them in another formula
            if len(new_elements) > 0:
                new_formula = Formula(Operation.OR)
                new_formula.add_elements(new_elements)
                self.add_element(new_formula)
            else:
                self.add_elements(new_elements)

    def add_game(self, game):
        for game_position in game:
            literal = Literal(game_position)
            self.add_element(literal)

    def add_element(self, element):
        self.elements.append(element)
    
    def add_elements(self, elements):
        for element in elements:
            self.elements.append(element)

    def get_elements_from_string(self, text):
        # print(f'calling get_elements_from_string with {text}')
        formula_strings = text.split(" ")
        elements = []

        for formula_string in formula_strings:
            if formula_string == '':
                continue

            if utils.is_digit(formula_string):
                literal = Literal(formula_string)
                elements.append(literal)
            else:
                
                inner_elements = self.get_elements_from_string(formula_string)
                
                # if we have more than one inner element, wrap them in another formula
                if len(inner_elements) > 0:
                    new_formula = Formula(Operation.OR)
                    new_formula.add_elements(inner_elements)
                    elements.append(new_formula)
                else:
                    elements.extend(inner_elements)

        return elements

    def is_correct(self) -> bool:
        result = False
        if self.operation == Operation.AND:
            if any(element.has_value() and not element.is_correct() for element in self.elements):
                raise UnsatisfiableError()

            result = all(element.is_correct() for element in self.elements)
        elif self.operation == Operation.OR:
            if all(element.has_value() and not element.is_correct() for element in self.elements):
                raise UnsatisfiableError()

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
        # if not all(type(element) is Literal for element in self.elements):
        if self.operation == Operation.AND:
            result = []
            for element in self.elements:
            # empty_literals = list(filter(lambda element: 
            #     # type(element) is Literal and 
            #     not element.has_value(), self.elements))
            # if len(empty_literals) > 1:
            #     return []
            
            # return empty_literals

                if type(element) is Formula:
                    inner_single_literals = element.get_single_literals()
                    if len(inner_single_literals) > 1:
                        continue
                    
                    # if element.operation == Operation.OR:
                    #     if len(inner_single_literals)
                    result.extend(inner_single_literals)
                elif type(element) is Literal:
                    if not element.has_value():
                        result.append(element)
            
            return result
        elif self.operation == Operation.OR:
            if any(element.is_correct() for element in self.elements):
                return []
            else:
                empty_literals = list(filter(lambda element: 
                    # type(element) is Literal and 
                    not element.has_value(), self.elements))
                if len(empty_literals) > 1:
                    return []

                return empty_literals
        # else:
        #     unfilled_literals = [element for element in self.elements if not element.has_value()]
        #     if len(unfilled_literals) > 1:
        #         return []
            
        #     if self.operation == Operation.AND:
        #         result = []
        #         for element in self.elements:
        #             result.append(element)
                
        #         return result
        #     elif self.operation == Operation.OR:
        #         if any(element.is_correct() for element in self.elements):
        #             return []
        #         else:
        #             empty_literals = list(filter(lambda element: 
        #                 # type(element) is Literal and 
        #                 not element.has_value(), self.elements))

        #             return empty_literals


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

        self.apply_values(values)

        if self.is_correct():
            # print all true values in DIMACS format
            for key in sorted(values):
                if values[key]:
                    print (f'{key} 0')

            return True
        
        single_literals = self.get_single_literals()
        if not single_literals:
            # return False
            all_literals = self.get_all_literals()
            all_set_literals = values.keys()
            all_non_set_literals = list(set(all_literals) - set(all_set_literals))
            if len(all_non_set_literals) == 0:
                return False

            first_non_set_literal = all_non_set_literals[0]
            new_values = copy.deepcopy(values)
            new_values[first_non_set_literal] = True
            try:
                if self.try_solve(new_values):
                    return True
            except UnsatisfiableError:
                pass

            new_values[first_non_set_literal] = False
            try:
                if self.try_solve(new_values):
                    return True
            except UnsatisfiableError:
                pass

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
            raise UnsatisfiableError()
            # return False

        new_values = copy.deepcopy(values)
        for single_literal in single_literals:
            value_to_set = True
            if not single_literal.get_sign():
                value_to_set = False

            new_values[single_literal.get_literal_string()] = value_to_set

        return self.try_solve(new_values)
    
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