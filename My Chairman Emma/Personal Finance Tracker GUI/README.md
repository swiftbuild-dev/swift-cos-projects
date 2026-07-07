# Personal Finance Tracker GUI

## 🚀 Core Functionality
A desktop personal finance tracker where you can log your income and expenses, view a running total balance, and delete transactions. All your data is saved automatically to a file so your records persist between sessions.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like a bank teller window — you hand over money without seeing the vault behind. The `Transaction` class defines a strict rule: every transaction (whether income or expense) **must** have an `apply_to_balance()` method. It doesn't say *how* — only that one must exist.

```python
# Every transaction MUST know how it affects the balance.
# The base class defines the rule, subclasses supply the answer.
class Transaction(ABC):
    @abstractmethod
    def apply_to_balance(self, current_balance: float) -> float:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance means a child class reuses a parent's code. Both `Income` and `Expense` inherit the `description`, `amount`, `id`, and `to_dict()` from `Transaction`. They don't repeat that code — they only add their own balance logic.

```python
# Income and Expense inherit all shared fields from Transaction.
# They only define what makes each one unique.
class Income(Transaction):
    def apply_to_balance(self, current_balance: float) -> float:
        return current_balance + self.amount  # Adds money

class Expense(Transaction):
    def apply_to_balance(self, current_balance: float) -> float:
        return current_balance - self.amount  # Subtracts money
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism is what makes the balance calculation elegant. When recalculating the total, the app loops through all transactions and calls `apply_to_balance()` on each one — without ever checking if it's an Income or Expense. Each object handles itself correctly.

```python
# The same method call works perfectly for both Income and Expense objects.
for t in self._transactions:
    self._balance = t.apply_to_balance(self._balance)
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation locks data safely inside a class. The `FinanceManager` keeps `_transactions` and `_balance` as private variables — no outside code can directly change your balance or delete transactions. You must go through the provided methods like `add_transaction()` and `remove_transaction()`.

```python
class FinanceManager:
    def __init__(self):
        # Private! Only FinanceManager's own methods can change these.
        self._transactions: List[Transaction] = []
        self._balance: float = 0.0
```
