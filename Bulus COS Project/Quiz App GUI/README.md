# Multiple-Choice Quiz App

## What This Does
This is a simple desktop quiz application built with Python and CustomTkinter. It presents users with a mix of single-answer and multi-answer questions, providing immediate visual feedback upon submission. The app keeps a running score and displays the final result at the end, demonstrating core Object-Oriented Programming principles in action.

## The Four Pillars

### Abstraction
We define a base template that guarantees all question types have an `is_correct` method, hiding the specific grading complexity from the rest of the app.
```python
class Question(ABC):
    def __init__(self, text: str, options: list[str]):
        self.text = text
        self.options = options

    @abstractmethod
    def is_correct(self, selected_answer: str) -> bool:
        pass
```

### Inheritance
Subclasses reuse the core attributes from the base `Question` class, adding only the specific properties they need (like `correct_answer`).
```python
class SingleAnswerQuestion(Question):
    def __init__(self, text: str, options: list[str], correct_answer: str):
        super().__init__(text, options)
        self.correct_answer = correct_answer
```

### Encapsulation
The `Quiz` class hides its internal state, forcing external code to use specific methods rather than allowing direct manipulation of the score or question list.
```python
class Quiz:
    def __init__(self, questions: list[Question]):
        self._questions = questions
        self._score = 0
        self._current_index = 0
```

### Polymorphism
The app can grade any type of question without checking what kind it is, because each question class implements its own unique version of `is_correct()`.
```python
    def submit_answer(self, selected_answer: str) -> bool:
        q = self.get_current_question()
        if not q: return False
        
        is_right = q.is_correct(selected_answer)
        if is_right: self._score += 1
        return is_right
```
