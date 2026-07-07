# pyrefly: ignore [missing-import]
import customtkinter as ctk
from converter import CurrencyConverter

class ConverterUI(ctk.CTk):
    def __init__(self, converter: CurrencyConverter) -> None:
        super().__init__()
        
        # Polymorphism: This UI variable doesn't care if the converter is Standard or Rounded.
        # It treats any subclass exactly the same way, simply expecting a valid '.convert()' method.
        self.converter: CurrencyConverter = converter
        
        self.title("Currency Converter")
        self.geometry("400x450")
        self.configure(fg_color="#FFFFFF")
        
        self.font_main = ("Arial", 14)
        self.font_title = ("Arial", 20, "bold")
        self.font_result = ("Arial", 22, "bold")
        self.currencies = ["USD", "EUR", "GBP", "NGN", "JPY", "CAD"]
        
        self._build_layout()
        
    def _build_layout(self) -> None:
        # Fixed-width card centered in the window
        self.card = ctk.CTkFrame(self, width=340, height=400, fg_color="#FFFFFF", corner_radius=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        ctk.CTkLabel(self.card, text="Currency Converter", font=self.font_title, text_color="#1A1A1A").pack(pady=(20, 16))
        
        self.amount_entry = ctk.CTkEntry(
            self.card, placeholder_text="Amount", font=self.font_main, 
            fg_color="#FFFFFF", border_color="#E0E0E0", border_width=1, text_color="#1A1A1A"
        )
        self.amount_entry.pack(fill="x", padx=16, pady=(0, 12))
        
        self.from_var = ctk.StringVar(value="USD")
        self._create_dropdown(self.from_var).pack(fill="x", padx=16, pady=(0, 8))
        
        self.swap_btn = ctk.CTkButton(
            self.card, text="⇄ Swap", font=self.font_main, command=self.swap_currencies,
            fg_color="#FFFFFF", text_color="#0056b3", border_color="#0056b3", border_width=1, hover_color="#F0F8FF", width=80
        )
        self.swap_btn.pack(pady=(4, 8))
        
        self.to_var = ctk.StringVar(value="EUR")
        self._create_dropdown(self.to_var).pack(fill="x", padx=16, pady=(0, 16))
        
        self.convert_btn = ctk.CTkButton(
            self.card, text="Convert", font=self.font_main, command=self.perform_conversion,
            fg_color="#0056b3", text_color="#FFFFFF", hover_color="#004494"
        )
        self.convert_btn.pack(fill="x", padx=16, pady=(0, 16))
        
        self.result_label = ctk.CTkLabel(self.card, text="", font=self.font_result, text_color="#1A1A1A")
        self.result_label.pack(pady=(16, 0))

    def _create_dropdown(self, variable: ctk.StringVar) -> ctk.CTkOptionMenu:
        return ctk.CTkOptionMenu(
            self.card, values=self.currencies, variable=variable, font=self.font_main,
            fg_color="#FFFFFF", button_color="#F5F5F5", button_hover_color="#EBEBEB", 
            text_color="#1A1A1A", dropdown_font=self.font_main
        )
        
    def swap_currencies(self) -> None:
        current_from, current_to = self.from_var.get(), self.to_var.get()
        self.from_var.set(current_to)
        self.to_var.set(current_from)
        
    def perform_conversion(self) -> None:
        try:
            amount = float(self.amount_entry.get())
            from_curr, to_curr = self.from_var.get(), self.to_var.get()
            
            # Polymorphism: calling .convert() works beautifully whether 
            # it's a StandardConverter or RoundedConverter.
            result = self.converter.convert(amount, from_curr, to_curr)
            
            # Format nicely (e.g., "100 USD = 92.3 EUR")
            self.result_label.configure(text=f"{amount:g} {from_curr} = {result} {to_curr}")
        except ValueError:
            self.result_label.configure(text="Please enter a valid number")
