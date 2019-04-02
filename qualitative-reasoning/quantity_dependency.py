from enums.dependency_type import DependencyType
# from quantity import Quantity

class QuantityDependency:
    def __init__(self, dependency_type: DependencyType, start_quantity, end_quantity):

        self.type = dependency_type
        self.start = start_quantity
        self.end = end_quantity