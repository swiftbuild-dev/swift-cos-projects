from quiz_manager import QuizManager
from ui import QuizApp

def main():
    manager = QuizManager()
    manager.load_questions("questions.json")
    
    app = QuizApp(manager)
    app.mainloop()

if __name__ == "__main__":
    main()
