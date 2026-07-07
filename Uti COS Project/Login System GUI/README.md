# Login System GUI

A secure authentication interface built with Python and `customtkinter`. It features role-based access control, secure password hashing, and user persistence via JSON files.

## Key Components

### 1. `Account` Base Class
The template for all users in the system.
```python
class Account(ABC):
    def __init__(self, username: str, password_hash: str) -> None:
        self.username = username
        self._password_hash = password_hash

    @abstractmethod
    def get_role_label(self) -> str:
        pass
```

### 2. User Roles
```python
class StandardUser(Account):
    def get_role_label(self) -> str:
        return "Standard User"

class AdminUser(Account):
    def get_role_label(self) -> str:
        return "Administrator"
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `Account` class (`user.py`).
   - **How it works**: It defines a blueprint for what a user account should be. By marking `get_role_label()` as an `@abstractmethod`, we guarantee that any type of account created in the future will have a way to declare its role, hiding the internal decision-making.

2. **Inheritance**: 
   - **Where it is**: `StandardUser` and `AdminUser` classes (`user.py`).
   - **How it works**: Both classes inherit from `Account`. They share the exact same logic for storing usernames, hashing passwords, and verifying logins. We don't have to rewrite the password verification code twice; they just inherit it!

3. **Encapsulation**: 
   - **Where it is**: The `self._password_hash` variable in the `Account` class (`user.py`).
   - **How it works**: The actual password hash is kept private. The rest of the application cannot just look at or change a user's password directly. Instead, they must use the `verify_password()` method, which controls the process and ensures passwords are only checked safely.

4. **Polymorphism**: 
   - **Where it is**: In the `show_welcome_screen` method in the UI (`ui.py`).
   - **How it works**: When the user logs in, the UI simply calls `self.current_user.get_role_label()`. It doesn't use `if/else` statements to check if the user is an admin or standard user; the object itself automatically returns the correct label based on its type.
