# Personal Finance Tracker GUI

A comprehensive financial management tool with a modern graphical interface. It allows users to track income and expenses, calculate overall balances, and persist data between sessions.

## Key Components

### 1. Finance Manager
The central brain that handles all data logic.
```python
class FinanceManager:
    def __init__(self, storage_file: str = "transactions.json"):
        self._transactions: List[Transaction] = []
        self._balance: float = 0.0
        self._storage_file = storage_file
        self._load_data()
        
    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)
        self._recalculate_balance()
```

### 2. Calculating the Balance
```python
def _recalculate_balance(self) -> None:
    self._balance = 0.0
    for t in self._transactions:
        self._balance = t.apply_to_balance(self._balance)
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `Transaction` base class (in `transaction.py`).
   - **How it works**: It sets a rule that all financial entries must have an `apply_to_balance` method. The main application doesn't need to know *how* an entry calculates math; it just needs to know that the entry *can* do it.

2. **Inheritance**: 
   - **Where it is**: `Income` and `Expense` classes inheriting from `Transaction`.
   - **How it works**: Both income and expenses share common traits (an ID, an amount, and a description). They inherit these shared attributes from `Transaction` so we don't have to write the same basic code twice. They only define what makes them unique (adding vs. subtracting).

3. **Encapsulation**: 
   - **Where it is**: The `FinanceManager` class (`finance_manager.py`).
   - **How it works**: The lists of transactions (`self._transactions`) and the current balance (`self._balance`) are hidden behind underscores. The UI cannot randomly modify the balance variable. If it wants to change the balance, it *must* use the `add_transaction()` method, ensuring the math is always correct.

4. **Polymorphism**: 
   - **Where it is**: The `_recalculate_balance` loop in `FinanceManager`.
   - **How it works**: The manager loops through a list of transactions. It simply calls `t.apply_to_balance(self._balance)`. It doesn't stop to ask, "Are you an income? Or an expense?" The object itself knows whether to add or subtract, making the code extremely clean and flexible.
