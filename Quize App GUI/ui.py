# pyrefly: ignore [missing-import]
import customtkinter as ctk
from quiz_manager import QuizManager

# UI Constants for consistent styling
ACCENT = "#4F46E5"         # Indigo Primary
ACCENT_HOVER = "#4338CA"
BG_WHITE = "#FFFFFF"
TEXT_DARK = "#1F2937"
BORDER = "#E5E7EB"
CORRECT_COLOR = "#10B981"  # Green
WRONG_COLOR = "#EF4444"    # Red
FONT_H = ("Helvetica", 24, "bold")
FONT_B = ("Helvetica", 16)

class QuizApp(ctk.CTk):
    def __init__(self, manager: QuizManager):
        super().__init__()
        self.manager = manager
        
        self.title("Modern OOP Quiz")
        self.geometry("600x500")
        self.configure(fg_color=BG_WHITE)
        ctk.set_appearance_mode("Light")
        
        self.build_ui()
        self.load_current_question()

    def build_ui(self):
        self.progress_lbl = ctk.CTkLabel(self, text="", font=FONT_B, text_color=TEXT_DARK)
        self.progress_lbl.pack(pady=(20, 10))
        
        self.card = ctk.CTkFrame(self, fg_color=BG_WHITE, border_width=1, border_color=BORDER, corner_radius=16)
        self.card.pack(fill="both", expand=True, padx=40, pady=10)
        
        self.question_lbl = ctk.CTkLabel(self.card, text="", font=FONT_H, text_color=TEXT_DARK, wraplength=400)
        self.question_lbl.pack(pady=(40, 30), padx=20)
        
        self.buttons_frame = ctk.CTkFrame(self.card, fg_color=BG_WHITE)
        self.buttons_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.next_btn = ctk.CTkButton(self, text="Next Question", command=self.on_next, font=FONT_B, 
                                      fg_color=TEXT_DARK, hover_color="#000000", height=45, corner_radius=8)

    def clear_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.next_btn.pack_forget()

    def create_option_btn(self, text: str, command) -> ctk.CTkButton:
        # A clean, minimalistic button that starts out looking like an outline
        return ctk.CTkButton(self.buttons_frame, text=text, command=command, font=FONT_B,
                             fg_color=BG_WHITE, text_color=TEXT_DARK, border_width=1, 
                             border_color=BORDER, hover_color="#F3F4F6", height=45, corner_radius=8)

    def load_current_question(self):
        self.clear_buttons()
        self.progress_lbl.configure(text=self.manager.get_progress_text())
        
        q_data = self.manager.get_current_question().render_prompt()
        self.question_lbl.configure(text=q_data["prompt"])
        
        for i, opt in enumerate(q_data["options"]):
            btn = self.create_option_btn(opt, None)
            btn.configure(command=lambda idx=i, b=btn: self.on_answer(idx, b))
            btn.pack(pady=8, fill="x")

    def on_answer(self, selected_index: int, selected_btn: ctk.CTkButton):
        is_correct = self.manager.submit_answer(selected_index)
        
        # Change the color of the picked answer to indicate selection & correctness
        if is_correct:
            selected_btn.configure(fg_color=CORRECT_COLOR, text_color=BG_WHITE, border_color=CORRECT_COLOR, hover_color=CORRECT_COLOR)
        else:
            selected_btn.configure(fg_color=WRONG_COLOR, text_color=BG_WHITE, border_color=WRONG_COLOR, hover_color=WRONG_COLOR)
            
        for child in self.buttons_frame.winfo_children():
            child.configure(state="disabled")
            
        self.next_btn.pack(pady=20)

    def on_next(self):
        if self.manager.next_question():
            self.load_current_question()
        else:
            self.show_results()

    def show_results(self):
        self.clear_buttons()
        self.progress_lbl.configure(text="Quiz Complete!")
        score, total = self.manager.get_score()
        
        self.question_lbl.configure(text=f"Your Score: {score}/{total}\n({int((score/total)*100)}%)")
        
        btn = ctk.CTkButton(self.buttons_frame, text="Restart Quiz", command=self.restart, font=FONT_B,
                            fg_color=ACCENT, text_color=BG_WHITE, hover_color=ACCENT_HOVER, height=45, corner_radius=8)
        btn.pack(pady=8, fill="x")

    def restart(self):
        self.manager.restart()
        self.load_current_question()
