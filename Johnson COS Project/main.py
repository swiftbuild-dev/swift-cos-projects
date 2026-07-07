from abc import ABC, abstractmethod
from typing import Tuple, Optional
from datetime import datetime

# Abstraction: We define a base template for alarms that forces subclasses to implement specific behavior.
class Alarm(ABC):
    def __init__(self) -> None:
        # Encapsulation: We hide the internal state of the alarm time from the outside world.
        self._alarm_time: Optional[Tuple[int, int]] = None
        
    @abstractmethod
    def should_ring_today(self, current_weekday: int) -> bool:
        """Returns True if the alarm should ring on the given weekday (0=Monday, 6=Sunday)."""
        pass
        
    def set_time(self, hour: int, minute: int) -> None:
        """Public interface to modify the private alarm time safely."""
        self._alarm_time = (hour, minute)
        
    def check(self, current_time: datetime) -> bool:
        """Checks if the alarm should ring right now."""
        if not self._alarm_time:
            return False
            
        current_hour = current_time.hour
        current_minute = current_time.minute
        current_weekday = current_time.weekday()
        
        # Check if the time matches and the subclass-specific day logic allows it to ring
        is_time_match = (current_hour == self._alarm_time[0] and current_minute == self._alarm_time[1])
        return is_time_match and self.should_ring_today(current_weekday)

# Inheritance: WeekdayAlarm extends the base Alarm, gaining its time-checking logic while providing specific day logic.
class WeekdayAlarm(Alarm):
    def should_ring_today(self, current_weekday: int) -> bool:
        # Monday to Friday (0 to 4)
        return current_weekday <= 4

# Inheritance: WeekendAlarm similarly builds on Alarm, but for Saturday and Sunday.
class WeekendAlarm(Alarm):
    def should_ring_today(self, current_weekday: int) -> bool:
        # Saturday and Sunday (5 and 6)
        return current_weekday >= 5

if __name__ == "__main__":
    from ui import AlarmClockApp
    app = AlarmClockApp()
    app.mainloop()
