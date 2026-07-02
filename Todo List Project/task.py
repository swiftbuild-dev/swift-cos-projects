from abc import ABC, abstractmethod
import uuid
from typing import Dict, Any

class Task(ABC):
    """
    Abstract base class defining the common structure of a task.
    This demonstrates Abstraction by enforcing a contract on subclasses.
    """
    def __init__(self, title: str, priority: str, is_completed: bool = False, task_id: str = None):
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.priority = priority
        self.is_completed = is_completed

    @abstractmethod
    def display_info(self) -> str:
        """
        Abstract method forces subclasses to define their own display logic — 
        this is Abstraction/Polymorphism in action.
        """
        pass
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON storage."""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "is_completed": self.is_completed,
            "type": self.__class__.__name__
        }

class SimpleTask(Task):
    """
    Inherits from Task. Represents a standard one-off task.
    This demonstrates Inheritance.
    """
    def display_info(self) -> str:
        # Overrides the abstract method to provide specific text
        status = "[X]" if self.is_completed else "[ ]"
        return f"{status} {self.title} (Priority: {self.priority})"

class RecurringTask(Task):
    """
    Inherits from Task. Represents a task that repeats.
    This demonstrates Inheritance.
    """
    def display_info(self) -> str:
        # Overrides the abstract method with different text logic
        status = "[X]" if self.is_completed else "[ ]"
        return f"{status} ↻ {self.title} (Priority: {self.priority}) [Daily]"
