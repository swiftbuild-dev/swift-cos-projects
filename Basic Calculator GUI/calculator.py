from abc import ABC, abstractmethod

# Abstraction: Common interface for all math operations
class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float: pass

# Inheritance: Subclasses provide specific math logic
class Addition(Operation):
    def execute(self, a, b): return a + b

class Subtraction(Operation):
    def execute(self, a, b): return a - b

class Multiplication(Operation):
    def execute(self, a, b): return a * b

class Division(Operation):
    def execute(self, a, b):
        if b == 0: raise ValueError("Error")
        return a / b

# Encapsulation: Calculator hides its internal state and exposes clear methods
class Calculator:
    def __init__(self):
        self._val, self._stored, self._op, self._new = "0", None, None, True
        # Polymorphism: Operations accessed uniformly via dictionary lookup
        self._ops = {"+": Addition(), "−": Subtraction(), "×": Multiplication(), "÷": Division()}

    def input_digit(self, d: str):
        if self._new: 
            self._val, self._new = ("0." if d == "." else d), False
        elif d != "." or "." not in self._val:
            self._val += d
            if self._val.startswith("0") and not self._val.startswith("0."): 
                self._val = self._val.lstrip("0") or "0"

    def set_operation(self, sym: str):
        if self._op and not self._new: self.calculate()
        self._stored, self._op, self._new = float(self._val) if self._val != "Error" else 0, self._ops.get(sym), True

    def calculate(self):
        if self._op and self._stored is not None:
            try:
                res = self._op.execute(self._stored, float(self._val))
                self._val = str(int(res)) if res.is_integer() else str(res)
            except ValueError as e: self._val = str(e)
        self._op, self._stored, self._new = None, None, True

    def clear(self):
        self._val, self._stored, self._op, self._new = "0", None, None, True

    def get_display_value(self) -> str: return self._val
