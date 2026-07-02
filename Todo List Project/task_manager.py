import json
import os
from typing import List
from task import Task, SimpleTask, RecurringTask

class TaskManager:
    """
    Manages the collection of tasks.
    This demonstrates Encapsulation by keeping the list of tasks private 
    and exposing only specific, controlled operations.
    """
    def __init__(self, file_path: str = "tasks.json"):
        # The underscore denotes this list is private to the class
        self._tasks: List[Task] = []
        self._file_path = file_path
        self._load_tasks()

    def add_task(self, task: Task) -> None:
        """Controlled method to modify the private task list."""
        self._tasks.append(task)
        self._save_tasks()

    def remove_task(self, task_id: str) -> None:
        """Controlled method to remove a task without exposing the list."""
        self._tasks = [t for t in self._tasks if t.id != task_id]
        self._save_tasks()

    def toggle_complete(self, task_id: str) -> None:
        """Controlled method to change task state."""
        for task in self._tasks:
            if task.id == task_id:
                task.is_completed = not task.is_completed
                self._save_tasks()
                break

    def get_all_tasks(self) -> List[Task]:
        """Returns a copy of the tasks so the internal list isn't modified directly."""
        return list(self._tasks)
        
    def get_stats(self) -> tuple[int, int, int]:
        """Returns total, completed, and pending counts."""
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.is_completed)
        return total, completed, total - completed

    def _save_tasks(self) -> None:
        """Private method handling file persistence."""
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self._tasks], f, indent=4)

    def _load_tasks(self) -> None:
        """Private method to load tasks from file on startup."""
        if not os.path.exists(self._file_path):
            return
        
        with open(self._file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for item in data:
                    # Reconstruct the proper subclass based on saved type
                    task_class = RecurringTask if item.get("type") == "RecurringTask" else SimpleTask
                    task = task_class(
                        title=item["title"],
                        priority=item["priority"],
                        is_completed=item["is_completed"],
                        task_id=item["id"]
                    )
                    self._tasks.append(task)
            except json.JSONDecodeError:
                pass
