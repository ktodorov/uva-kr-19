from enums.dependency_type import DependencyType
# from quantity import Quantity


class QuantityDependency:
    def __init__(self, dependency_type: DependencyType,
                 start_quantity,
                 end_quantity,
                 start_quantity_space=None,
                 end_quantity_space=None):

        self.type = dependency_type
        self.start = start_quantity
        self.end = end_quantity
        self.start_space = start_quantity_space
        self.end_space = end_quantity_space
