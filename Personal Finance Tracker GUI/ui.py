# pyrefly: ignore [missing-import]
import customtkinter as ctk
import tkinter.messagebox as messagebox
from transaction import Income, Expense
from finance_manager import FinanceManager

class FinanceTrackerUI:
    def __init__(self, root: ctk.CTk, manager: FinanceManager):
        self.root = root
        self.manager = manager
        
        self._setup_window()
        self._setup_styles()
        self._build_layout()
        self._refresh_ui()

    def _setup_window(self):
        self.root.title("Personal Finance Tracker")
        self.root.geometry("420x600")
        self.root.configure(fg_color="#FFFFFF")

    def _setup_styles(self):
        self.card_bg = "#FFFFFF"
        self.border_col = "#E0E0E0"
        self.accent_col = "#3B82F6" # Clean blue accent
        self.text_col = "#1F2937"   # Dark gray
        self.inc_col = "#10B981"    # Soft green
        self.exp_col = "#EF4444"    # Soft red
        self.font_hd = ("Inter", 36, "bold")
        self.font_bd = ("Inter", 14)

    def _build_layout(self):
        # We use a fixed-width card in the center to prevent stretching when maximized
        self.card = ctk.CTkFrame(
            self.root, width=380, height=560, fg_color=self.card_bg,
            border_width=1, border_color=self.border_col, corner_radius=12
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False) # Prevents the card from shrinking to its children
        
        self.bal_label = ctk.CTkLabel(self.card, text="$0.00", font=self.font_hd, text_color=self.text_col)
        self.bal_label.pack(pady=(24, 16))
        
        self.desc_ent = ctk.CTkEntry(
            self.card, placeholder_text="Description", font=self.font_bd, 
            fg_color="#F9FAFB", border_color=self.border_col, text_color=self.text_col
        )
        self.desc_ent.pack(fill="x", padx=16, pady=(0, 8))
        
        self.amt_ent = ctk.CTkEntry(
            self.card, placeholder_text="Amount", font=self.font_bd, 
            fg_color="#F9FAFB", border_color=self.border_col, text_color=self.text_col
        )
        self.amt_ent.pack(fill="x", padx=16, pady=(0, 8))
        
        self.type_var = ctk.StringVar(value="Expense")
        tgl_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        tgl_frame.pack(fill="x", padx=16, pady=(0, 16))
        
        ctk.CTkRadioButton(
            tgl_frame, text="Income", variable=self.type_var, value="Income",
            font=self.font_bd, text_color=self.text_col, fg_color=self.accent_col
        ).pack(side="left", expand=True)
        
        ctk.CTkRadioButton(
            tgl_frame, text="Expense", variable=self.type_var, value="Expense",
            font=self.font_bd, text_color=self.text_col, fg_color=self.accent_col
        ).pack(side="left", expand=True)
        
        self.add_btn = ctk.CTkButton(
            self.card, text="Add Transaction", font=self.font_bd,
            fg_color=self.accent_col, text_color="#FFFFFF", hover_color="#2563EB", command=self._add_txn
        )
        self.add_btn.pack(fill="x", padx=16, pady=(0, 24))
        
        self.list_frame = ctk.CTkScrollableFrame(self.card, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    def _add_txn(self):
        desc = self.desc_ent.get().strip()
        amt_str = self.amt_ent.get().strip()
        if not desc or not amt_str: return
        
        try:
            amt = float(amt_str)
        except ValueError: return
            
        t = Income(desc, amt) if self.type_var.get() == "Income" else Expense(desc, amt)
        self.manager.add_transaction(t)
        
        self.desc_ent.delete(0, 'end')
        self.amt_ent.delete(0, 'end')
        self._refresh_ui()

    def _del_txn(self, t_id: str):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?"):
            self.manager.remove_transaction(t_id)
            self._refresh_ui()

    def _refresh_ui(self):
        self.bal_label.configure(text=f"${self.manager.get_balance():,.2f}")
        for w in self.list_frame.winfo_children(): w.destroy()
            
        for t in reversed(self.manager.get_transactions()):
            row = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            row.pack(fill="x", pady=4)
            
            ctk.CTkLabel(row, text=t.description, font=self.font_bd, text_color=self.text_col).pack(side="left")
            
            btn = ctk.CTkButton(
                row, text="Delete", width=60, font=self.font_bd, fg_color="#FFFFFF",
                text_color=self.accent_col, border_width=1, border_color=self.accent_col,
                command=lambda tid=t.id: self._del_txn(tid)
            )
            btn.pack(side="right", padx=(8, 0))
            
            col = self.inc_col if isinstance(t, Income) else self.exp_col
            sign = "+" if isinstance(t, Income) else "-"
            ctk.CTkLabel(row, text=f"{sign}${t.amount:,.2f}", font=self.font_bd, text_color=col).pack(side="right")
            
            # Simple list divider
            ctk.CTkFrame(self.list_frame, height=1, fg_color=self.border_col).pack(fill="x", pady=2)
