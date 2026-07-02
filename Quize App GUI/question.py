from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Question(ABC):
    """
    Abstract base class enforcing a common interface.
    WHY: This demonstrates Abstraction by defining what a question must do, 
    but leaving the specific implementation details to the subclasses.
    """
    def __init__(self, prompt: str):
        self.prompt = prompt

    @abstractmethod
    def check_answer(self, user_input: Any) -> bool:
        pass

    @abstractmethod
    def render_prompt(self) -> Dict[str, Any]:
        pass

class MultipleChoiceQuestion(Question):
    """
    WHY: Demonstrates Inheritance. We extend the Question blueprint 
    but provide logic specific to multiple choice formatting.
    """
    def __init__(self, prompt: str, options: List[str], correct_index: int):
        super().__init__(prompt)
        self.options = options
        self.correct_index = correct_index

    def check_answer(self, user_input: int) -> bool:
        # WHY: Each question type defines its own check_answer logic. 
        # This is polymorphism in action—callers don't need to know the type.
        return user_input == self.correct_index

    def render_prompt(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "options": self.options
        }
