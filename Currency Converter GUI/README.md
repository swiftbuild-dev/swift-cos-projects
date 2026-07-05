# Currency Converter GUI

A robust currency converter application with a graphical user interface built using `customtkinter`. It supports converting between various currencies and implements multiple rounding behaviors.

## Key Components

### 1. `CurrencyConverter` (Base Class)
The foundation of our converter logic.
```python
class CurrencyConverter(ABC):
    def __init__(self) -> None:
        self._rates: dict[str, float] = {
            "USD": 1.00,
            "EUR": 0.92,
            # ...
        }

    @abstractmethod
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        pass
```

### 2. Converter Subclasses
Implementations that define specific calculation rules.
```python
class StandardConverter(CurrencyConverter):
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        amount_in_usd = amount / self._rates[from_currency]
        return amount_in_usd * self._rates[to_currency]
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `CurrencyConverter` class (`converter.py`).
   - **How it works**: It acts as a strict template. It says, "Any converter in this app *must* have a `convert` method," but it doesn't say *how* the math is done. This hides complex details and forces a consistent design.

2. **Inheritance**: 
   - **Where it is**: `StandardConverter` and `RoundedConverter` classes (`converter.py`).
   - **How it works**: Both of these classes inherit from `CurrencyConverter`. They automatically get the `_rates` dictionary without us having to type it out again. They reuse the common data and add their specific mathematical behaviors.

3. **Encapsulation**: 
   - **Where it is**: The `self._rates` dictionary in `CurrencyConverter` (`converter.py`).
   - **How it works**: We bundle the data (the exchange rates) inside the class and put an underscore in front of its name (`_rates`). This is a signal to other programmers: "This is protected data. Do not change it directly from outside the class!" This keeps our conversion rates safe from accidental tampering.

4. **Polymorphism**: 
   - **Where it is**: In the `perform_conversion` method in the UI (`ui.py`).
   - **How it works**: The UI has a `self.converter` variable. It doesn't care whether that converter is a `StandardConverter` or a `RoundedConverter`. It simply calls `self.converter.convert(...)` and trusts that the object will know how to calculate the result based on its own specific type.
