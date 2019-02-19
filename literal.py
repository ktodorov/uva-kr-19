from base_element import BaseElement

class Literal(BaseElement):
    def __init__(self, number):
        int_number = int(number)
        self.negation = (int_number < 0)
        self.number = abs(int_number)
        self.value = None

    def is_correct(self) -> bool:
        return (self.negation and self.value == False) or (not self.negation and self.value)

    def has_value(self) -> bool:
        return self.value != None

    def is_empty(self) -> bool:
        return False # TODO: Make a check for empty literal?

    def contains_empty_clause(self, levels_further = 1) -> bool:
        return False

    def get_literal_string(self) -> str:
        return str(self.number)

    def get_number(self) -> int:
        return self.number

    def get_sign(self) -> bool:
        return not self.negation

    def set_value(self, value):
        self.value = value

    def apply_values(self, values):
        self.value = values[self.number]

    def get_unit_clauses(self):
        result = []

        if not self.has_value():
            result.append(self)

        return result

    def get_pure_literals(self):
        return [self]

    def simplify(self):
        pass

    def reset_value(self):
        self.value = None

    def __str__(self):
        result = ""
        if self.negation:
            result += "-"
            
        result += str(self.number)
        return result