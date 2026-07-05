from abc import ABC, abstractmethod
from typing import List

class Question(ABC):
    def __init__(self, text: str, options: List[str], correct_answers: List[str]):
        self.text = text
        self.options = options
        self.correct_answers = correct_answers

    @abstractmethod
    def is_correct(self, selected_answer: List[str]) -> bool:
        """
        Check if the provided answer is correct.
        Uses List[str] to accommodate both single and multiple answers.
        """
        pass

class SingleAnswerQuestion(Question):
    def is_correct(self, selected_answer: List[str]) -> bool:
        # A single answer question is correct if exactly one option is selected 
        # and it matches the only correct answer.
        if len(selected_answer) != 1:
            return False
        return selected_answer[0] == self.correct_answers[0]

class MultiAnswerQuestion(Question):
    def is_correct(self, selected_answer: List[str]) -> bool:
        # A multi-answer question is correct if the set of selected options
        # exactly matches the set of correct answers.
        return set(selected_answer) == set(self.correct_answers)

class Quiz:
    def __init__(self, questions: List[Question]):
        self._questions = questions
        self._score = 0
        self._current_index = 0

    def get_current_question(self) -> Question | None:
        if self._current_index < len(self._questions):
            return self._questions[self._current_index]
        return None

    def submit_answer(self, selected_answer: List[str]) -> bool:
        question = self.get_current_question()
        if not question:
            return False
            
        correct = question.is_correct(selected_answer)
        if correct:
            self._score += 1
        return correct

    def next_question(self) -> None:
        self._current_index += 1

    def get_score(self) -> str:
        return f"Score: {self._score}/{len(self._questions)}"
        
    def get_raw_score(self) -> int:
        return self._score
        
    def get_total_questions(self) -> int:
        return len(self._questions)
        
    def restart(self) -> None:
        self._score = 0
        self._current_index = 0
