# Todo List Project

## 🚀 Core Functionality
A simple **Todo List desktop app** built with Python. It allows users to add daily tasks and one-off tasks, mark them as completed, and delete them. It saves tasks locally so they persist when you close the app.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)
This project uses all four core principles of OOP. Here's how it works using simple terms!

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a TV remote. You press a button to change the channel, but you don't need to know how the circuits inside work. In our code, we create a basic blueprint that says *what* should happen, but leaves the *how* for later.

**Code Example:**
```python
# Task is an abstract class — it defines WHAT every task must have, but does not say HOW.
class Task(ABC):
    @abstractmethod
    def display(self) -> str:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting eye color from a parent. A new class (child) can reuse the code from an existing class (parent) so we don't have to write the same code twice.

**Code Example:**
```python
# SimpleTask inherits the shared code (id, title, prio, is_comp) from Task.
class SimpleTask(Task):
    def display(self):
        return f"{self.title}"
```

### 3. 🔄 Polymorphism — *Many forms*
Polymorphism means "many forms". It's like how you can tell a dog to "speak" and it barks, but if you tell a cat to "speak", it meows. They both understand the same command but do it differently.

**Code Example:**
```python
# In main.py, we call task.display() on ANY task without knowing if it's Simple or Recurring.
# Python picks the right version automatically.
ctk.CTkLabel(card, text=task.display())
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is like a safe. The valuables (data) are locked inside, and you can only access them if you have the key (specific methods). This prevents outside code from accidentally messing up the internal data.

**Code Example:**
```python
class TaskManager:
    def __init__(self, path="tasks.json"):
        # TaskManager hides the task list using private variables (_tasks).
        self._tasks = []
```
