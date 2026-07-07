# What This Does
This is a minimalist desktop Contact Book application. It allows you to store, view, search, and delete personal and work contacts, automatically saving data to a local JSON file.

# The Four Pillars

## Abstraction
We define a shared blueprint without worrying about the specific details yet.
```python
class Contact(ABC):
    @abstractmethod
    def display_details(self) -> str:
        pass
```

## Inheritance
Child classes reuse the base code but add their own specific fields.
```python
class PersonalContact(Contact):
    def __init__(self, name: str, phone: str, relationship: str):
        super().__init__(name, phone)
        self.relationship = relationship
```

## Encapsulation
The contact list is kept private so outside code can't mess with it directly.
```python
class ContactBook:
    def __init__(self, filepath: str = "contacts.json"):
        self._contacts: List[Contact] = []
```

## Polymorphism
The app displays each contact differently depending on its type, without needing `if` statements.
```python
        for contact in contacts:
            # Polymorphism: The book doesn't know if contact is Personal or Work,
            # it just calls display_details() and gets the right format back.
            details = contact.display_details()
```
