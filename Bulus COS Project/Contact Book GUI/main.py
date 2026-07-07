import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any

# Abstraction: Contact is an abstract base class.
# We define what a contact should do (display details) but leave the how to subclasses.
class Contact(ABC):
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone

    @abstractmethod
    def display_details(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

# Inheritance: PersonalContact inherits from Contact and adds a 'relationship' field.
class PersonalContact(Contact):
    def __init__(self, name: str, phone: str, relationship: str):
        super().__init__(name, phone)
        self.relationship = relationship

    # Polymorphism: PersonalContact implements display_details its own way.
    def display_details(self) -> str:
        return f"{self.name} — {self.relationship} — {self.phone}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Personal",
            "name": self.name,
            "phone": self.phone,
            "relationship": self.relationship
        }

# Inheritance: WorkContact inherits from Contact and adds a 'company' field.
class WorkContact(Contact):
    def __init__(self, name: str, phone: str, company: str):
        super().__init__(name, phone)
        self.company = company

    # Polymorphism: WorkContact implements display_details differently than PersonalContact.
    def display_details(self) -> str:
        return f"{self.name} — {self.company} — {self.phone}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "Work",
            "name": self.name,
            "phone": self.phone,
            "company": self.company
        }

# Encapsulation: ContactBook hides its internal _contacts list.
# Other parts of the code must use add_contact or get_all_contacts.
class ContactBook:
    def __init__(self, filepath: str = "contacts.json"):
        self._contacts: List[Contact] = []
        self._filepath = filepath
        self._load_contacts()

    def add_contact(self, contact: Contact) -> None:
        self._contacts.append(contact)
        self._save_contacts()

    def remove_contact(self, name: str) -> None:
        self._contacts = [c for c in self._contacts if c.name.lower() != name.lower()]
        self._save_contacts()

    def get_all_contacts(self) -> List[Contact]:
        return sorted(self._contacts, key=lambda c: c.name.lower())

    def search_contacts(self, query: str) -> List[Contact]:
        query = query.lower()
        results = [c for c in self._contacts if query in c.name.lower()]
        return sorted(results, key=lambda c: c.name.lower())

    def _load_contacts(self) -> None:
        if not os.path.exists(self._filepath):
            return
        with open(self._filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                if item["type"] == "Personal":
                    self._contacts.append(
                        PersonalContact(item["name"], item["phone"], item["relationship"])
                    )
                elif item["type"] == "Work":
                    self._contacts.append(
                        WorkContact(item["name"], item["phone"], item["company"])
                    )

    def _save_contacts(self) -> None:
        with open(self._filepath, "w", encoding="utf-8") as f:
            data = [contact.to_dict() for contact in self._contacts]
            json.dump(data, f, indent=4)
