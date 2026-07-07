# OOP Todo List — Python Project

A simple **Todo List desktop app** built with Python. It demonstrates all **four pillars of Object-Oriented Programming (OOP)** in a clean, minimal way.

---

## 📁 Project Structure

```
Todo List Project/
├── main.py       # The user interface (what you see on screen)
├── tasks.py      # The back-end logic (tasks & data management)
├── tasks.json    # Auto-generated: stores your saved tasks
└── README.md     # This file
```

---

## 🚀 How to Run

1. Make sure you have Python installed.
2. Install the required package:
   ```bash
   pip install customtkinter
   ```
3. Run the app:
   ```bash
   python main.py
   ```

---

## 🧠 The Four Pillars of OOP — Explained Simply

This project uses all four core principles of Object-Oriented Programming. Here's where each one appears:

---

### 1. 🔒 Abstraction — *Hide the complexity*

> **File:** `tasks.py` → `class Task(ABC)`

Abstraction means showing only what's necessary and hiding the internal details.

The `Task` class is **abstract** — it cannot be used directly. It just defines the *blueprint* that all tasks must follow. It says: *"Every task must have a `display()` method"*, but doesn't say how.

```python
class Task(ABC):
    @abstractmethod
    def display(self) -> str:
        pass  # No implementation here — subclasses decide HOW
```

---

### 2. 👪 Inheritance — *Reuse and extend*

> **File:** `tasks.py` → `SimpleTask` and `RecurringTask`

Inheritance lets a new class **reuse code from an existing class**.

Both `SimpleTask` and `RecurringTask` inherit from `Task`. They automatically get all of `Task`'s properties (`id`, `title`, `prio`, `is_comp`) without rewriting them.

```python
class SimpleTask(Task):      # Inherits from Task
    ...

class RecurringTask(Task):   # Also inherits from Task
    ...
```

---

### 3. 🔄 Polymorphism — *One interface, many behaviours*

> **File:** `tasks.py` → `display()` method in `SimpleTask` and `RecurringTask`

Polymorphism means the **same method name behaves differently** depending on the object.

Both task types have a `display()` method, but they produce different text. The app calls `task.display()` without needing to know which type it is — Python figures it out automatically.

```python
class SimpleTask(Task):
    def display(self):
        return f"{self.title} [{self.prio}]"           # Simple text

class RecurringTask(Task):
    def display(self):
        return f"↻ {self.title} [{self.prio}] — Daily" # Different text
```

---

### 4. 📦 Encapsulation — *Protect your data*

> **File:** `tasks.py` → `class TaskManager`

Encapsulation means keeping internal data **private** and only allowing access through controlled methods.

`TaskManager` stores tasks in `self._tasks` (the underscore means private). You cannot modify the list directly from outside. You must use the provided methods: `add()`, `remove()`, `toggle()`, `get_all()`.

```python
class TaskManager:
    def __init__(self):
        self._tasks = []   # Private — cannot be directly accessed outside

    def add(self, task):   # Controlled public method to add a task
        self._tasks.append(task)
        self._save()
```

---

## 🖥️ How the App Works

| File | Role |
|---|---|
| `tasks.py` | Defines what a Task is, and manages the list of tasks |
| `main.py` | Builds the window, buttons, and task cards using `customtkinter` |

**Flow when you add a task:**
1. You type a title and click **+ Add** in `main.py`
2. `main.py` creates a `SimpleTask` or `RecurringTask` object
3. It passes the object to `TaskManager.add()`
4. `TaskManager` saves it to `tasks.json` and updates the list
5. `main.py` calls `refresh()` to redraw the task cards on screen

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `customtkinter` | Modern-looking UI widgets for Python |

Install with:
```bash
pip install customtkinter
```
