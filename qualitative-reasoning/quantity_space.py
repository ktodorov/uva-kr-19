class QuantitySpace:
    def __init__(self, label: str):
        self.label = label
    
    def __str__(self):
        return self.label
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if not isinstance(other, QuantitySpace):
            return False

        return self.label == other.label