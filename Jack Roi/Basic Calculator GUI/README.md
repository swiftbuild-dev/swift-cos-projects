# Basic Calculator GUI

A beautifully designed calculator application built with Python and `customtkinter`. It handles standard arithmetic operations through a clean, modern user interface while heavily relying on Object-Oriented Design principles for its core logic.

## Key Components

### 1. `Operation` (The Blueprint)
The foundational contract for any math operation.
```python
class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float: 
        pass
```

### 2. Specific Operations
Individual classes that implement actual mathematics.
```python
class Addition(Operation):
    def execute(self, a, b): return a + b

class Subtraction(Operation):
    def execute(self, a, b): return a - b
```

### 3. The Calculator Core
The engine that manages inputs and calculations.
```python
class Calculator:
    def __init__(self):
        self._val = "0"
        self._ops = {"+": Addition(), "−": Subtraction(), "×": Multiplication(), "÷": Division()}
        
    def calculate(self):
        # Executes the chosen operation seamlessly
        res = self._op.execute(self._stored, float(self._val))
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `Operation` base class (`calculator.py`).
   - **How it works**: By defining an `execute` method as an `@abstractmethod`, we guarantee that any math operation will have exactly that method. The overall calculator doesn't need to know *how* to add or subtract; it just knows every operation has an `execute()` method.

2. **Inheritance**: 
   - **Where it is**: The `Addition`, `Subtraction`, `Multiplication`, and `Division` classes (`calculator.py`).
   - **How it works**: They inherit the strict rules of the `Operation` class. Because they inherit this structure, the calculator can treat them all uniformly.

3. **Encapsulation**: 
   - **Where it is**: The variables inside the `Calculator` class, like `self._val`, `self._stored`, and `self._op` (`calculator.py`).
   - **How it works**: These variables are "protected" (indicated by the underscore). The user interface (`ui.py`) is not allowed to reach inside and directly change the number on the screen. Instead, the UI is forced to press buttons using methods like `input_digit()` and `set_operation()`, keeping the calculator's internal brain safe from bad inputs.

4. **Polymorphism**: 
   - **Where it is**: The `calculate()` method in the `Calculator` class.
   - **How it works**: When you hit the equals (`=`) sign, the calculator takes whatever operation it has saved (e.g., `Addition` or `Division`) and simply calls `self._op.execute(a, b)`. It does *not* use a messy block of `if` statements to check what the symbol is. The correct math happens automatically because the `execute()` method takes different forms depending on the object!
