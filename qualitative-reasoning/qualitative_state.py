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

    def get_quantities(self) -> List[QuantityState]:
        return self.qualitative_state_quantities

    def get_quantity(self, quantity_label: str) -> QuantityState:
        for quantity_state in self.qualitative_state_quantities:
            if quantity_state.quantity.label == quantity_label:
                return quantity_state
