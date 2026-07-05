# Todo List Project

A practical task management application. Users can add, complete, and track tasks. The application supports different task behaviors, like simple one-off tasks and recurring tasks.

## Key Components

### 1. `Task` Base Class
The core definition of a task in the system.
```python
class Task(ABC):
    def __init__(self, title: str, priority: str, is_completed: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.priority = priority
        self.is_completed = is_completed

    @abstractmethod
    def display_info(self) -> str:
        pass
```

### 2. Task Variations
```python
class SimpleTask(Task):
    def display_info(self) -> str:
        status = "[X]" if self.is_completed else "[ ]"
        return f"{status} {self.title} (Priority: {self.priority})"

class RecurringTask(Task):
    def display_info(self) -> str:
        status = "[X]" if self.is_completed else "[ ]"
        return f"{status} ↻ {self.title} (Priority: {self.priority}) [Daily]"
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `Task` base class (`task.py`).
   - **How it works**: It sets a strict rule using the `@abstractmethod` decorator: every single task type *must* have a `display_info()` method. The rest of the app doesn't need to know how the task is formatted; it just knows the method exists.

2. **Inheritance**: 
   - **Where it is**: `SimpleTask` and `RecurringTask` classes (`task.py`).
   - **How it works**: Both of these classes inherit everything from the `Task` class (like the `title`, `priority`, and `id`). We didn't have to write the code to generate random IDs twice! They share the basic properties and only override the specific text they display.

3. **Encapsulation**: 
   - **Where it is**: The overall object structure in `Task` (`task.py`).
   - **How it works**: All the details about a specific chore (its name, ID, and priority) are neatly bundled and packaged inside a single `Task` object. The application manages "Task objects" instead of dealing with loose strings and booleans scattered everywhere.

4. **Polymorphism**: 
   - **Where it is**: The `display_info()` method across different task types.
   - **How it works**: If you have a list containing both simple tasks and recurring tasks, you can loop through the list and call `.display_info()` on all of them. The program automatically knows to add a "↻" symbol for recurring tasks and leave it off for simple tasks, all without needing messy `if` statements!
