# Countdown Timer GUI

## 🚀 Core Functionality
A desktop countdown timer application. You set a number of seconds for your timer, choose whether it's for an Event or a Study session, and start it. The timer counts down live on screen, and when it hits zero, it displays a customized finish message depending on the timer type you chose.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like a light switch — you flip it without knowing how electricity works inside the wall. The `Countdown` class defines a firm rule: every type of countdown **must** have an `on_finish()` method that tells the user what to show when time is up. The base class doesn't decide the message — only that one must exist.

```python
# Every countdown MUST define what happens when time runs out.
# The base class doesn't answer that — it forces subclasses to.
class Countdown(ABC):
    @abstractmethod
    def on_finish(self) -> str:
        pass  # No answer here — subclasses provide it
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child reusing their parent's tools. `EventCountdown` and `StudyCountdown` both inherit the countdown mechanics (`tick()`, `is_done()`, `_seconds_left`) from `Countdown` without rewriting any of it. They only add the one thing that makes them unique: the finish message.

```python
# EventCountdown and StudyCountdown inherit all the countdown logic.
# They each just add their own unique finish message.
class EventCountdown(Countdown):
    def on_finish(self) -> str:
        return "Time's up!"

class StudyCountdown(Countdown):
    def on_finish(self) -> str:
        return "Break time!"
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means one command produces different results depending on which object runs it. When the timer reaches zero, the app calls `timer.on_finish()`. If it's an `EventCountdown`, you see "Time's up!". If it's a `StudyCountdown`, you see "Break time!" — same line of code, different outcome.

```python
# When done, just call on_finish(). Python picks the right version.
if timer.is_done():
    display_message(timer.on_finish())
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation keeps internal data locked away and protected. The remaining seconds are stored in `_seconds_left` — a private variable. Code outside the class cannot directly change it to cheat the timer. You can only interact with it through the public `tick()` and `is_done()` methods.

```python
class Countdown(ABC):
    def __init__(self, seconds: int):
        # Private! Only the Countdown class itself should touch this.
        self._seconds_left = seconds

    def tick(self) -> int:
        if self._seconds_left > 0:
            self._seconds_left -= 1  # Controlled reduction only
        return self._seconds_left
```
