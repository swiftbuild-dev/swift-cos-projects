import json
import os
from typing import List, Optional, Tuple
from transaction import Transaction, Income, Expense

# Encapsulation: FinanceManager hides the raw lists and balances, providing
# controlled methods to interact with the data, preventing external corruption.
class FinanceManager:
    def __init__(self, data_file: str = "transactions.json"):
        # Private variables (_transactions, _balance) protect internal state
        self._transactions: List[Transaction] = []
        self._balance: float = 0.0
        self._data_file = data_file
        self.load_data()

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)
        # Polymorphism: We don't need to know if it's Income or Expense.
        # We just call the method and the object handles its specific logic.
        self._balance = transaction.apply_to_balance(self._balance)
        self.save_data()

    def remove_transaction(self, transaction_id: str) -> None:
        transaction = self._get_transaction_by_id(transaction_id)
        if transaction:
            self._transactions.remove(transaction)
            self._recalculate_balance()
            self.save_data()

    def get_balance(self) -> float:
        # Exposes the balance safely without allowing direct modification
        return self._balance

    def get_transactions_by_category(self, category: Optional[str] = None) -> List[Transaction]:
        if not category or category == "All":
            return self._transactions
        return [t for t in self._transactions if t.category == category]
        
    def get_totals(self) -> Tuple[float, float]:
        total_income = sum(t.amount for t in self._transactions if isinstance(t, Income))
        total_expense = sum(t.amount for t in self._transactions if isinstance(t, Expense))
        return total_income, total_expense

    def _get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        for t in self._transactions:
            if t.id == transaction_id:
                return t
        return None

    def _recalculate_balance(self) -> None:
        self._balance = 0.0
        for t in self._transactions:
            # Polymorphism again: cleanly rebuilding the balance
            self._balance = t.apply_to_balance(self._balance)

    def save_data(self) -> None:
        data = [t.to_dict() for t in self._transactions]
        with open(self._data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self) -> None:
        if not os.path.exists(self._data_file):
            return
        with open(self._data_file, 'r') as f:
            data = json.load(f)
            
        self._transactions.clear()
        for item in data:
            if item["type"] == "Income":
                t = Income(item["amount"], item["category"], item["note"], item["id"])
            else:
                t = Expense(item["amount"], item["category"], item["note"], item["id"])
            self._transactions.append(t)
        self._recalculate_balance()
