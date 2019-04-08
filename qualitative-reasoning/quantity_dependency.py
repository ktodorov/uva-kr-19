from enums.dependency_type import DependencyType

class QuantityDependency:
    def __init__(self, dependency_type: DependencyType,
                 start_quantity,
                 end_quantity,
                 start_quantity_values=None,
                 start_quantity_gradients=None,
                 end_quantity_values=None,
                 end_quantity_gradients=None):

        self.type = dependency_type
        self.start = start_quantity
        self.end = end_quantity
        self.start_quantity_values = start_quantity_values
        self.start_quantity_gradients = start_quantity_gradients
        self.end_quantity_values = end_quantity_values
        self.end_quantity_gradients = end_quantity_gradients