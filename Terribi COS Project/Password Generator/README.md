# Object-Oriented Password Generator

## What This Does
This is a lightweight desktop application that generates random passwords of customizable length. It offers two security levels ("Simple" and "Strong") and includes a copy-to-clipboard feature. The codebase is designed specifically as an educational example to demonstrate the four pillars of Object-Oriented Programming (OOP) in a clear, minimal way.

## The Four Pillars

### Abstraction
We define a template for what a password policy must do using an abstract base class, without specifying exactly how it does it.
```python
class PasswordPolicy(ABC):
    @abstractmethod
    def generate(self, length: int) -> str:
        pass
```

### Inheritance
New classes are created based on the existing `PasswordPolicy`, inheriting its structure while providing their own specific implementation for password generation.
```python
class SimplePolicy(PasswordPolicy):
    def generate(self, length: int) -> str:
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
```

### Encapsulation
The history of generated passwords is kept private inside the `PasswordGenerator` class, preventing outside code from directly modifying or breaking the internal list.
```python
class PasswordGenerator:
    def __init__(self):
        self._history: List[str] = []

    def get_last_password(self) -> str:
        if self._history:
            return self._history[-1]
        return ""
```

### Polymorphism
The generator can use any policy without knowing its exact type; it simply calls `.generate()` and the correct subclass method automatically runs.
```python
    def create_password(self, policy: PasswordPolicy, length: int) -> str:
        new_password = policy.generate(length)
        self._history.append(new_password)
        return new_password
```
