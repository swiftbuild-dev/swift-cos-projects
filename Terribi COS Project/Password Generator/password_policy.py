import random
import string
from abc import ABC, abstractmethod
from typing import List

# Abstraction: We define a base contract that every policy must follow.
# Any policy must have a generate() method, hiding the complexity of how it's done.
class PasswordPolicy(ABC):
    @abstractmethod
    def generate(self, length: int) -> str:
        pass

# Inheritance: SimplePolicy extends the base PasswordPolicy,
# inheriting its structure while providing its own logic for simple passwords.
class SimplePolicy(PasswordPolicy):
    def generate(self, length: int) -> str:
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

# Inheritance: StrongPolicy also extends the base PasswordPolicy,
# but provides different logic to include uppercase letters and symbols.
class StrongPolicy(PasswordPolicy):
    def generate(self, length: int) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

class PasswordGenerator:
    def __init__(self):
        # Encapsulation: We hide the history list using an underscore prefix.
        # This prevents external code from directly modifying the history data.
        self._history: List[str] = []

    def create_password(self, policy: PasswordPolicy, length: int) -> str:
        # Polymorphism: The generator calls generate() without knowing if it's
        # a SimplePolicy or StrongPolicy. The correct method runs automatically.
        new_password = policy.generate(length)
        self._history.append(new_password)
        return new_password

    def get_last_password(self) -> str:
        if self._history:
            return self._history[-1]
        return ""
