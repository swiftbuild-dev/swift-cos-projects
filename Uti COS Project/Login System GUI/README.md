# Login System GUI

## 🚀 Core Functionality
A desktop login and registration application with two account types: **Standard User** and **Administrator**. You can create a new account, log in with your credentials, and see a welcome screen that shows your username and role. Passwords are securely stored as hashed values (never as plain text) in a local file.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a door handle — you pull it open without knowing the lock mechanism inside. The `Account` class defines a rule: every account type **must** have a `get_role_label()` method that returns a string describing what kind of account it is. The base class doesn't decide that label — each subclass does.

```python
# Every account type MUST be able to describe its role.
# The base class defines the rule, not the answer.
class Account(ABC):
    @abstractmethod
    def get_role_label(self) -> str:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting their parent's house. `StandardUser` and `AdminUser` both inherit the login verification (`verify_password()`) and data saving (`to_dict()`) logic from `Account`. They don't rewrite any of it — they only add their own unique role label.

```python
# Both account types inherit all the shared logic from Account.
# They only need to define what makes them different: their role name.
class StandardUser(Account):
    def get_role_label(self) -> str:
        return "Standard User"

class AdminUser(Account):
    def get_role_label(self) -> str:
        return "Administrator"
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means the same method call on different objects produces the right result automatically. After logging in, the welcome screen calls `current_user.get_role_label()` — it doesn't check if the user is Standard or Admin. It just gets the correct label back.

```python
# The welcome screen doesn't check which type the user is.
# Python calls the right get_role_label() automatically.
role_label = self.current_user.get_role_label()
# → "Standard User" or "Administrator" depending on the object
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is critical for security here. The password is **never stored as plain text**. It's converted to a hash and saved in `_password_hash` — a private variable. External code cannot read the raw hash directly. Verification only happens through the `verify_password()` method, which re-hashes the input and compares.

```python
class Account(ABC):
    def __init__(self, username: str, password_hash: str):
        self.username = username
        # _password_hash is private — it can NEVER be read from outside.
        self._password_hash = password_hash

    def verify_password(self, entered_password: str) -> bool:
        entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        return self._password_hash == entered_hash  # Compare hashes, not passwords
```
