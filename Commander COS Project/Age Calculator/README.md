# Age Calculator

## What This Does
This is a simple, modern desktop application that calculates a user's exact age and days remaining until their next birthday. It demonstrates fundamental Object-Oriented Programming (OOP) concepts in Python, serving as an educational portfolio project.

## The Four Pillars

### Abstraction
The `Person` abstract base class defines a strict contract by requiring all subclasses to implement a specific method without providing the implementation itself.
```python
    @abstractmethod
    def status_message(self) -> str:
        # Abstraction creates a strict contract. All subclasses must provide 
        # their own unique implementation of this method.
        pass
```

### Inheritance
Subclasses like `Minor` inherit common properties and methods from `Person` (like age calculation) while providing their own unique behaviors.
```python
class Minor(Person):
    def status_message(self) -> str:
        # Inheritance allows Minor to use calculate_age() from Person.
        years_left: int = 18 - self.calculate_age()
        return f"You're a minor — {years_left} years to adulthood"
```

### Encapsulation
Internal object state is hidden and protected from outside interference; the birth date can only be interacted with via approved public methods.
```python
    def __init__(self, birth_date: date) -> None:
        # Encapsulation is used here to hide internal state.
        self._birth_date: date = birth_date
        
    def calculate_age(self) -> int:
        # ... logic safely using self._birth_date ...
```

### Polymorphism
The application can treat different objects uniformly; it calls `.status_message()` without needing to check if the object is a `Minor` or an `Adult`.
```python
    def _display_results(self, person: Person) -> None:
        # Polymorphism is demonstrated here: we just call .status_message()
        # on the object, without needing to check if it's a Minor or an Adult.
        self.status_lbl.configure(text=person.status_message())
```
