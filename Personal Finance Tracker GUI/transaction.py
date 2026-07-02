from abc import ABC, abstractmethod
import uuid
from typing import Dict, Any

# Abstraction: Transaction is an abstract base class. It defines the "contract"
# that all transactions must follow, without being instantiable itself.
class Transaction(ABC):
    def __init__(self, amount: float, category: str, note: str, id: str = None):
        self.id = id or str(uuid.uuid4())
        self.amount = amount
        self.category = category
        self.note = note
        
    @abstractmethod
    def apply_to_balance(self, current_balance: float) -> float:
        # Subclasses must define how they affect the balance
        pass

    @abstractmethod
    def display_label(self) -> str:
        # Subclasses must define how their amount is displayed
        pass
        
    @abstractmethod
    def display_color(self) -> str:
        # Subclasses must define their UI color to avoid type-checking in UI
        pass
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "amount": self.amount,
            "category": self.category,
            "note": self.note
        }

# Inheritance: Income inherits from Transaction and provides concrete implementations
# for the abstract methods defined in the parent class.
class Income(Transaction):
    def apply_to_balance(self, current_balance: float) -> float:
        # Polymorphism: Income specifically adds to the balance
        return current_balance + self.amount
        
    def display_label(self) -> str:
        return f"+₦{self.amount:,.2f}"
        
    def display_color(self) -> str:
        return "#10B981" # Soft Green

# Inheritance: Expense inherits from Transaction and provides its own specific implementations.
class Expense(Transaction):
    def apply_to_balance(self, current_balance: float) -> float:
        # Polymorphism: Expense specifically subtracts from the balance
        return current_balance - self.amount
        
    def display_label(self) -> str:
        return f"-₦{self.amount:,.2f}"
        
    def display_color(self) -> str:
        return "#EF4444" # Soft Red
