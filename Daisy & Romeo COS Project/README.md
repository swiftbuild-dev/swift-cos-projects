# Media Tracker (Movies & Books)

## 🚀 Core Functionality
A desktop app for tracking your personal media library. You can log Movies and Books you've watched or read, give them a star rating (1–5), and delete entries you no longer need. Your list is automatically saved so it's still there next time you open the app.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using an ATM — you press buttons to get cash without knowing how the bank's computers work behind the scenes. The `MediaItem` class defines a strict rule: *every item in the library must have a `display_summary()` method*, but the blueprint itself doesn't say what that summary looks like.

```python
# MediaItem is the blueprint. It says WHAT needs to exist,
# but each specific type (Movie, Book) decides HOW it looks.
class MediaItem(ABC):
    @abstractmethod
    def display_summary(self) -> str:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting their parent's skills. Both `Movie` and `Book` inherit the shared `title`, `rating`, and `to_dict()` code from `MediaItem`. They only need to add the pieces that make them unique.

```python
# Movie gets all of MediaItem's core logic for free.
# It just adds a 'director' field on top.
class Movie(MediaItem):
    def __init__(self, title: str, director: str, rating: int):
        super().__init__(title, rating)  # Call parent's setup
        self.director = director
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means calling the same method on different objects and getting the right result automatically. When the app lists your library, it calls `display_summary()` on every item. It doesn't need to know if it's a Movie or a Book — each handles it differently on its own.

```python
# The same method call, two totally different results:
movie.display_summary()  # → "🎬 Inception (dir. Nolan) — ★★★★★"
book.display_summary()   # → "📖 Harry Potter (by Rowling) — ★★★★☆"
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is like a safe. The `_items` list inside `MediaTracker` is kept private. You can't go in and randomly delete or edit items from outside — you *must* use the provided `add_item()` and `remove_item()` methods, keeping the data safe and controlled.

```python
class MediaTracker:
    def __init__(self):
        # _items is private. The underscore is a signal: "hands off!"
        self._items: List[MediaItem] = []

    def add_item(self, item: MediaItem) -> None:
        self._items.append(item)
        self._save_data()  # Auto-saves after every change
```
