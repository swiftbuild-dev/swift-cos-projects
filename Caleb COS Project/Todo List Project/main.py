# pyrefly: ignore [missing-import]
import customtkinter as ctk
from tasks import SimpleTask, RecurringTask, TaskManager

# Use light mode with white background
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Todo List")
        self.geometry("620x680")
        self.configure(fg_color="white")
        self.resizable(False, False)
        self.mgr = TaskManager()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        # --- Title ---
        ctk.CTkLabel(self, text="My Todo List", font=("Helvetica", 26, "bold"),
                     text_color="#1a1a1a").pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Stay organised, one task at a time.",
                     font=("Helvetica", 13), text_color="#888888").pack(pady=(0, 20))

        # --- Input Row ---
        row = ctk.CTkFrame(self, fg_color="#f5f5f5", corner_radius=12)
        row.pack(fill="x", padx=30, pady=(0, 10))

        # Task title entry
        self.ent = ctk.CTkEntry(row, placeholder_text="Add a new task...",
                                border_width=0, fg_color="transparent",
                                font=("Helvetica", 13), text_color="#1a1a1a",
                                placeholder_text_color="#aaaaaa", height=42)
        self.ent.pack(side="left", padx=(12, 0), expand=True, fill="x")

        # Priority dropdown
        self.prio = ctk.CTkOptionMenu(row, values=["Low", "Medium", "High"],
                                      width=90, height=34, font=("Helvetica", 12),
                                      fg_color="#e0e0e0", text_color="#333333",
                                      button_color="#cccccc", button_hover_color="#bbbbbb",
                                      dropdown_fg_color="white", dropdown_text_color="#1a1a1a")
        self.prio.set("Medium")
        self.prio.pack(side="left", padx=8)

        # Recurring checkbox
        self.rec = ctk.CTkCheckBox(row, text="Daily", font=("Helvetica", 12),
                                   text_color="#555555", checkbox_width=18, checkbox_height=18,
                                   fg_color="#4a90d9", border_color="#cccccc")
        self.rec.pack(side="left", padx=(0, 8))

        # Add button
        ctk.CTkButton(row, text="+ Add", command=self.add_task, width=70, height=34,
                      font=("Helvetica", 13, "bold"), fg_color="#1a1a1a",
                      hover_color="#333333", corner_radius=8).pack(side="left", padx=(0, 10))

        # --- Stats Label ---
        self.stats_lbl = ctk.CTkLabel(self, text="", font=("Helvetica", 12),
                                      text_color="#aaaaaa")
        self.stats_lbl.pack(pady=(6, 4))

        # --- Divider ---
        ctk.CTkFrame(self, height=1, fg_color="#eeeeee").pack(fill="x", padx=30, pady=(0, 10))

        # --- Task List ---
        self.list_frm = ctk.CTkScrollableFrame(self, fg_color="white",
                                               scrollbar_button_color="#e0e0e0",
                                               scrollbar_button_hover_color="#cccccc")
        self.list_frm.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def add_task(self):
        # Get the text from the entry box
        title = self.ent.get().strip()
        if not title:
            return
        # Create the right type of task based on the Daily checkbox
        task = RecurringTask(title, self.prio.get()) if self.rec.get() else SimpleTask(title, self.prio.get())
        self.mgr.add(task)
        self.ent.delete(0, "end")
        self.rec.deselect()
        self.refresh()

    def refresh(self):
        # Remove all existing task cards from the list
        for w in self.list_frm.winfo_children():
            w.destroy()

        tasks = self.mgr.get_all()

        if not tasks:
            ctk.CTkLabel(self.list_frm, text="No tasks yet. Add one above!",
                         font=("Helvetica", 13), text_color="#cccccc").pack(pady=40)
        else:
            for task in tasks:
                self._make_card(task)

        # Update stats
        total = len(tasks)
        done = sum(1 for t in tasks if t.is_comp)
        self.stats_lbl.configure(text=f"{done} of {total} completed")

    def _make_card(self, task):
        # Colour based on priority
        prio_color = {"High": "#ff4d4d", "Medium": "#f5a623", "Low": "#4cd964"}.get(task.prio, "#cccccc")

        # Card frame
        card = ctk.CTkFrame(self.list_frm, fg_color="#fafafa", corner_radius=10,
                            border_width=1, border_color="#eeeeee")
        card.pack(fill="x", pady=5)

        # Priority dot
        ctk.CTkLabel(card, text="●", font=("Helvetica", 10),
                     text_color=prio_color, width=16).pack(side="left", padx=(14, 4))

        # Task display text
        txt_color = "#bbbbbb" if task.is_comp else "#1a1a1a"
        ctk.CTkLabel(card, text=task.display(), font=("Helvetica", 13),
                     text_color=txt_color, anchor="w").pack(side="left", fill="x", expand=True, pady=14)

        # Delete button
        ctk.CTkButton(card, text="✕", width=30, height=28, font=("Helvetica", 12),
                      fg_color="transparent", text_color="#cccccc", hover_color="#f5f5f5",
                      command=lambda i=task.id: [self.mgr.remove(i), self.refresh()]
                      ).pack(side="right", padx=(0, 6))

        # Toggle done button
        btn_text = "Undo" if task.is_comp else "Done"
        ctk.CTkButton(card, text=btn_text, width=56, height=28, font=("Helvetica", 12),
                      fg_color="#e8f5e9" if task.is_comp else "#e3f2fd",
                      text_color="#388e3c" if task.is_comp else "#1565c0",
                      hover_color="#dcedc8" if task.is_comp else "#bbdefb",
                      border_width=0, corner_radius=6,
                      command=lambda i=task.id: [self.mgr.toggle(i), self.refresh()]
                      ).pack(side="right", padx=(0, 6))

if __name__ == "__main__":
    App().mainloop()
