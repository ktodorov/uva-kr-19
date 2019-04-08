from typing import List

from node import Node
from quantity_space import QuantitySpace


class Quantity():
    def __init__(self, label: str, spaces: List[QuantitySpace], gradients: List[str]):
        self.label = label
        self.spaces = spaces
        self.gradients = gradients

    def __str__(self):
        return self.label
