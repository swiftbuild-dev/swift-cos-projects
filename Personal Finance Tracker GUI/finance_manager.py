import json
import os
from typing import List
from transaction import Transaction, Income, Expense

class FinanceManager:
    def __init__(self, storage_file: str = "transactions.json"):
        # Encapsulation: The transaction list and balance are private (denoted by _).
        # We control access through specific methods, preventing accidental corruption.
        self._transactions: List[Transaction] = []
        self._balance: float = 0.0
        self._storage_file = storage_file
        self._load_data()

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)
        self._recalculate_balance()
        self._save_data()

    def remove_transaction(self, t_id: str) -> None:
        self._transactions = [t for t in self._transactions if t.id != t_id]
        self._recalculate_balance()
        self._save_data()

    def get_transactions(self) -> List[Transaction]:
        return self._transactions.copy()

    def get_balance(self) -> float:
        return self._balance

    def _recalculate_balance(self) -> None:
        self._balance = 0.0
        for t in self._transactions:
            # Polymorphism: We don't check if 't' is Income or Expense.
            # We simply call apply_to_balance() and trust the object to handle it correctly.
            self._balance = t.apply_to_balance(self._balance)

    def _save_data(self) -> None:
        with open(self._storage_file, "w") as f:
            json.dump([t.to_dict() for t in self._transactions], f, indent=4)

    def _load_data(self) -> None:
        if not os.path.exists(self._storage_file): return
        with open(self._storage_file, "r") as f:
            try:
                for item in json.load(f):
                    if item["type"] == "Income":
                        self._transactions.append(Income(item["description"], item["amount"], item["id"]))
                    elif item["type"] == "Expense":
                        self._transactions.append(Expense(item["description"], item["amount"], item["id"]))
                self._recalculate_balance()
            except json.JSONDecodeError: pass
