from abc import ABC, abstractmethod

class BaseElement(ABC):

    # @abstractmethod
    # def initialize_from_string(self, text):
    #     pass

    @abstractmethod
    def is_correct(self) -> bool:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def contains_empty_clause(self, levels_further = 1) -> bool:
        pass

    @abstractmethod
    def get_literal_string(self) -> str:
        pass

    @abstractmethod
    def get_sign(self) -> bool:
        pass
    
    @abstractmethod
    def get_number(self) -> int:
        pass

    @abstractmethod
    def has_value(self) -> bool:
        pass