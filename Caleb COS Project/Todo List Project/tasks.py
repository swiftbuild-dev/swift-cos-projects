import json, os, uuid
from abc import ABC, abstractmethod

# ─────────────────────────────────────────────
# 1. ABSTRACTION
# Task is an abstract class — it defines WHAT every task
# must have, but does not say HOW each type works.
# You cannot create a plain Task object directly.
# ─────────────────────────────────────────────
class Task(ABC):
    def __init__(self, title, prio, is_comp=False, tid=None):
        self.id = tid or str(uuid.uuid4())  # Unique ID for each task
        self.title = title                  # Task name
        self.prio = prio                    # Priority: Low, Medium, or High
        self.is_comp = is_comp             # Is this task completed?

    @abstractmethod
    def display(self) -> str:
        """Every subclass MUST implement its own display method."""
        pass

    @abstractmethod
    def get_badge(self) -> tuple:
        """Every subclass MUST return a (label, color) badge for the UI.
        This is used to demonstrate Polymorphism visually in the app."""
        pass

    def to_dict(self):
        """Converts the task to a dictionary so it can be saved to a file."""
        return {"id": self.id, "title": self.title, "prio": self.prio,
                "is_comp": self.is_comp, "type": type(self).__name__}

# ─────────────────────────────────────────────
# 2. INHERITANCE
# SimpleTask and RecurringTask both inherit the shared code
# (id, title, prio, is_comp, to_dict) from Task.
#
# 3. POLYMORPHISM
# Both classes override display() and get_badge() differently.
# In main.py, we call task.display() and task.get_badge() on ANY task
# without knowing if it's Simple or Recurring — Python picks the right
# version automatically. That's Polymorphism.
# ─────────────────────────────────────────────
class SimpleTask(Task):
    """A one-off task. Inherits from Task."""

    def display(self):
        # Polymorphism: SimpleTask's version of display()
        return f"{self.title}"

    def get_badge(self):
        # Polymorphism: returns a badge unique to SimpleTask
        return ("One-off", "#4a90d9")  # (label text, colour)

class RecurringTask(Task):
    """A task that repeats every day. Inherits from Task."""

    def display(self):
        # Polymorphism: RecurringTask's version of display()
        return f"↻  {self.title}"

    def get_badge(self):
        # Polymorphism: returns a different badge from SimpleTask
        return ("Daily", "#9b59b6")  # (label text, colour)

# ─────────────────────────────────────────────
# 4. ENCAPSULATION
# TaskManager hides the task list using private variables (_tasks, _path).
# The outside world can only interact through add(), remove(), toggle(), get_all().
# ─────────────────────────────────────────────
class TaskManager:
    def __init__(self, path="tasks.json"):
        self._path = path       # Private: path to the save file
        self._tasks = []        # Private: the internal list of tasks

        # Load tasks from file if it exists
        if os.path.exists(path):
            with open(path) as f:
                for d in json.load(f):
                    cls = RecurringTask if d["type"] == "RecurringTask" else SimpleTask
                    self._tasks.append(cls(d["title"], d["prio"], d["is_comp"], d["id"]))

    def _save(self):
        """Private method: saves all tasks to the JSON file."""
        with open(self._path, "w") as f:
            json.dump([t.to_dict() for t in self._tasks], f, indent=2)

    def add(self, task):
        """Add a new task and save."""
        self._tasks.append(task)
        self._save()

    def remove(self, tid):
        """Remove a task by its ID and save."""
        self._tasks = [t for t in self._tasks if t.id != tid]
        self._save()

    def toggle(self, tid):
        """Flip the completion status of a task and save."""
        for t in self._tasks:
            if t.id == tid:
                t.is_comp = not t.is_comp
        self._save()

    def get_all(self):
        """Return the full list of tasks."""
        return self._tasks
