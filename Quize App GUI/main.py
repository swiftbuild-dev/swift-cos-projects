import json
import os
import sys
from question import Quiz, SingleAnswerQuestion, MultiAnswerQuestion
from ui import QuizUI

def load_questions(filepath: str) -> list:
    """Loads questions from a JSON file and instantiates the correct Question objects."""
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    questions = []
    for q_data in data:
        text = q_data['text']
        options = q_data['options']
        answer = q_data['answer']
        q_type = q_data['type']
        
        if q_type == 'single':
            questions.append(SingleAnswerQuestion(text, options, answer))
        elif q_type == 'multi':
            questions.append(MultiAnswerQuestion(text, options, answer))
            
    return questions

def main():
    # File containing the questions
    questions_file = "questions.json"
    
    # Ensure working directory is correct
    if not os.path.exists(questions_file) and os.path.exists(os.path.join(os.path.dirname(__file__), questions_file)):
        questions_file = os.path.join(os.path.dirname(__file__), questions_file)

    # 1. Load data
    questions = load_questions(questions_file)
    
    if not questions:
        print("No questions found.")
        return

    # 2. Initialize Core Logic (Quiz)
    quiz = Quiz(questions)
    
    # 3. Initialize Presentation Logic (UI) and start
    app = QuizUI(quiz)
    app.mainloop()

if __name__ == "__main__":
    main()
