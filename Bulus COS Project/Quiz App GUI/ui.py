# pyrefly: ignore [missing-import]
import customtkinter as ctk
from main import Quiz, get_quiz_questions, SingleAnswerQuestion, MultiAnswerQuestion

class QuizApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OOP Quiz")
        self.geometry("420x550")
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")
        
        self.ACCENT, self.TEXT = "#3B82F6", "#1F2937"
        self.FONT_L, self.FONT_S = ("Arial", 18, "bold"), ("Arial", 14)
        
        self.quiz = Quiz(get_quiz_questions())
        self.setup_ui()

    def setup_ui(self):
        self.card = ctk.CTkFrame(
            self, width=360, height=500, fg_color="#FFFFFF",
            border_width=1, border_color="#E5E7EB", corner_radius=12
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        self.build_quiz_screen()

    def build_quiz_screen(self):
        self.clear_card()
        self.progress_label = ctk.CTkLabel(self.card, text="", font=self.FONT_S, text_color="#6B7280")
        self.progress_label.pack(pady=(20, 10))
        
        self.question_label = ctk.CTkLabel(self.card, text="", font=self.FONT_L, text_color=self.TEXT, wraplength=300)
        self.question_label.pack(pady=(0, 20))
        
        self.options_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=20, pady=10)
        
        self.submit_btn = ctk.CTkButton(self.card, text="Submit", font=self.FONT_S, fg_color=self.ACCENT, text_color="#FFFFFF")
        self.submit_btn.pack(pady=(20, 10))
        
        self.score_label = ctk.CTkLabel(self.card, text="", font=self.FONT_S, text_color="#6B7280")
        self.score_label.pack(pady=5)
        self.load_question()

    def clear_card(self):
        for w in self.card.winfo_children(): w.destroy()

    def load_question(self):
        q = self.quiz.get_current_question()
        if not q: return self.show_results()
            
        self.progress_label.configure(text=f"Question {self.quiz._current_index + 1} of {self.quiz.get_total()}")
        self.question_label.configure(text=q.text)
        self.score_label.configure(text=f"Score: {self.quiz.get_score()}/{self.quiz.get_total()}")
        self.submit_btn.configure(text="Submit", command=self.on_submit, state="normal")
        self.render_options(q)

    def render_options(self, q):
        for w in self.options_frame.winfo_children(): w.destroy()
        self.option_widgets = []
        self.radio_var = ctk.StringVar(value="")
        
        for option in q.options:
            row = ctk.CTkFrame(self.options_frame, fg_color="#FFFFFF", border_width=1, border_color="#E5E7EB")
            row.pack(fill="x", pady=6)
            
            if isinstance(q, SingleAnswerQuestion):
                w = ctk.CTkRadioButton(row, text=option, font=self.FONT_S, text_color=self.TEXT, fg_color=self.ACCENT, variable=self.radio_var, value=option)
            else:
                w = ctk.CTkCheckBox(row, text=option, font=self.FONT_S, text_color=self.TEXT, fg_color=self.ACCENT)
                
            w.pack(anchor="w", padx=12, pady=10)
            self.option_widgets.append((option, w, row))

    def get_selected(self, q) -> list[str]:
        if isinstance(q, SingleAnswerQuestion):
            ans = self.radio_var.get()
            return [ans] if ans else []
        return [opt for opt, w, _ in self.option_widgets if w.get() == 1]

    def on_submit(self):
        q = self.quiz.get_current_question()
        selected = self.get_selected(q)
        if not selected: return
        
        ans_str = ",".join(sorted(selected)) if isinstance(q, MultiAnswerQuestion) else selected[0]
        self.quiz.submit_answer(ans_str)
        
        correct = q.correct_answers if isinstance(q, MultiAnswerQuestion) else [q.correct_answer]
        self.highlight_answers(correct, selected)
        
        self.score_label.configure(text=f"Score: {self.quiz.get_score()}/{self.quiz.get_total()}")
        self.submit_btn.configure(text="Next", command=self.on_next)

    def highlight_answers(self, correct, selected):
        for opt, w, row in self.option_widgets:
            w.configure(state="disabled")
            if opt in correct:
                row.configure(fg_color="#D1FAE5", border_color="#10B981")
                w.configure(bg_color="#D1FAE5", text_color="#065F46")
            elif opt in selected:
                row.configure(fg_color="#FEE2E2", border_color="#EF4444")
                w.configure(bg_color="#FEE2E2", text_color="#991B1B")

    def on_next(self):
        self.quiz.next_question()
        self.load_question()

    def show_results(self):
        self.clear_card()
        score, total = self.quiz.get_score(), self.quiz.get_total()
        
        ctk.CTkLabel(self.card, text="Quiz Complete!", font=self.FONT_L, text_color=self.TEXT).pack(pady=(120, 10))
        ctk.CTkLabel(self.card, text=f"Score: {score}/{total} ({int(score/total*100)}%)", font=self.FONT_S, text_color="#6B7280").pack(pady=10)
        
        btn = ctk.CTkButton(self.card, text="Restart Quiz", font=self.FONT_S, fg_color=self.ACCENT, text_color="#FFFFFF", command=self.restart_quiz)
        btn.pack(pady=30)

    def restart_quiz(self):
        self.quiz = Quiz(get_quiz_questions())
        self.build_quiz_screen()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
