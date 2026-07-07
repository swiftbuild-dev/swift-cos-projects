from abc import ABC, abstractmethod

class Question(ABC):
    # Abstraction: We define a template (Question) that guarantees any subclass
    # will have an is_correct() method, hiding the complexity of how grading works.
    def __init__(self, text: str, options: list[str]):
        self.text = text
        self.options = options

    @abstractmethod
    def is_correct(self, selected_answer: str) -> bool:
        pass

class SingleAnswerQuestion(Question):
    # Inheritance: We reuse the text and options setup from the Question base class,
    # adding only what's unique to a single-answer question.
    def __init__(self, text: str, options: list[str], correct_answer: str):
        super().__init__(text, options)
        self.correct_answer = correct_answer

    def is_correct(self, selected_answer: str) -> bool:
        # Polymorphism: SingleAnswerQuestion grades by matching an exact string.
        return selected_answer == self.correct_answer

class MultiAnswerQuestion(Question):
    # Inheritance: MultiAnswerQuestion adds a list of correct answers instead of one.
    def __init__(self, text: str, options: list[str], correct_answers: list[str]):
        super().__init__(text, options)
        self.correct_answers = correct_answers

    def is_correct(self, selected_answer: str) -> bool:
        # Polymorphism: Grades a comma-separated string of sorted answers.
        expected = ",".join(sorted(self.correct_answers))
        return selected_answer == expected

class Quiz:
    # Encapsulation: We use private variables (_score, _questions) so external code
    # can't accidentally change the score or skip questions directly.
    def __init__(self, questions: list[Question]):
        self._questions = questions
        self._score = 0
        self._current_index = 0

    def get_current_question(self) -> Question | None:
        if self._current_index < len(self._questions):
            return self._questions[self._current_index]
        return None

    def submit_answer(self, selected_answer: str) -> bool:
        q = self.get_current_question()
        if not q: return False
        
        # Polymorphism: The Quiz doesn't need to know which type of question it's grading.
        # It just calls is_correct() and the specific question object handles its own logic.
        is_right = q.is_correct(selected_answer)
        if is_right: self._score += 1
        return is_right

    def next_question(self) -> None:
        self._current_index += 1

    def get_score(self) -> int:
        return self._score

    def get_total(self) -> int:
        return len(self._questions)

def get_quiz_questions() -> list[Question]:
    return [
        SingleAnswerQuestion("What is the capital of France?", ["Berlin", "Madrid", "Paris", "Rome"], "Paris"),
        MultiAnswerQuestion("Which of these are programming languages?", ["Python", "HTML", "C++", "JPEG"], ["C++", "Python"]),
        SingleAnswerQuestion("What does OOP stand for?", ["Object-Oriented Programming", "Only One Path", "Out Of Print", "Over-Oriented Processing"], "Object-Oriented Programming"),
        MultiAnswerQuestion("Which keywords are used for loops in Python?", ["for", "loop", "while", "repeat"], ["for", "while"]),
        SingleAnswerQuestion("What keyword defines a function in Python?", ["func", "def", "function", "lambda"], "def")
    ]
