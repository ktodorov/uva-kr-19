from enums.operation import Operation
from literal import Literal
import utils
from base_element import BaseElement
from exceptions.unsatisfiable_error import UnsatisfiableError
import copy
from collections import Counter

class Formula(BaseElement):

    def __init__(self, operation):
        self.elements = []
        self.operation = operation
        self.removed_elements = []

        utils.timer1 = 0
        utils.timer2 = 0
        utils.timer3 = 0
        utils.timer4 = 0
        
    def add_elements_from_file(self, file_name):
        file = open(file_name, "r")
        
        # next(file) # skip first line

        # read every clause until we get 0, then go to the next line
        for line in file:
            current_line_formula = line.split("\n")[0]
            if current_line_formula.startswith('p cnf'):
                continue

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
        utils.cache_dict[element.get_full_number()] += 1
    
    def add_elements(self, elements):
        for element in elements:
            self.add_element(element)
            
    def remove_elements(self, elements):
        for element in elements:
            self.elements.remove(element)
            utils.cache_dict[element.get_full_number()] -= 1

    def get_elements_from_string(self, text):
        formula_strings = text.split(" ")
        elements = []

        for formula_string in formula_strings:
            if formula_string == '' or formula_string == text:
                continue

            if utils.is_digit(formula_string):
                if (int(formula_string) == 0):
                    break

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
        if len(self.elements) == 0:
            return False

        if self.operation == Operation.AND:
            for element in self.elements:
                if not element.is_correct():
                    if element.has_value():
                        return False
                        # raise UnsatisfiableError
                
                    return False
            
            return True
        elif self.operation == Operation.OR:
            all_unsatisfiable = True

            for element in self.elements:
                if element.is_correct():
                    return True
                elif not element.has_value():
                    all_unsatisfiable = False
                
            if all_unsatisfiable:
                return False

            return False

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
        elements_to_remove = []

        if self.operation == Operation.OR:
            for element in self.elements:
                check, timer = utils.measure_function(lambda: element.has_value() and not element.is_correct())
                utils.timer1 += timer
                if check:
                    elements_to_remove.append(element)
                else:
                    element.simplify()
            # pass

        elif self.operation == Operation.AND:
            for element in self.elements:
                check, timer = utils.measure_function(element.is_correct)
                utils.timer2 += timer
                if check:
                    elements_to_remove.append(element)
                else:
                    element.simplify()

        _, timer = utils.measure_function(lambda: self.removed_elements.extend(elements_to_remove))
        utils.timer3 += timer

        _, timer = utils.measure_function(lambda: self.remove_elements(elements_to_remove))
        utils.timer4 += timer

    def should_remove_element(self, element):
        if self.operation == Operation.OR:
            if not element.is_correct() and element.has_value():
                return True
        elif self.operation == Operation.AND:
            if element.is_correct():
                return True

            element.simplify()

        return False

    def reset_elements(self):
        for element in self.removed_elements:
            self.add_element(element)
        
        for element in self.elements:
            element.reset_elements()

        self.removed_elements = []

    def get_literal_string(self) -> str:
        result_string = ""
        for element in self.elements:
            result_string += element.get_literal_string() + "_"
        
        return result_string

    def get_sign(self) -> bool:
        result = True

        for element in self.elements:
            result &= element.get_sign()

        return result

    def get_all_literals(self, only_unpopulated = False) -> dict:
        result = Counter()

        for element in self.elements:
            if type(element) is Literal:
                if only_unpopulated and element.has_value():
                    continue
                    
                element_string = element.get_number()
                result[element_string] = result[element_string] + 1
            elif type(element) is Formula:
                formula_literals = element.get_all_literals(only_unpopulated)
                # add all elements from inner formula to current one
                for key, value in formula_literals.items():
                    result[key] = result[key] + value

        return result
    
    def get_clause_size(self) -> (int, dict):
        counter = 0
        ls = []

        for element in self.elements:
            if type(element) is Literal:
                ls.append(element.get_full_number())
                counter += 1

        return counter, ls

    def get_clause_literals_size(self) -> (int, dict):
        counter = 0
        ls = []

        for element in self.elements:
            if type(element) is Literal:
                ls.append(element.get_number())
                counter += 1

        return counter, ls

    def get_all_literals_by_sign(self, only_unpopulated = False) -> dict:
        result = Counter()

        for element in self.elements:
            if type(element) is Literal:
                if only_unpopulated and element.has_value():
                    continue
                    
                element_string = element.get_number()
                if not element.get_sign():
                    element_string = element_string * (-1)

                result[element_string] = result[element_string] + 1
            elif type(element) is Formula:
                formula_literals = element.get_all_literals_by_sign(only_unpopulated)
                
                # add all elements from inner formula to current one
                for key, value in formula_literals.items():
                    result[key] = result[key] + value

        return result

    def get_all_literals_binary(self, only_unpopulated = False, number_of_levels = 1) -> dict:
        if number_of_levels < 0:
            return {}

        result = Counter()

        for element in self.elements:
            if type(element) is Literal:
                if only_unpopulated and element.has_value():
                    continue
                    
                element_string = element.get_number()
                result[element_string] = 1
            elif type(element) is Formula:
                formula_literals = element.get_all_literals_binary(only_unpopulated, number_of_levels - 1)
                
                # add all elements from inner formula to current one
                for key, value in formula_literals.items():
                    result[key] = result[key] + value

        return result



    def get_unit_clauses(self) -> list:
        result = []

        if self.operation == Operation.AND:
            for element in self.elements:
                inner_unit_clauses = element.get_unit_clauses()
                if len(inner_unit_clauses) > 1:
                    continue
                
                result.extend(inner_unit_clauses)

        elif self.operation == Operation.OR:
            for element in self.elements:
                if element.is_correct():
                    return []
                
                if not element.has_value():
                    result.append(element)

            if len(result) > 1:
                return []

        return result

    def get_pure_literals(self):
        result = {}
        unpure_literals = []

        for element in self.elements:
            if element.has_value():
                continue
            
            inner_pure_literals = element.get_pure_literals()
            for pure_literal in inner_pure_literals:
                pure_literal_number = pure_literal.get_number()

                if pure_literal_number in unpure_literals:
                    continue

                if pure_literal_number not in result.keys():
                    result[pure_literal_number] = pure_literal
                elif result[pure_literal_number].get_sign() != pure_literal.get_sign():
                    del result[pure_literal_number]
                    unpure_literals.append(pure_literal_number)

        return result.values()

    def apply_values(self, values):
        for element in self.elements:
            element.apply_values(values)

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
    
    def get_full_number(self) -> int:
        return None
