# Voting Poll GUI

## 🚀 Core Functionality
An interactive desktop polling application. You can create a poll with custom options and let users vote. It supports two modes: **Single Choice** (pick one option) and **Multi Choice** (pick multiple options). A live bar chart updates in real-time to display the vote counts for each option.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like an election ballot — you just mark your choice; you don't see the counting room. The `Poll` class defines *what* every poll must be able to do (record a vote via `record_vote()`), without deciding *how* votes are counted. Each subclass handles that detail itself.

```python
# Every poll type MUST have a record_vote() method.
# This base class doesn't say HOW — only that it must exist.
class Poll(ABC):
    @abstractmethod
    def record_vote(self, option: str) -> None:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting a parent's business. Both `SingleChoicePoll` and `MultiChoicePoll` inherit the `_results` dictionary and the `get_results()` method from `Poll`. They don't rewrite that shared logic — they only add their own way of recording votes.

```python
# SingleChoicePoll inherits all the poll setup from Poll,
# and only adds its own simple vote-counting logic.
class SingleChoicePoll(Poll):
    def record_vote(self, option: str) -> None:
        if option in self._results:
            self._results[option] += 1
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means the same instruction produces different behavior depending on the object. When the UI calls `poll.record_vote(option)`, it doesn't need to know if it's a Single or Multi choice poll. Each one handles the vote in its own way automatically.

```python
# Same method call — but the behavior is completely different
# depending on whether 'poll' is SingleChoicePoll or MultiChoicePoll.
poll.record_vote(selected_option)
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation prevents vote tampering. The `_results` dictionary is stored as a private variable inside the `Poll` class. Outside code cannot directly edit vote counts — it must go through `record_vote()`. The `get_results()` method returns only a safe *copy* of the data, never the original.

```python
class Poll(ABC):
    def __init__(self, options):
        # _results is private. No one can directly change the scores from outside.
        self._results = {opt: 0 for opt in options}

    def get_results(self) -> dict:
        return self._results.copy()  # Returns a copy, not the real data
```
