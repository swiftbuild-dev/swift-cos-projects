# Stop Watch GUI

A sleek stopwatch application demonstrating the State Design Pattern. It features accurate time tracking, a laps record list, and smooth transitions between running, paused, and idle states.

## Key Components

### 1. `TimerState` (State Pattern Base)
The abstract foundation that controls how the stopwatch behaves in different states.
```python
class TimerState(ABC):
    @abstractmethod
    def handle_start_stop(self, context: 'Stopwatch') -> None:
        pass
```

### 2. The Stopwatch Controller
```python
class Stopwatch:
    def __init__(self):
        self._elapsed_seconds: float = 0.0
        self._state: TimerState = IdleState()

    def start_stop(self) -> None:
        self._state.handle_start_stop(self)
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `TimerState` base class (`stopwatch.py`).
   - **How it works**: It hides the complicated details of what a stopwatch does when you press the "start/stop" button. It just provides a simple `handle_start_stop()` method that all state objects must use, creating a clean contract.

2. **Inheritance**: 
   - **Where it is**: `IdleState`, `RunningState`, and `PausedState` classes (`stopwatch.py`).
   - **How it works**: All three of these specific states inherit from the main `TimerState` class. They reuse the same interface but provide their own unique behavior for what should happen when the button is pressed (e.g., transitioning from Running to Paused).

3. **Encapsulation**: 
   - **Where it is**: The `Stopwatch` class (`stopwatch.py`).
   - **How it works**: Internal variables like `_elapsed_seconds`, `_start_time`, and `_state` are protected. You can't reach in from the UI and magically change the stopwatch to read 10 hours. You must use the provided public methods like `start_stop()` or `reset()` to interact with the timer safely.

4. **Polymorphism**: 
   - **Where it is**: The `start_stop()` method in the `Stopwatch` class.
   - **How it works**: When you click the start/stop button, the stopwatch calls `self._state.handle_start_stop(self)`. It doesn't use `if/else` statements to figure out if the timer is running or paused. The current state object (whatever it happens to be) automatically knows what to do!
