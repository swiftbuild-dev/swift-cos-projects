# pyrefly: ignore [missing-import]
import customtkinter as ctk
from typing import Callable, List
from question import Question, SingleAnswerQuestion, MultiAnswerQuestion, Quiz

ACCENT_COLOR = "#3B82F6"
CORRECT_COLOR = "#10B981"  # Soft green
INCORRECT_COLOR = "#EF4444" # Soft red
BG_COLOR = "#FFFFFF"
CARD_BG = "#FFFFFF"
TEXT_COLOR = "#111827"

class QuizUI(ctk.CTk):
    def __init__(self, quiz: Quiz):
        super().__init__()
        self.quiz = quiz
        
        # Window setup
        self.title("OOP Quiz App")
        self.geometry("420x550")
        self.configure(fg_color=BG_COLOR)
        
        # Main card frame (centered)
        self.card = ctk.CTkFrame(self, width=380, height=500, fg_color=CARD_BG, corner_radius=15, 
                                 border_width=1, border_color="#E5E7EB")
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        # UI Elements
        self.score_label = ctk.CTkLabel(self.card, text=self.quiz.get_score(), text_color="#6B7280", font=("Arial", 14))
        self.score_label.pack(pady=(20, 10), padx=20, anchor="e")
        
        self.question_label = ctk.CTkLabel(self.card, text="", text_color=TEXT_COLOR, font=("Arial", 18, "bold"), 
                                           wraplength=340, justify="left")
        self.question_label.pack(pady=(10, 20), padx=20, fill="x")
        
        self.options_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.options_frame.pack(fill="both", expand=True, padx=20)
        
        self.submit_btn = ctk.CTkButton(self.card, text="Submit", command=self.on_submit, 
                                        fg_color=ACCENT_COLOR, hover_color="#2563EB", 
                                        font=("Arial", 16, "bold"), height=45, corner_radius=8)
        self.submit_btn.pack(pady=(10, 20), padx=20, fill="x")
        
        # State
        self.selected_options = []
        self.option_widgets = []
        
        self.load_question()
        
    def clear_options(self):
        for widget in self.option_widgets:
            widget[0].destroy()
        self.option_widgets.clear()
        self.selected_options.clear()
        
    def load_question(self):
        self.clear_options()
        self.submit_btn.configure(text="Submit", command=self.on_submit, state="normal")
        self.score_label.configure(text=self.quiz.get_score())
        
        question = self.quiz.get_current_question()
        if not question:
            self.show_results()
            return
            
        self.question_label.configure(text=question.text)
        
        if isinstance(question, SingleAnswerQuestion):
            for opt in question.options:
                btn = ctk.CTkButton(self.options_frame, text=opt, fg_color="transparent", 
                                    text_color=TEXT_COLOR, border_width=2, border_color="#E5E7EB", 
                                    hover_color="#F3F4F6", anchor="w", height=40, corner_radius=8,
                                    command=lambda o=opt: self.select_single(o))
                btn.pack(pady=5, fill="x")
                self.option_widgets.append((btn, opt))
        
        elif isinstance(question, MultiAnswerQuestion):
            for opt in question.options:
                chk = ctk.CTkCheckBox(self.options_frame, text=opt, text_color=TEXT_COLOR, 
                                      fg_color=ACCENT_COLOR, hover_color="#2563EB", border_color="#E5E7EB",
                                      corner_radius=4, command=lambda o=opt: self.toggle_multi(o))
                chk.pack(pady=8, fill="x", padx=5)
                self.option_widgets.append((chk, opt))
                
    def select_single(self, option: str):
        self.selected_options = [option]
        for btn, opt in self.option_widgets:
            if opt == option:
                btn.configure(border_color=ACCENT_COLOR)
            else:
                btn.configure(border_color="#E5E7EB")
                
    def toggle_multi(self, option: str):
        if option in self.selected_options:
            self.selected_options.remove(option)
        else:
            self.selected_options.append(option)
            
    def on_submit(self):
        if not self.selected_options:
            return # Don't submit if nothing selected
            
        question = self.quiz.get_current_question()
        is_correct = self.quiz.submit_answer(self.selected_options)
        
        # Highlight feedback
        if isinstance(question, SingleAnswerQuestion):
            for btn, opt in self.option_widgets:
                btn.configure(state="disabled")
                if opt in question.correct_answers:
                    btn.configure(border_color=CORRECT_COLOR, text_color=CORRECT_COLOR)
                elif opt in self.selected_options and not is_correct:
                    btn.configure(border_color=INCORRECT_COLOR, text_color=INCORRECT_COLOR)
                    
        elif isinstance(question, MultiAnswerQuestion):
            for chk, opt in self.option_widgets:
                chk.configure(state="disabled")
                if opt in question.correct_answers:
                    chk.configure(text_color=CORRECT_COLOR)
                elif opt in self.selected_options and opt not in question.correct_answers:
                    chk.configure(text_color=INCORRECT_COLOR)
                    
        self.score_label.configure(text=self.quiz.get_score())
        self.submit_btn.configure(text="Next", command=self.on_next)
        
    def on_next(self):
        self.quiz.next_question()
        self.load_question()
        
    def show_results(self):
        self.clear_options()
        self.question_label.configure(text="Quiz Completed!")
        
        percentage = (self.quiz.get_raw_score() / self.quiz.get_total_questions()) * 100
        
        result_text = f"Final Score: {self.quiz.get_raw_score()} / {self.quiz.get_total_questions()}\nPercentage: {percentage:.1f}%"
        result_label = ctk.CTkLabel(self.options_frame, text=result_text, text_color=TEXT_COLOR, 
                                    font=("Arial", 20, "bold"), justify="center")
        result_label.pack(pady=40)
        
        self.submit_btn.configure(text="Restart Quiz", command=self.restart_quiz)
        
    def restart_quiz(self):
        self.quiz.restart()
        self.load_question()
