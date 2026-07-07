# Basic Calculator GUI

## 🚀 Core Functionality
A clean, functional desktop calculator that supports addition, subtraction, multiplication, and division. It has a display screen showing the current value, number buttons (0–9 and decimal), operator buttons, and an equals button to compute results.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a TV remote — you just press "+", you don't think about circuits. The `Operation` class defines a rule: every math operation must have an `execute(a, b)` method. It hides the *how* and just defines *what* must exist.

```python
# All we know is that any Operation can be "executed" with two numbers.
# The specific math happens inside each subclass.
class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance lets new classes reuse code from a parent. All four math operations (`Addition`, `Subtraction`, `Multiplication`, `Division`) inherit from `Operation`. They automatically qualify as valid operations without rewriting any structure.

```python
# Addition and Subtraction both inherit from Operation.
# They just fill in the specific math logic.
class Addition(Operation):
    def execute(self, a, b): return a + b

class Subtraction(Operation):
    def execute(self, a, b): return a - b
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means calling the same method on different objects and getting different results. When the user presses "=", the calculator calls `self._op.execute(a, b)` — it doesn't care if `_op` is Addition or Division. The right math happens automatically.

```python
# The Calculator stores the chosen operation and calls execute().
# It doesn't need to know WHICH operation it is — Python handles that.
result = self._op.execute(self._stored, float(self._val))
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation keeps internal data safe. The `Calculator` class stores its state (`_val`, `_stored`, `_op`, `_new`) with private underscore names. Only the `Calculator`'s own methods can change them. The UI interacts through clean public methods like `input_digit()` and `calculate()`.

```python
class Calculator:
    def __init__(self):
        # All private! The _ prefix signals these are internal data.
        self._val = "0"       # Current display value
        self._stored = None   # First number stored before an operation
        self._op = None       # Current chosen operation object
        self._new = True      # Whether next digit starts a new number
```
