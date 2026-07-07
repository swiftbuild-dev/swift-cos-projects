from abc import ABC, abstractmethod

# Abstraction: CurrencyConverter provides a strict template for any converter.
# It ensures all subclasses will definitely have a 'convert' method,
# without caring about exactly how they do the math.
class CurrencyConverter(ABC):
    def __init__(self) -> None:
        # Encapsulation: The _rates dictionary is bundled inside the class.
        # The underscore signals it's protected and shouldn't be modified 
        # directly by outside code, keeping the data safe.
        self._rates: dict[str, float] = {
            "USD": 1.00,
            "EUR": 0.92,
            "GBP": 0.79,
            "NGN": 1500.0,
            "JPY": 151.0,
            "CAD": 1.36,
        }

    @abstractmethod
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        pass

# Inheritance: StandardConverter takes everything from CurrencyConverter 
# (like the _rates dictionary) so we don't have to rewrite it, 
# and then provides its own specific 'convert' logic.
class StandardConverter(CurrencyConverter):
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        amount_in_usd = amount / self._rates[from_currency]
        return amount_in_usd * self._rates[to_currency]

# Inheritance: RoundedConverter also inherits the shared data, but overrides 
# the 'convert' behavior to return a neat 2-decimal rounded number.
class RoundedConverter(CurrencyConverter):
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        amount_in_usd = amount / self._rates[from_currency]
        raw_result = amount_in_usd * self._rates[to_currency]
        return round(raw_result, 2)
