# Quiz App GUI

An interactive and educational quiz application. It supports different types of questions (single choice and multiple choice), tracks the user's score, and presents questions through a clean user interface.

## Key Components

### 1. `Question` Base Class
The foundational block for quiz questions.
```python
class Question(ABC):
    def __init__(self, text: str, options: List[str], correct_answers: List[str]):
        self.text = text
        self.options = options
        self.correct_answers = correct_answers

    @abstractmethod
    def is_correct(self, selected_answer: List[str]) -> bool:
        pass
```

### 2. Quiz Engine
```python
class Quiz:
    def submit_answer(self, selected_answer: List[str]) -> bool:
        question = self.get_current_question()
        correct = question.is_correct(selected_answer)
        if correct:
            self._score += 1
        return correct
```

## The Four Pillars of OOP in this Project

This project is a perfect example of Object-Oriented Programming (OOP). Here's how the four main pillars are used:

1. **Abstraction**: 
   - **Where it is**: The `Question` class (`question.py`).
   - **How it works**: It acts as a contract that guarantees every type of question will have an `is_correct()` method. The rest of the app doesn't have to worry about the complex logic behind grading the question; it just interacts with this clean interface.

2. **Inheritance**: 
   - **Where it is**: `SingleAnswerQuestion` and `MultiAnswerQuestion` classes (`question.py`).
   - **How it works**: They inherit the standard structure (question text, options, and correct answers) from the base `Question` class. We avoid rewriting the setup logic and only write the unique grading rules for single versus multiple choices.

3. **Encapsulation**: 
   - **Where it is**: The `Quiz` class (`question.py`).
   - **How it works**: The user's score (`self._score`) and their current question index (`self._current_index`) are protected. The UI cannot just cheat and set `score = 100`. It has to go through the `submit_answer()` method, which safely checks the answer and increments the score only if it's correct.

4. **Polymorphism**: 
   - **Where it is**: The `submit_answer` method in the `Quiz` class.
   - **How it works**: When grading an answer, the code calls `question.is_correct(selected_answer)`. It doesn't care if the question is a `SingleAnswerQuestion` or a `MultiAnswerQuestion`. Each question type knows how to grade itself, allowing the `Quiz` class to treat all questions identically.
