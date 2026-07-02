# pyrefly: ignore [missing-import]
import customtkinter as ctk
import tkinter.messagebox as messagebox
from task import SimpleTask, RecurringTask
from task_manager import TaskManager

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("OOP Todo List")
        self.geometry("600x600")
        
        # Configure layout to allow dynamic resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.manager = TaskManager()
        
        self._setup_ui()
        self._refresh_task_list()
        
    def _setup_ui(self):
        # Typography: 2 sizes only
        self.heading_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        self.body_font = ctk.CTkFont(family="Helvetica", size=14)
        
        # Top Frame (Input Area)
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.title_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter task title...", font=self.body_font)
        self.title_entry.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")
        
        self.priority_var = ctk.StringVar(value="Medium")
        self.priority_menu = ctk.CTkOptionMenu(input_frame, values=["Low", "Medium", "High"], variable=self.priority_var, font=self.body_font)
        self.priority_menu.grid(row=0, column=1, pady=(0, 10))
        
        self.recurring_var = ctk.BooleanVar(value=False)
        self.recurring_check = ctk.CTkCheckBox(input_frame, text="Repeats daily", variable=self.recurring_var, font=self.body_font)
        self.recurring_check.grid(row=1, column=0, sticky="w", pady=(0, 10))
        
        # Primary Button Style
        add_btn = ctk.CTkButton(input_frame, text="Add Task", font=self.body_font, command=self._handle_add_task)
        add_btn.grid(row=1, column=1, sticky="e", pady=(0, 10))
        
        # Stats Label
        self.stats_label = ctk.CTkLabel(self, text="", font=self.body_font)
        self.stats_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        # Scrollable Task List
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

    def _handle_add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            return
            
        priority = self.priority_var.get()
        
        if self.recurring_var.get():
            task = RecurringTask(title, priority)
        else:
            task = SimpleTask(title, priority)
            
        self.manager.add_task(task)
        self.title_entry.delete(0, "end")
        self.recurring_var.set(False)
        self._refresh_task_list()

    def _handle_toggle(self, task_id: str):
        self.manager.toggle_complete(task_id)
        self._refresh_task_list()
        
    def _handle_delete(self, task_id: str):
        if messagebox.askyesno("Confirm", "Delete this task?"):
            self.manager.remove_task(task_id)
            self._refresh_task_list()

    def _refresh_task_list(self):
        # Clear existing task widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        tasks = self.manager.get_all_tasks()
        
        for idx, task in enumerate(tasks):
            # This demonstrates Polymorphism: we call display_info() on 'task'
            # without knowing if it's a SimpleTask or RecurringTask.
            # Python determines which overridden method to execute at runtime.
            display_text = task.display_info()
            
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=8)
            card.grid(row=idx, column=0, sticky="ew", pady=(0, 10), padx=5)
            card.grid_columnconfigure(1, weight=1)
            
            check_var = ctk.BooleanVar(value=task.is_completed)
            check = ctk.CTkCheckBox(card, text="", variable=check_var, width=20,
                                    command=lambda t_id=task.id: self._handle_toggle(t_id))
            check.grid(row=0, column=0, padx=12, pady=12)
            
            # Simple text color change for completed items
            label_color = "gray" if task.is_completed else "white"
            label = ctk.CTkLabel(card, text=display_text, font=self.body_font, text_color=label_color)
            label.grid(row=0, column=1, sticky="w", padx=5, pady=12)
            
            # Secondary Outline Button Style
            del_btn = ctk.CTkButton(card, text="Delete", fg_color="transparent", border_width=1, 
                                    text_color=("gray10", "gray90"), width=60, font=self.body_font,
                                    command=lambda t_id=task.id: self._handle_delete(t_id))
            del_btn.grid(row=0, column=2, padx=12, pady=12)
            
        # Update Stats
        total, completed, pending = self.manager.get_stats()
        self.stats_label.configure(text=f"Total: {total} | Completed: {completed} | Pending: {pending}")
