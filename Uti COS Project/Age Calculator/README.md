# Age Calculator

## 🚀 Core Functionality
A desktop Age Calculator application where you enter a date of birth and it tells you your current age instantly. It performs date math to calculate how many years, months, and days have passed since the entered date.

> **Note:** This project is currently under development. The core UI and logic files are being set up.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)
This project is designed to demonstrate all four pillars of OOP. Here's how they will be implemented:

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like pressing a button on an elevator — you press "3" and it takes you there; you don't handle the cables yourself. In this project, a base `Person` or `AgeCalculator` class will define *what* must be done (like `calculate_age()`) without exposing the date math complexity to the outside world.

```python
# Example pattern this project follows:
class AgeCalculator(ABC):
    @abstractmethod
    def calculate_age(self) -> dict:
        """Returns a breakdown of age (years, months, days)."""
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance lets a new class reuse existing code. For example, different calculator modes (like `BasicAgeCalculator` and `DetailedAgeCalculator`) can inherit shared setup from a parent class, only adding what makes each one unique.

```python
class DetailedAgeCalculator(AgeCalculator):
    def calculate_age(self) -> dict:
        # Inherits the structure, provides a more detailed breakdown
        ...
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means calling the same method on different objects and getting the right result. The UI will call `.calculate_age()` on whichever calculator object is active — without needing to know which specific type it is.

```python
# Whether it's Basic or Detailed, the same call works:
result = calculator.calculate_age()
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation means keeping internal data safe inside the class. The birth date will be stored as a private variable so outside code can't accidentally change it — only controlled public methods will interact with it.

```python
class AgeCalculator(ABC):
    def __init__(self, birth_date):
        # Private: can't be changed from outside the class
        self._birth_date = birth_date
```
