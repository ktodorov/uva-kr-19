from quantity import Quantity
from quantity_space import QuantitySpace

class QuantityState:
    def __init__(self, quantity: Quantity, value: QuantitySpace, gradient: str):
        self.quantity = quantity
        self.value = value
        self.gradient = gradient
        