from abc import ABC, abstractmethod
from datetime import date

class Person(ABC):
    def __init__(self, birth_date: date) -> None:
        # Encapsulation is used here to hide internal state.
        # External code cannot directly access or modify _birth_date.
        self._birth_date: date = birth_date
        
    def calculate_age(self) -> int:
        today: date = date.today()
        age: int = today.year - self._birth_date.year
        if (today.month, today.day) < (self._birth_date.month, self._birth_date.day):
            age -= 1
        return age
        
    def days_until_next_birthday(self) -> int:
        today: date = date.today()
        has_passed: bool = (today.month, today.day) > (self._birth_date.month, self._birth_date.day)
        next_year: int = today.year + (1 if has_passed else 0)
        try:
            next_bday = self._birth_date.replace(year=next_year)
        except ValueError:
            next_bday = date(next_year, 3, 1) # Handle leap years (Feb 29)
        return (next_bday - today).days

    @abstractmethod
    def status_message(self) -> str:
        # Abstraction creates a strict contract. All subclasses must provide 
        # their own unique implementation of this method.
        pass

class Minor(Person):
    def status_message(self) -> str:
        # Inheritance allows Minor to use calculate_age() from Person.
        # It defines status_message uniquely for minors.
        years_left: int = 18 - self.calculate_age()
        return f"You're a minor — {years_left} years to adulthood"

class Adult(Person):
    def status_message(self) -> str:
        # Inheritance lets Adult share core logic while providing 
        # a different implementation of the required abstract method.
        return "You're an adult"

if __name__ == "__main__":
    from ui import AgeCalculatorApp
    app = AgeCalculatorApp()
    app.mainloop()
