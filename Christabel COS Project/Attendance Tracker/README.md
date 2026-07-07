# What This Does
This is a minimalist desktop application for tracking student attendance, built with Python and CustomTkinter. It allows a user to mark students as present or absent, stores the records locally in a JSON file, and calculates real-time attendance rates while visually logging history.

# The Four Pillars

## Abstraction
Abstraction hides complex implementation details and exposes only essential features by defining a rigid contract that subclasses must follow.

```python
class AttendanceRecord(ABC):
    @abstractmethod
    def status_label(self) -> str:
        pass
```

## Inheritance
Inheritance allows new classes to adopt the properties and behaviors of existing classes, preventing duplicate code while allowing specialized modifications.

```python
class PresentRecord(AttendanceRecord):
    def status_label(self) -> str:
        return "✅ Present"
```

## Encapsulation
Encapsulation groups data and methods together while hiding the internal state (using a private attribute) to prevent unintended interference from outside code.

```python
class AttendanceTracker:
    def __init__(self, file_path: str = "attendance.json"):
        self._records: List[AttendanceRecord] = []
        
    def get_all_records(self) -> List[AttendanceRecord]:
        return list(reversed(self._records))
```

## Polymorphism
Polymorphism allows objects of different classes to be treated as if they were instances of the same class, enabling a single method call to behave differently based on the exact object type.

```python
# The UI loop processes both PresentRecord and AbsentRecord identically:
status_text = record.status_label()
```
