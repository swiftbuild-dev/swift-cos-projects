# Quiz App GUI

## 🚀 Core Functionality
A clean, interactive Quiz application where users can answer multiple-choice questions. It supports single-answer and multi-answer question types, grades the quiz automatically, and shows a final score.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)
This project uses all four core principles of OOP. Here's how it works using simple terms!

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like using a TV remote. You press a button to change the channel, but you don't need to know how the circuits inside work. In our code, we create a basic blueprint that says *what* should happen, but leaves the *how* for later.

**Code Example:**
```python
# We define a template (Question) that guarantees any subclass will have an is_correct() method.
class Question(ABC):
    @abstractmethod
    def is_correct(self, selected_answer: str) -> bool:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child inheriting eye color from a parent. A new class (child) can reuse the code from an existing class (parent) so we don't have to write the same code twice.

**Code Example:**
```python
# We reuse the text and options setup from the Question base class,
# adding only what's unique to a single-answer question.
class SingleAnswerQuestion(Question):
    def __init__(self, text: str, options: list[str], correct_answer: str):
        super().__init__(text, options)
        self.correct_answer = correct_answer
```

### 3. 🔄 Polymorphism — *Many forms*
Polymorphism means "many forms". It's like how you can tell a dog to "speak" and it barks, but if you tell a cat to "speak", it meows. They both understand the same command but do it differently.

**Code Example:**
```python
# The Quiz doesn't need to know which type of question it's grading.
# It just calls is_correct() and the specific question object handles its own logic.
is_right = q.is_correct(selected_answer)
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation is like a safe. The valuables (data) are locked inside, and you can only access them if you have the key (specific methods). This prevents outside code from accidentally messing up the internal data.

**Code Example:**
```python
class Quiz:
    def __init__(self, questions: list[Question]):
        # We use private variables (_score) so external code can't cheat!
        self._score = 0
```
