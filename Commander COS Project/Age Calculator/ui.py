# pyrefly: ignore [missing-import]
import customtkinter as ctk
from datetime import date
from main import Person, Minor, Adult

class AgeCalculatorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self._setup_window()
        self._create_content_frame()
        self._create_inputs()
        self._create_results_display()

    def _setup_window(self) -> None:
        self.title("Age Calculator")
        self.geometry("400x480")
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")

    def _create_content_frame(self) -> None:
        self.content = ctk.CTkFrame(
            self, width=340, height=440, fg_color="#FFFFFF",
            border_width=1, border_color="#E0E0E0"
        )
        self.content.place(relx=0.5, rely=0.5, anchor="center")
        self.content.grid_propagate(False)
        self.content.pack_propagate(False)
        
        title_lbl = ctk.CTkLabel(
            self.content, text="Age Calculator", 
            font=("Arial", 24, "bold"), text_color="#333333"
        )
        title_lbl.pack(pady=(24, 16))

    def _create_inputs(self) -> None:
        frame = ctk.CTkFrame(self.content, fg_color="transparent")
        frame.pack(pady=12)
        
        self.day_input = self._entry(frame, "DD", 60, 0)
        self.month_input = self._entry(frame, "MM", 60, 1)
        self.year_input = self._entry(frame, "YYYY", 80, 2)
        
        btn = ctk.CTkButton(
            self.content, text="Calculate Age", command=self.calculate,
            fg_color="#0066FF", text_color="#FFFFFF", font=("Arial", 14, "bold")
        )
        btn.pack(pady=24)

    def _entry(self, parent: ctk.CTkFrame, ph: str, w: int, col: int) -> ctk.CTkEntry:
        entry = ctk.CTkEntry(
            parent, placeholder_text=ph, width=w, fg_color="#FFFFFF", 
            border_color="#E0E0E0", border_width=1, text_color="#333333"
        )
        entry.grid(row=0, column=col, padx=8)
        return entry

    def _create_results_display(self) -> None:
        self.err_lbl = ctk.CTkLabel(self.content, text="", text_color="red")
        self.err_lbl.pack(pady=4)
        
        self.age_lbl = ctk.CTkLabel(
            self.content, text="", font=("Arial", 48, "bold"), text_color="#111111"
        )
        self.age_lbl.pack(pady=4)
        
        self.status_lbl = ctk.CTkLabel(self.content, text="", text_color="#666666")
        self.status_lbl.pack(pady=4)
        
        self.bday_lbl = ctk.CTkLabel(self.content, text="", text_color="#666666")
        self.bday_lbl.pack(pady=4)
        
    def calculate(self) -> None:
        self._clear_results()
        try:
            b_date: date = date(
                int(self.year_input.get()), 
                int(self.month_input.get()), 
                int(self.day_input.get())
            )
        except ValueError:
            self.err_lbl.configure(text="Invalid date. Check your numbers.")
            return
            
        if b_date > date.today():
            self.err_lbl.configure(text="Birth date cannot be in the future.")
            return
            
        self._process_valid_date(b_date)

    def _process_valid_date(self, birth_date: date) -> None:
        today: date = date.today()
        age: int = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        # Object Creation via if/else
        person: Person = Minor(birth_date) if age < 18 else Adult(birth_date)
        self._display_results(person)

    def _display_results(self, person: Person) -> None:
        # Polymorphism is demonstrated here: we just call .status_message()
        # on the object, without needing to check if it's a Minor or an Adult.
        self.age_lbl.configure(text=f"{person.calculate_age()}")
        self.status_lbl.configure(text=person.status_message())
        self.bday_lbl.configure(text=f"{person.days_until_next_birthday()} days to birthday")

    def _clear_results(self) -> None:
        self.err_lbl.configure(text="")
        self.age_lbl.configure(text="")
        self.status_lbl.configure(text="")
        self.bday_lbl.configure(text="")
