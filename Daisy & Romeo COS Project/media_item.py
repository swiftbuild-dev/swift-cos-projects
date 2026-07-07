import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class MediaItem(ABC):
    def __init__(self, title: str, rating: int):
        self.title = title
        self.rating = rating

    # Abstraction: Defines a required action but hides implementation details.
    # Subclasses MUST implement how they display their summary.
    @abstractmethod
    def display_summary(self) -> str:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "rating": self.rating}

class Movie(MediaItem):
    # Inheritance: Movie reuses MediaItem's logic and adds its own (director).
    def __init__(self, title: str, director: str, rating: int):
        super().__init__(title, rating)
        self.director = director

    def display_summary(self) -> str:
        stars = "★" * self.rating + "☆" * (5 - self.rating)
        return f"🎬 {self.title} (dir. {self.director}) — {stars}"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({"type": "Movie", "director": self.director})
        return data

class Book(MediaItem):
    # Inheritance: Book extends MediaItem with an author property.
    def __init__(self, title: str, author: str, rating: int):
        super().__init__(title, rating)
        self.author = author

    def display_summary(self) -> str:
        stars = "★" * self.rating + "☆" * (5 - self.rating)
        return f"📖 {self.title} (by {self.author}) — {stars}"

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({"type": "Book", "author": self.author})
        return data

class MediaTracker:
    def __init__(self, filepath: str = "media.json"):
        self._filepath = filepath
        # Encapsulation: The _items list is private. We protect it from
        # direct outside modification, forcing use of add/remove methods.
        self._items: List[MediaItem] = []
        self._load_data()

    def add_item(self, item: MediaItem) -> None:
        self._items.append(item)
        self._save_data()

    def remove_item(self, index: int) -> None:
        if 0 <= index < len(self._items):
            self._items.pop(index)
            self._save_data()

    def get_all_items(self) -> List[MediaItem]:
        # Return a copy to maintain encapsulation of the internal list.
        return self._items[:]

    def _save_data(self) -> None:
        with open(self._filepath, 'w', encoding='utf-8') as f:
            json.dump([i.to_dict() for i in self._items], f, indent=4)

    def _load_data(self) -> None:
        if not os.path.exists(self._filepath):
            return
        with open(self._filepath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                if item.get("type") == "Movie":
                    self._items.append(Movie(item["title"], item["director"], item["rating"]))
                elif item.get("type") == "Book":
                    self._items.append(Book(item["title"], item["author"], item["rating"]))
