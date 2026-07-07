from abc import ABC, abstractmethod
import uuid

# Abstraction: We define a base blueprint (Transaction) that hides complex details
# and enforces that any subclass MUST have an `apply_to_balance` method.
class Transaction(ABC):
    def __init__(self, description: str, amount: float, t_id: str = None):
        self.description = description
        self.amount = amount
        self.id = t_id if t_id else str(uuid.uuid4())

    @abstractmethod
    def apply_to_balance(self, current_balance: float) -> float:
        pass

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "type": self.__class__.__name__
        }

# Inheritance: Income builds upon Transaction, reusing its __init__ and to_dict,
# while providing its own specific implementation for apply_to_balance.
class Income(Transaction):
    def apply_to_balance(self, current_balance: float) -> float:
        return current_balance + self.amount

# Inheritance: Expense also builds upon Transaction but behaves differently.
class Expense(Transaction):
    def apply_to_balance(self, current_balance: float) -> float:
        return current_balance - self.amount
