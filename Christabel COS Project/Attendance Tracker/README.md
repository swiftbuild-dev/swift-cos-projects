# Attendance Tracker

## 🚀 Core Functionality
A desktop application that helps teachers or administrators track student attendance. You can mark students as present or absent for the day, and it calculates and displays their overall attendance percentage based on saved records.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)
This project uses all four core principles of OOP. Here's how it works using simple terms!

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a TV remote. You press a button to change the channel, but you don't need to know how the circuits inside work. In our code, we create a basic blueprint that says *what* should happen, but leaves the *how* for later.

**Code Example:**
```python
# We define a base template with a strict contract. Any type of record MUST have a status_label.
class AttendanceRecord(ABC):
    @abstractmethod
    def status_label(self) -> str:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting eye color from a parent. A new class (child) can reuse the code from an existing class (parent) so we don't have to write the same code twice.

**Code Example:**
```python
# PresentRecord inherits the basic properties (student_name, date_str) from AttendanceRecord.
class PresentRecord(AttendanceRecord):
    def status_label(self) -> str:
        return "✅ Present"
```

### 3. 🔄 Polymorphism — *Many forms*
Polymorphism means "many forms". It's like how you can tell a dog to "speak" and it barks, but if you tell a cat to "speak", it meows. They both understand the same command but do it differently.

**Code Example:**
```python
# Calling status_label() without knowing if it's PresentRecord or AbsentRecord.
# The UI doesn't care about the exact subclass type, it just trusts the method exists.
status_text = record.status_label()
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is like a safe. The valuables (data) are locked inside, and you can only access them if you have the key (specific methods). This prevents outside code from accidentally messing up the internal data.

**Code Example:**
```python
class AttendanceTracker:
    def __init__(self, file_path: str = "attendance.json"):
        # The tracker protects its internal list of records by making it private (_records).
        self._records: List[AttendanceRecord] = []
```
