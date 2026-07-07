# Password Generator GUI

## 🚀 Core Functionality
A desktop password generator where you choose a password strength level (**Simple** or **Strong**) and a desired length using a slider. Click **Generate** to create a new password and **Copy to Clipboard** to copy it instantly. Your last generated password is always available to copy again.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like a coffee machine — you press a button for espresso; you don't grind the beans yourself. `PasswordPolicy` defines *what* every policy must do (have a `generate()` method) without saying *how* it builds the password. Each policy type fills in that detail.

```python
# Every policy type MUST be able to generate a password of a given length.
# The base class defines the rule, subclasses provide the logic.
class PasswordPolicy(ABC):
    @abstractmethod
    def generate(self, length: int) -> str:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance lets new classes build on existing ones. Both `SimplePolicy` and `StrongPolicy` inherit the structure from `PasswordPolicy`. They are recognized as valid policies without rewriting anything — they just each define their own character set.

```python
# SimplePolicy uses only lowercase letters and digits.
class SimplePolicy(PasswordPolicy):
    def generate(self, length: int) -> str:
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

# StrongPolicy uses letters, digits, AND symbols for more security.
class StrongPolicy(PasswordPolicy):
    def generate(self, length: int) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means calling the same method on different objects and getting different (appropriate) results. The `PasswordGenerator` calls `policy.generate(length)` without ever checking *which* policy it is. A simple or strong password comes back based on the object passed in.

```python
# The generator doesn't check "is this Simple or Strong?".
# It just calls generate() and gets the correct type of password.
def create_password(self, policy: PasswordPolicy, length: int) -> str:
    new_password = policy.generate(length)
    self._history.append(new_password)
    return new_password
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation keeps data safe inside a class. The `PasswordGenerator` stores the history of generated passwords in `_history` — a private list. Outside code cannot read or modify the history directly. You interact with it only through the provided methods.

```python
class PasswordGenerator:
    def __init__(self):
        # _history is private. No one outside this class should touch it.
        self._history: List[str] = []
```
