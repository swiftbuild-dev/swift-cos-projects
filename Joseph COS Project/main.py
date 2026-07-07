from abc import ABC, abstractmethod

class Countdown(ABC):
    def __init__(self, seconds: int):
        self._seconds_left = seconds # Encapsulation: hidden state
        
    def tick(self) -> int:
        if self._seconds_left > 0:
            self._seconds_left -= 1
        return self._seconds_left
        
    def is_done(self) -> bool:
        return self._seconds_left <= 0
        
    @abstractmethod
    def on_finish(self) -> str: pass # Abstraction: enforce contract

class EventCountdown(Countdown): # Inheritance: reuse base behavior
    def on_finish(self) -> str: return "Time's up!"

class StudyCountdown(Countdown):
    def on_finish(self) -> str: return "Break time!"
