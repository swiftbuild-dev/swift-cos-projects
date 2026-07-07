# Contact Book GUI

## 🚀 Core Functionality
This is a minimalist desktop Contact Book application. It allows you to store, view, search, and delete personal and work contacts, automatically saving data to a local JSON file.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)
This project uses all four core principles of OOP. Here's how it works using simple terms!

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a TV remote. You press a button to change the channel, but you don't need to know how the circuits inside work. In our code, we create a basic blueprint that says *what* should happen, but leaves the *how* for later.

**Code Example:**
```python
# We define what a contact should do (display details) but leave the how to subclasses.
class Contact(ABC):
    @abstractmethod
    def display_details(self) -> str:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting eye color from a parent. A new class (child) can reuse the code from an existing class (parent) so we don't have to write the same code twice.

**Code Example:**
```python
# PersonalContact inherits from Contact and adds a 'relationship' field.
class PersonalContact(Contact):
    def __init__(self, name: str, phone: str, relationship: str):
        super().__init__(name, phone)
        self.relationship = relationship
```

### 3. 🔄 Polymorphism — *Many forms*
Polymorphism means "many forms". It's like how you can tell a dog to "speak" and it barks, but if you tell a cat to "speak", it meows. They both understand the same command but do it differently.

**Code Example:**
```python
# The book doesn't know if contact is Personal or Work,
# it just calls display_details() and gets the right format back automatically.
for contact in contacts:
    details = contact.display_details()
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is like a safe. The valuables (data) are locked inside, and you can only access them if you have the key (specific methods). This prevents outside code from accidentally messing up the internal data.

**Code Example:**
```python
class ContactBook:
    def __init__(self, filepath: str = "contacts.json"):
        # The underscore means _contacts is private and hidden from outside.
        self._contacts: List[Contact] = []
```
