# Alarm Clock GUI

## 🚀 Core Functionality
A desktop alarm clock application. You can set a specific hour and minute for an alarm, and choose whether it should ring on Weekdays (Monday–Friday) or Weekends (Saturday–Sunday). The app continuously checks the current time in the background and triggers a notification when the alarm time matches.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a car horn — you press it and it beeps; you don't worry about the electronics. The `Alarm` class defines *what* every alarm must be able to do (decide if it should ring today via `should_ring_today()`), but it doesn't specify *how* — that's left to specific alarm types.

```python
# Every alarm type MUST decide if it rings today.
# The base Alarm class doesn't make that decision itself.
class Alarm(ABC):
    @abstractmethod
    def should_ring_today(self, current_weekday: int) -> bool:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance means a child class reuses code from its parent. Both `WeekdayAlarm` and `WeekendAlarm` inherit the `set_time()` and `check()` logic from `Alarm` — they don't need to rewrite that complex time-checking code. They only add their own simple day-of-week rule.

```python
# WeekdayAlarm gets the full time-checking logic from Alarm for free.
# It only needs to add ONE rule: only ring Monday to Friday.
class WeekdayAlarm(Alarm):
    def should_ring_today(self, current_weekday: int) -> bool:
        return current_weekday <= 4  # 0=Monday, 4=Friday
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism means the same method call works correctly on different object types. The app calls `alarm.check(current_time)` on whatever alarm is set. If it's a `WeekdayAlarm`, it rings on weekdays; if it's a `WeekendAlarm`, on weekends — the calling code never needs to check which type it is.

```python
# The UI just calls check() on the alarm.
# Whether it's a WeekdayAlarm or WeekendAlarm, the right rule applies.
if alarm.check(datetime.now()):
    trigger_notification()
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is putting data in a safe. The alarm time (`_alarm_time`) is stored as a private variable. You can't set it from outside code by accident — you must use the public `set_time(hour, minute)` method, which makes sure only valid time values get stored.

```python
class Alarm(ABC):
    def __init__(self) -> None:
        # _alarm_time is private. Use set_time() to change it safely.
        self._alarm_time = None

    def set_time(self, hour: int, minute: int) -> None:
        self._alarm_time = (hour, minute)
```
