from abc import ABC, abstractmethod
from typing import List

class Poll(ABC):
    # Abstraction: Using ABC and abstractmethod ensures every poll 
    # must implement record_vote, enforcing a consistent interface.
    def __init__(self, options: List[str]):
        # Encapsulation: _results is private. External code cannot modify 
        # votes directly, protecting the integrity of the poll data.
        self._results = {opt: 0 for opt in options}

    @abstractmethod
    def record_vote(self, option: str) -> None:
        pass

    def get_results(self) -> dict:
        # Encapsulation: We provide read-only access to the results via this public method.
        return self._results.copy()


class SingleChoicePoll(Poll):
    # Inheritance: SingleChoicePoll inherits from Poll and implements its own 
    # specific behavior for record_vote.
    def record_vote(self, option: str) -> None:
        # Simple increment for a single chosen option.
        if option in self._results:
            self._results[option] += 1


class MultiChoicePoll(Poll):
    # Inheritance: MultiChoicePoll also inherits from Poll but provides a 
    # different implementation, allowing multiple comma-separated votes.
    def record_vote(self, option: str) -> None:
        # Parses comma-separated string to increment multiple options at once.
        for opt in option.split(','):
            opt = opt.strip()
            if opt in self._results:
                self._results[opt] += 1

if __name__ == "__main__":
    from ui import PollApp
    app = PollApp()
    app.mainloop()
