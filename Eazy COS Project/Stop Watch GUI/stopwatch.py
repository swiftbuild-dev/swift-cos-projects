import time
from abc import ABC, abstractmethod
from typing import List

# ABSTRACTION: TimerState serves as an abstract base class (contract). 
# It hides the implementation details of what a state should do, 
# only mandating that any concrete state must implement handle_start_stop.
class TimerState(ABC):
    @abstractmethod
    def handle_start_stop(self, context: 'Stopwatch') -> None:
        pass

# INHERITANCE: IdleState, RunningState, and PausedState inherit from TimerState.
# They reuse the common interface and provide specific behaviors for their respective states.
class IdleState(TimerState):
    def handle_start_stop(self, context: 'Stopwatch') -> None:
        # Transition from Idle to Running
        context._start_time = time.time() - context._elapsed_seconds
        context._set_state(RunningState())

class RunningState(TimerState):
    def handle_start_stop(self, context: 'Stopwatch') -> None:
        # Transition from Running to Paused
        context._elapsed_seconds = time.time() - context._start_time
        context._set_state(PausedState())

class PausedState(TimerState):
    def handle_start_stop(self, context: 'Stopwatch') -> None:
        # Transition from Paused to Running
        context._start_time = time.time() - context._elapsed_seconds
        context._set_state(RunningState())

class Stopwatch:
    # ENCAPSULATION: Internal variables like _elapsed_seconds, _start_time, 
    # _laps, and _state are protected (indicated by the underscore). 
    # They cannot be modified directly from outside; state changes and 
    # interactions are strictly controlled through public methods.
    def __init__(self):
        self._elapsed_seconds: float = 0.0
        self._start_time: float = 0.0
        self._laps: List[float] = []
        self._state: TimerState = IdleState()

    def _set_state(self, new_state: TimerState) -> None:
        self._state = new_state

    def start_stop(self) -> None:
        # POLYMORPHISM: The Stopwatch delegates behavior to its current state object. 
        # It calls handle_start_stop() without needing to check `if state == "running"`. 
        # The correct behavior executes depending on the actual object type held in _state.
        self._state.handle_start_stop(self)

    def reset(self) -> None:
        if not isinstance(self._state, RunningState):
            self._elapsed_seconds = 0.0
            self._start_time = 0.0
            self._laps.clear()
            self._set_state(IdleState())

    def record_lap(self) -> None:
        if isinstance(self._state, RunningState):
            self._laps.insert(0, self.get_elapsed_time())

    def get_elapsed_time(self) -> float:
        if isinstance(self._state, RunningState):
            return time.time() - self._start_time
        return self._elapsed_seconds

    def get_laps(self) -> List[float]:
        return self._laps.copy()

    # Public helper methods so the UI can check the current state 
    # without breaking encapsulation to read the private _state object directly.
    def is_running(self) -> bool:
        return isinstance(self._state, RunningState)

    def is_idle(self) -> bool:
        return isinstance(self._state, IdleState)
