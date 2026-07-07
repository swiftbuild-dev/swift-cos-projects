# Stopwatch GUI

## 🚀 Core Functionality
A desktop stopwatch application where you can Start, Pause, and Reset a timer. You can also record lap times while the clock is running. The app uses a smart "State Pattern" to manage what should happen when you press the button depending on whether the timer is running, paused, or idle.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like a car's steering wheel — it's a simple interface to a complex engine underneath. `TimerState` defines a strict rule: *any state must know how to handle a start/stop button press*, but leaves the actual logic to each specific state.

```python
# TimerState is the abstract blueprint. It says:
# "Every state MUST handle a button press — but each state does it differently."
class TimerState(ABC):
    @abstractmethod
    def handle_start_stop(self, context: 'Stopwatch') -> None:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting their parent's name — they start with something and build on it. `IdleState`, `RunningState`, and `PausedState` all inherit from `TimerState`, getting its structure for free and only defining their own unique button-press behavior.

```python
# IdleState inherits from TimerState and adds its own specific action:
# when pressed while idle, start the timer.
class IdleState(TimerState):
    def handle_start_stop(self, context: 'Stopwatch') -> None:
        context._start_time = time.time() - context._elapsed_seconds
        context._set_state(RunningState())
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism is the star of this project. When you press the button, the `Stopwatch` calls `handle_start_stop()` on whatever state it currently holds. It doesn't check "am I running or paused?" — the state object itself knows what to do.

```python
def start_stop(self) -> None:
    # This single line triggers completely different behavior
    # depending on whether the state is Idle, Running, or Paused.
    self._state.handle_start_stop(self)
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is like locking valuables in a safe. All the internal variables (`_elapsed_seconds`, `_start_time`, `_laps`, `_state`) are private. The UI cannot directly change them — it must use the public methods like `start_stop()`, `reset()`, and `record_lap()`.

```python
class Stopwatch:
    def __init__(self):
        # All private! The underscore means "don't access this from outside."
        self._elapsed_seconds: float = 0.0
        self._start_time: float = 0.0
        self._laps: List[float] = []
        self._state: TimerState = IdleState()
```
