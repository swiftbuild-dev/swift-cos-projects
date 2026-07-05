# pyrefly: ignore [missing-import]
import customtkinter as ctk
from calculator import Calculator

ACCENT_COLOR = "#005bb5" # a nice blue
WHITE = "#FFFFFF"
TEXT_DARK = "#2c3e50"
BG_LIGHT_GRAY = "#f1f3f5"
BORDER_GRAY = "#e9ecef"

class CalculatorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Basic Calculator")
        self.geometry("400x600")
        self.configure(fg_color=WHITE)
        
        self.calc = Calculator()
        self.active_operator_btn: ctk.CTkButton | None = None
        
        # Center the calculator card with a fixed size to prevent stretching
        self.card = ctk.CTkFrame(self, width=320, height=480, fg_color=WHITE, 
                                 border_width=1, border_color=BORDER_GRAY)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        self._build_display()
        self._build_buttons()

    def _build_display(self) -> None:
        self.display_var = ctk.StringVar(value="0")
        self.display_label = ctk.CTkLabel(
            self.card, textvariable=self.display_var, font=("Helvetica", 42, "bold"), 
            text_color=TEXT_DARK, anchor="e"
        )
        self.display_label.pack(fill="x", padx=24, pady=(32, 16))

    def _build_buttons(self) -> None:
        btn_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True, padx=16, pady=(0, 24))
        
        for i in range(4): btn_frame.grid_columnconfigure(i, weight=1, uniform="col")
        for i in range(5): btn_frame.grid_rowconfigure(i, weight=1, uniform="row")
            
        layout = [
            ("C", 0, 0, 3), ("÷", 0, 3, 1),
            ("7", 1, 0, 1), ("8", 1, 1, 1), ("9", 1, 2, 1), ("×", 1, 3, 1),
            ("4", 2, 0, 1), ("5", 2, 1, 1), ("6", 2, 2, 1), ("−", 2, 3, 1),
            ("1", 3, 0, 1), ("2", 3, 1, 1), ("3", 3, 2, 1), ("+", 3, 3, 1),
            ("0", 4, 0, 2), (".", 4, 2, 1), ("=", 4, 3, 1)
        ]
        
        self.buttons: dict[str, ctk.CTkButton] = {}
        for txt, r, c, cs in layout:
            btn = self._create_button(btn_frame, txt)
            btn.grid(row=r, column=c, columnspan=cs, sticky="nsew", padx=4, pady=4)
            self.buttons[txt] = btn

    def _create_button(self, parent: ctk.CTkFrame, text: str) -> ctk.CTkButton:
        btn = ctk.CTkButton(parent, text=text, font=("Helvetica", 20),
                            command=lambda t=text: self._on_click(t), corner_radius=8)
        
        if text in "0123456789.":
            btn.configure(fg_color=WHITE, text_color=TEXT_DARK, border_width=1, 
                          border_color=BORDER_GRAY, hover_color=BG_LIGHT_GRAY)
        elif text in "÷×−+":
            btn.configure(fg_color=BG_LIGHT_GRAY, text_color=TEXT_DARK, hover_color=BORDER_GRAY)
        elif text == "=":
            btn.configure(fg_color=ACCENT_COLOR, text_color=WHITE, hover_color="#004a94")
        elif text == "C":
            btn.configure(fg_color=WHITE, text_color=ACCENT_COLOR, border_width=1, 
                          border_color=ACCENT_COLOR, hover_color=BG_LIGHT_GRAY)
        return btn

    def _on_click(self, value: str) -> None:
        if value in "0123456789.":
            self.calc.input_digit(value)
            self._reset_op_colors()
        elif value in "÷×−+":
            self.calc.set_operation(value)
            self._highlight_op(value)
        elif value == "=":
            self.calc.calculate()
            self._reset_op_colors()
        elif value == "C":
            self.calc.clear()
            self._reset_op_colors()
            
        self.display_var.set(self.calc.get_display_value())

    def _highlight_op(self, symbol: str) -> None:
        self._reset_op_colors()
        btn = self.buttons[symbol]
        btn.configure(fg_color=ACCENT_COLOR, text_color=WHITE)
        self.active_operator_btn = btn

    def _reset_op_colors(self) -> None:
        if self.active_operator_btn:
            self.active_operator_btn.configure(fg_color=BG_LIGHT_GRAY, text_color=TEXT_DARK)
            self.active_operator_btn = None
