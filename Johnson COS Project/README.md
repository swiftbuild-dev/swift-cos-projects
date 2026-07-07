# Basic Alarm Clock

## What This Does
This is a simple desktop alarm clock built with Python and CustomTkinter. It allows users to set alarms specifically for weekdays or weekends, visually alerting them when the time is reached.

## The Four Pillars

### Abstraction
The `Alarm` class serves as a blueprint, forcing any new alarm type to define its own logic for when it should ring by implementing the abstract method `should_ring_today()`.
```python
class Alarm(ABC):
    @abstractmethod
    def should_ring_today(self, current_weekday: int) -> bool:
        pass
```

### Inheritance
`WeekdayAlarm` and `WeekendAlarm` inherit all the time-checking functionality from the base `Alarm` class, so we don't have to rewrite the `check()` method for each specific alarm type.
```python
class WeekdayAlarm(Alarm):
    def should_ring_today(self, current_weekday: int) -> bool:
        return current_weekday <= 4
```

### Encapsulation
The internal alarm time is hidden inside the `_alarm_time` variable, and outside code can only modify it safely through the `set_time()` method.
```python
    def __init__(self) -> None:
        self._alarm_time: Optional[Tuple[int, int]] = None
        
    def set_time(self, hour: int, minute: int) -> None:
        self._alarm_time = (hour, minute)
```

### Polymorphism
The UI code doesn't need to know if it's checking a `WeekdayAlarm` or `WeekendAlarm`; it simply calls `.check()` on the active alarm, and the correct overriding logic runs automatically.
```python
        # Polymorphism: The app doesn't need to check which alarm type is active,
        # it just calls .check() and the correct method is executed.
        if self.active_alarm and not self.is_ringing:
            if self.active_alarm.check(now) and now.second == 0:
```
