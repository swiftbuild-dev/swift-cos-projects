# Countdown Timer

## What This Does
A minimalist desktop countdown timer built with Python and CustomTkinter. It strictly demonstrates fundamental Object-Oriented Programming principles using a simple event and study break timer.

## The Four Pillars

### Abstraction
The `Countdown` class defines a contract with an abstract `on_finish()` method that all timers must implement.
```python
    @abstractmethod
    def on_finish(self) -> str: pass # Abstraction: enforce contract
```

### Inheritance
The `EventCountdown` and `StudyCountdown` classes reuse the core timing logic from `Countdown` while providing their own finish behaviors.
```python
class EventCountdown(Countdown): # Inheritance: reuse base behavior
    def on_finish(self) -> str: return "Time's up!"
```

### Encapsulation
The remaining time is kept private (`_seconds_left`), preventing the UI from invalidly altering the state directly, exposing only safe interaction methods like `tick()`.
```python
    def __init__(self, seconds: int):
        self._seconds_left = seconds # Encapsulation: hidden state
```

### Polymorphism
The UI code simply calls `.on_finish()` on the active timer object, and the appropriate message is returned without needing to check the object's specific type.
```python
        if self.timer.is_done():
            # Polymorphism: uniform call across different subclasses
            self.display.configure(text=self.timer.on_finish())
```
