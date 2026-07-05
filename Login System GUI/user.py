
import json
import os
import hashlib
from abc import ABC, abstractmethod
from typing import Dict, Optional

USERS_FILE = "users.json"

class Account(ABC):
    """
    Abstract base class for all account types.
    Demonstrates Abstraction: Defines the interface (get_role_label) that all subclasses must implement.
    """
    def __init__(self, username: str, password_hash: str) -> None:
        self.username = username
        # Encapsulation: _password_hash is private and only ever compared via verify_password(), never read directly.
        self._password_hash = password_hash

    @abstractmethod
    def get_role_label(self) -> str:
        """Returns a string describing the account type."""
        pass

    def verify_password(self, entered_password: str) -> bool:
        entered_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        return self._password_hash == entered_hash
    
    def to_dict(self) -> dict:
        return {"username": self.username, "password_hash": self._password_hash, "role": self.__class__.__name__}


# StandardUser and AdminUser both inherit login logic from Account and only override get_role_label \u2014 this is inheritance and polymorphism working together.
class StandardUser(Account):
    def get_role_label(self) -> str:
        return "Standard User"

class AdminUser(Account):
    def get_role_label(self) -> str:
        return "Administrator"


class UserManager:
    """Manages the collection of users, providing basic persistence."""
    def __init__(self) -> None:
        self.users: Dict[str, Account] = {}
        self.load_users()

    def load_users(self) -> None:
        if not os.path.exists(USERS_FILE):
            return
        with open(USERS_FILE, "r") as f:
            for data in json.load(f):
                user, pwd_hash, role = data["username"], data["password_hash"], data["role"]
                if role == "AdminUser":
                    self.users[user] = AdminUser(user, pwd_hash)
                else:
                    self.users[user] = StandardUser(user, pwd_hash)

    def save_users(self) -> None:
        with open(USERS_FILE, "w") as f:
            json.dump([u.to_dict() for u in self.users.values()], f, indent=4)

    def register(self, username: str, password: str, is_admin: bool) -> bool:
        if username in self.users:
            return False
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = AdminUser(username, pwd_hash) if is_admin else StandardUser(username, pwd_hash)
        self.save_users()
        return True

    def login(self, username: str, password: str) -> Optional[Account]:
        user = self.users.get(username)
        return user if user and user.verify_password(password) else None
