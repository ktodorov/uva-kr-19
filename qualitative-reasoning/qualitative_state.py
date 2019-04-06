from typing import List

from quantity import Quantity
from quantity_space import QuantitySpace
from quantity_state import QuantityState


class QualitativeState:
    def __init__(self):
        self.qualitative_state_quantities = []

    def add_quantity(self, quantity: Quantity, value: QuantitySpace, gradient: str):
        quantity_state = QuantityState(quantity, value, gradient)
        self.qualitative_state_quantities.append(quantity_state)

    def add_quantity_state(self, quantity_state: QuantityState):
        self.qualitative_state_quantities.append(quantity_state)

    def get_quantities(self) -> List[QuantityState]:
        return self.qualitative_state_quantities

    def get_quantity(self, quantity_label: str) -> QuantityState:
        for quantity_state in self.qualitative_state_quantities:
            if quantity_state.quantity.label == quantity_label:
                return quantity_state

    def __eq__(self, other):
        """Overrides the default implementation"""
        if not isinstance(other, QualitativeState):
            return False

        for i, quantity in enumerate(self.get_quantities()):
            if (self.qualitative_state_quantities[i].quantity.label != other.qualitative_state_quantities[i].quantity.label
                    or self.qualitative_state_quantities[i].value.label != other.qualitative_state_quantities[i].value.label
                    or self.qualitative_state_quantities[i].gradient != other.qualitative_state_quantities[i].gradient):
                return False

        return True

    def __str__(self):
        result = '('

        for quantity in self.get_quantities():
            result = result + \
                f'({quantity.quantity.label}, {quantity.value.label}, {quantity.gradient}), '

        result = result + ')'
        return result
