# pyrefly: ignore [missing-import]
import customtkinter as ctk
from tkinter import messagebox
from finance_manager import FinanceManager
from transaction import Income, Expense, Transaction

# Constants for a clean, modern, minimalistic UI
ACCENT_COLOR = "#4F46E5" # Indigo
ACCENT_HOVER = "#4338CA"
BG_WHITE = "#FFFFFF"
TEXT_DARK = "#111827"
TEXT_MUTED = "#6B7280"
BORDER_GRAY = "#E5E7EB"

CATEGORIES = ["All", "Food", "Transport", "Salary", "Bills", "Other"]
ADD_CATEGORIES = ["Food", "Transport", "Salary", "Bills", "Other"]

class FinanceTrackerUI(ctk.CTk):
    def __init__(self, manager: FinanceManager):
        super().__init__(fg_color=BG_WHITE)
        self.manager = manager
        self.current_filter = "All"
        self._setup_window()
        self._build_ui()
        self.refresh_ui()

    def _setup_window(self) -> None:
        self.title("Personal Finance Tracker")
        self.geometry("600x800")
        ctk.set_appearance_mode("Light")
        
    def _build_ui(self) -> None:
        self._build_header()
        self._build_totals()
        self._build_add_transaction_form()
        self._build_filters()
        self._build_transaction_list()
        
    def _build_header(self) -> None:
        self.lbl_balance = ctk.CTkLabel(
            self, text="₦0.00", font=("Inter", 36, "bold"), text_color=TEXT_DARK
        )
        self.lbl_balance.pack(pady=(30, 5))
        
        ctk.CTkLabel(
            self, text="Current Balance", font=("Inter", 14), text_color=TEXT_MUTED
        ).pack(pady=(0, 20))
        
    def _build_totals(self) -> None:
        totals_frame = ctk.CTkFrame(self, fg_color=BG_WHITE)
        totals_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.lbl_income_total = ctk.CTkLabel(
            totals_frame, text="Total Income: ₦0.00", font=("Inter", 14), text_color="#10B981"
        )
        self.lbl_income_total.pack(side="left", expand=True)
        
        self.lbl_expense_total = ctk.CTkLabel(
            totals_frame, text="Total Expenses: ₦0.00", font=("Inter", 14), text_color="#EF4444"
        )
        self.lbl_expense_total.pack(side="right", expand=True)

    def _build_add_transaction_form(self) -> None:
        form = ctk.CTkFrame(self, fg_color=BG_WHITE, border_color=BORDER_GRAY, border_width=1, corner_radius=8)
        form.pack(fill="x", padx=20, pady=10)
        
        row1 = ctk.CTkFrame(form, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=(15, 5))
        self.entry_amount = ctk.CTkEntry(row1, placeholder_text="Amount", font=("Inter", 14))
        self.entry_amount.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.type_var = ctk.StringVar(value="Expense")
        self.combo_type = ctk.CTkComboBox(row1, values=["Expense", "Income"], variable=self.type_var, font=("Inter", 14))
        self.combo_type.pack(side="right")
        
        row2 = ctk.CTkFrame(form, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=5)
        self.combo_category = ctk.CTkComboBox(row2, values=ADD_CATEGORIES, font=("Inter", 14))
        self.combo_category.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_note = ctk.CTkEntry(row2, placeholder_text="Note (optional)", font=("Inter", 14))
        self.entry_note.pack(side="right", fill="x", expand=True)
        
        btn = ctk.CTkButton(form, text="Add Transaction", font=("Inter", 14, "bold"), fg_color=ACCENT_COLOR, hover_color=ACCENT_HOVER, text_color=BG_WHITE, command=self.handle_add_transaction)
        btn.pack(fill="x", padx=15, pady=(10, 15))

    def _build_filters(self) -> None:
        self.filter_frame = ctk.CTkScrollableFrame(self, fg_color=BG_WHITE, orientation="horizontal", height=40)
        self.filter_frame.pack(fill="x", padx=20, pady=10)
        
        self.filter_buttons = {}
        for cat in CATEGORIES:
            btn = ctk.CTkButton(
                self.filter_frame, text=cat, font=("Inter", 12), width=70,
                command=lambda c=cat: self.set_filter(c)
            )
            btn.pack(side="left", padx=5)
            self.filter_buttons[cat] = btn

    def _build_transaction_list(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_WHITE, border_color=BORDER_GRAY, border_width=1, corner_radius=8
        )
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    def set_filter(self, category: str) -> None:
        self.current_filter = category
        self.refresh_ui()

    def handle_add_transaction(self) -> None:
        try:
            amount = float(self.entry_amount.get())
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount.")
            return

        cat = self.combo_category.get()
        note = self.entry_note.get()
        
        # Abstraction & Inheritance at work: we instantiate a specific subclass
        t = Income(amount, cat, note) if self.type_var.get() == "Income" else Expense(amount, cat, note)
        
        # Encapsulation: We ask the manager to add it; we don't manipulate its list directly
        self.manager.add_transaction(t)
        
        self.entry_amount.delete(0, 'end')
        self.entry_note.delete(0, 'end')
        self.refresh_ui()

    def handle_delete(self, transaction_id: str) -> None:
        if messagebox.askyesno("Confirm", "Delete this transaction?"):
            self.manager.remove_transaction(transaction_id)
            self.refresh_ui()

    def refresh_ui(self) -> None:
        self.lbl_balance.configure(text=f"₦{self.manager.get_balance():,.2f}")
        inc_tot, exp_tot = self.manager.get_totals()
        self.lbl_income_total.configure(text=f"Total Income: ₦{inc_tot:,.2f}")
        self.lbl_expense_total.configure(text=f"Total Expenses: ₦{exp_tot:,.2f}")
        
        for cat, btn in self.filter_buttons.items():
            if cat == self.current_filter:
                btn.configure(fg_color=ACCENT_COLOR, text_color=BG_WHITE, hover_color=ACCENT_HOVER)
            else:
                btn.configure(fg_color=BG_WHITE, text_color=ACCENT_COLOR, border_color=ACCENT_COLOR, border_width=1, hover_color="#EEEDF9")

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for t in reversed(self.manager.get_transactions_by_category(self.current_filter)):
            self._create_transaction_row(t)

    def _create_transaction_row(self, t: Transaction) -> None:
        row = ctk.CTkFrame(self.list_frame, fg_color=BG_WHITE, border_color=BORDER_GRAY, border_width=1, corner_radius=6)
        row.pack(fill="x", padx=10, pady=5)
        
        info = ctk.CTkFrame(row, fg_color="transparent")
        info.pack(side="left", padx=15, pady=10)
        ctk.CTkLabel(info, text=t.category, font=("Inter", 14, "bold"), text_color=TEXT_DARK).pack(anchor="w")
        if t.note:
            ctk.CTkLabel(info, text=t.note, font=("Inter", 12), text_color=TEXT_MUTED).pack(anchor="w")
            
        action = ctk.CTkFrame(row, fg_color="transparent")
        action.pack(side="right", padx=15, pady=10)
        
        # Polymorphism: Calling t.display_label() and t.display_color() without checking type
        ctk.CTkLabel(action, text=t.display_label(), font=("Inter", 14, "bold"), text_color=t.display_color()).pack(side="left", padx=(0, 15))
        
        btn_del = ctk.CTkButton(
            action, text="✕", width=30, font=("Inter", 12), fg_color=BG_WHITE, text_color=ACCENT_COLOR, 
            border_color=ACCENT_COLOR, border_width=1, hover_color="#EEEDF9", command=lambda: self.handle_delete(t.id)
        )
        btn_del.pack(side="right")
