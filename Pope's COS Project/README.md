# What This Does
This is a simple Voting/Poll desktop application that allows users to vote for their favorite programming language. It demonstrates core Object-Oriented Programming principles by allowing the poll to switch between single-choice and multi-choice modes seamlessly using an in-memory data structure.

# The Four Pillars

### Abstraction
The `Poll` base class uses `ABC` and `@abstractmethod` to define a blueprint, ensuring every poll type must implement the `record_vote` method.
```python
class Poll(ABC):
    @abstractmethod
    def record_vote(self, option: str) -> None:
        pass
```

### Inheritance
`SingleChoicePoll` and `MultiChoicePoll` inherit from the `Poll` base class, meaning they automatically get the initialization logic and the `get_results` method, while defining their own specific voting rules.
```python
class SingleChoicePoll(Poll):
    def record_vote(self, option: str) -> None:
        if option in self._results:
            self._results[option] += 1
```

### Encapsulation
The dictionary storing the vote counts (`self._results`) is kept private (indicated by the underscore), so external code cannot modify the votes directly; they must use the public `record_vote` and `get_results` methods.
```python
    def __init__(self, options: List[str]):
        self._results = {opt: 0 for opt in options}
        
    def get_results(self) -> dict:
        return self._results.copy()
```

### Polymorphism
When the "Submit Vote" button is clicked, the UI calls `record_vote()` on the active poll object without needing to check if it is a single-choice or multi-choice poll; the correct logic runs automatically.
```python
        # options_str is either "Python" or "Python,Java"
        # The app calls record_vote without checking the poll type.
        self.poll.record_vote(options_str)
```
