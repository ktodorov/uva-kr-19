from typing import List

from node import Node
from quantity_space import QuantitySpace


class Quantity():
    def __init__(self, label: str, spaces: List[QuantitySpace] = []):
        self.label = label
        self.spaces = spaces
        self.gradients = ['+', '0', '-']

    def __str__(self):
        return self.label
