import json
from typing import List, Tuple, Any
from question import Question, MultipleChoiceQuestion

class QuizManager:
    """
    WHY: Demonstrates Encapsulation. Internal state like the score and list 
    of questions are hidden (private). The outside world can only interact 
    via controlled methods, preventing accidental data corruption.
    """
    def __init__(self):
        self._questions: List[Question] = []
        self._score: int = 0
        self._current_index: int = 0

    def load_questions(self, filepath: str) -> None:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            q = MultipleChoiceQuestion(item["prompt"], item["options"], item["correct_index"])
            self._questions.append(q)

    def submit_answer(self, user_input: Any) -> bool:
        # WHY: Polymorphism! We call check_answer without knowing the concrete class.
        current_q = self._questions[self._current_index]
        is_correct = current_q.check_answer(user_input)
        if is_correct:
            self._score += 1
        return is_correct

    def next_question(self) -> bool:
        self._current_index += 1
        return self._current_index < len(self._questions)

    def get_current_question(self) -> Question:
        return self._questions[self._current_index]

    def get_progress_text(self) -> str:
        return f"Question {self._current_index + 1} of {len(self._questions)}"

    def get_score(self) -> Tuple[int, int]:
        return self._score, len(self._questions)

    def restart(self) -> None:
        self._score = 0
        self._current_index = 0
