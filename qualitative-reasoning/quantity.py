from typing import List

from node import Node
from quantity_dependency import QuantityDependency

class Quantity(Node):
    def __init__(self, label: str, dependencies: List[QuantityDependency] = []):
        super(Quantity, self).__init__(label, 'black')
        self.dependencies = dependencies

    def add_dependencies(self, dependencies: List[QuantityDependency]):
        self.dependencies.extend(dependencies)