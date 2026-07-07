# Age Calculator

## 🚀 Core Functionality
A desktop application where you enter your date of birth and instantly find out your exact age, how many days are left until your next birthday, and whether you are classified as a Minor or an Adult.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a TV remote — you press a button without needing to understand the electronics inside. Here, the `Person` class defines *what* every person must be able to do (give a `status_message`), but leaves *how* to the specific subclasses.

```python
# Every person-type class MUST provide a status_message, but the blueprint
# itself doesn't decide what that message will say.
class Person(ABC):
    @abstractmethod
    def status_message(self) -> str:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting skills from a parent. `Minor` and `Adult` both inherit the `calculate_age()` and `days_until_next_birthday()` methods from `Person` for free — no need to write them twice.

```python
# Minor gets all of Person's calculation logic automatically.
# It only needs to define what makes it *different*.
class Minor(Person):
    def status_message(self) -> str:
        years_left = 18 - self.calculate_age()
        return f"You're a minor — {years_left} years to adulthood"

class Adult(Person):
    def status_message(self) -> str:
        return "You're an adult"
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means you can call the same method on different objects and get different, appropriate results. When the UI calls `person.status_message()`, it doesn't check *which* type the person is — Python figures it out automatically.

```python
# We create either a Minor or Adult object depending on age.
# Then we call the same method on either — and get the right message each time.
person = Minor(birth_date) if age < 18 else Adult(birth_date)
message = person.status_message()  # Different result, same call!
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is like putting valuables in a safe. The `_birth_date` is stored privately inside the `Person` class. Outside code can't mess with it directly — it can only use the safe public methods like `calculate_age()`.

```python
class Person(ABC):
    def __init__(self, birth_date: date) -> None:
        # The underscore means this is private. Don't touch it from outside!
        self._birth_date: date = birth_date
```
