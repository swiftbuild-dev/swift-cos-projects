# Currency Converter GUI

## 🚀 Core Functionality
A desktop currency converter that lets you type in an amount, select a source currency (e.g., USD), and a target currency (e.g., NGN), then instantly see the converted value. It supports two conversion modes: a standard precise result and a rounded result.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like a vending machine — you press a button and get a snack without needing to see the machinery inside. `CurrencyConverter` defines *what* a converter must do (have a `convert()` method) without saying *how* it calculates the result.

```python
# Any converter MUST have a convert() method.
# This class doesn't say HOW — the subclasses decide.
class CurrencyConverter(ABC):
    @abstractmethod
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting a parent's house — they get it and can then customize it. Both `StandardConverter` and `RoundedConverter` inherit the `_rates` dictionary from `CurrencyConverter` so they don't have to rewrite all the exchange rates.

```python
# StandardConverter gets _rates from its parent for free.
# It only needs to write the convert() logic.
class StandardConverter(CurrencyConverter):
    def convert(self, amount, from_currency, to_currency) -> float:
        amount_in_usd = amount / self._rates[from_currency]
        return amount_in_usd * self._rates[to_currency]
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means calling the same method on different objects and getting different (but appropriate) results. The UI calls `.convert()` on whichever converter the user picked — it doesn't need to know which one is active.

```python
# The app picks the right converter object, then calls .convert().
# Whether it's Standard or Rounded, the same line of code works.
result = selected_converter.convert(amount, from_curr, to_curr)
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation keeps data safe inside a class. The `_rates` dictionary lives inside `CurrencyConverter` with an underscore, signaling it's protected. External code should not directly change exchange rates — they're bundled safely with the logic that uses them.

```python
class CurrencyConverter(ABC):
    def __init__(self) -> None:
        # _rates is private. Only the converter's own methods should use it.
        self._rates: dict[str, float] = {
            "USD": 1.00,
            "EUR": 0.92,
            "NGN": 1500.0,
            # ...and more
        }
```
