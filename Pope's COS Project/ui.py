# pyrefly: ignore [missing-import]
import customtkinter as ctk
from main import Poll, SingleChoicePoll, MultiChoicePoll

# Setup clean, modern appearance
ctk.set_appearance_mode("light")

class PollApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Voting App")
        self.geometry("400x500")
        self.configure(fg_color="#FFFFFF")
        
        self.options = ["Python", "JavaScript", "Java", "C++"]
        self.poll: Poll = SingleChoicePoll(self.options)
        
        self.checkboxes = []
        self.checkbox_vars = []
        
        self._build_ui()
        self._update_results_display()

    def _build_ui(self):
        # Fixed-width content frame
        self.content_frame = ctk.CTkFrame(
            self, width=340, fg_color="#FFFFFF", 
            border_width=1, border_color="#E5E5E5", corner_radius=8
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_lbl = ctk.CTkLabel(
            self.content_frame, text="Best Programming Language?", 
            font=("Arial", 18, "bold"), text_color="#111111"
        )
        title_lbl.pack(pady=(20, 10), padx=20)
        
        # Poll Type Dropdown
        self.poll_type_var = ctk.StringVar(value="Single Choice")
        self.poll_type_dropdown = ctk.CTkOptionMenu(
            self.content_frame, values=["Single Choice", "Multi Choice"],
            variable=self.poll_type_var, command=self._on_poll_type_change,
            fg_color="#F0F0F0", text_color="#111111", button_color="#E5E5E5",
            button_hover_color="#DDDDDD", font=("Arial", 14)
        )
        self.poll_type_dropdown.pack(pady=(0, 15), padx=20, fill="x")
        
        # Poll Options (Checkboxes)
        for opt in self.options:
            var = ctk.StringVar(value="")
            self.checkbox_vars.append(var)
            cb = ctk.CTkCheckBox(
                self.content_frame, text=opt, variable=var, onvalue=opt, offvalue="",
                fg_color="#0052CC", border_color="#CCCCCC", hover_color="#003D99",
                text_color="#333333", font=("Arial", 14),
                command=lambda current_var=var: self._on_checkbox_click(current_var)
            )
            cb.pack(pady=5, padx=20, anchor="w")
            self.checkboxes.append(cb)
            
        # Submit Button
        self.submit_btn = ctk.CTkButton(
            self.content_frame, text="Submit Vote",
            fg_color="#0052CC", hover_color="#003D99", text_color="#FFFFFF",
            font=("Arial", 14, "bold"), command=self._submit_vote
        )
        self.submit_btn.pack(pady=(15, 10), padx=20, fill="x")
        
        # Results Container
        self.results_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.results_container.pack(pady=5, padx=20, fill="x")
        
        # Reset Button
        self.reset_btn = ctk.CTkButton(
            self.content_frame, text="Reset Poll",
            fg_color="#FFFFFF", hover_color="#F5F5F5", text_color="#0052CC",
            border_width=1, border_color="#0052CC",
            font=("Arial", 14, "bold"), command=self._reset_poll
        )
        self.reset_btn.pack(pady=(10, 20), padx=20, fill="x")

    def _on_checkbox_click(self, clicked_var: ctk.StringVar):
        # Restrict to one selection if Single Choice is active
        if self.poll_type_var.get() == "Single Choice":
            for var in self.checkbox_vars:
                if var != clicked_var:
                    var.set("")

    def _on_poll_type_change(self, choice: str):
        # Change poll type and clear selections
        if choice == "Single Choice":
            self.poll = SingleChoicePoll(self.options)
        else:
            self.poll = MultiChoicePoll(self.options)
            
        for var in self.checkbox_vars:
            var.set("")
        self._update_results_display()

    def _submit_vote(self):
        selected = [var.get() for var in self.checkbox_vars if var.get() != ""]
        if not selected:
            return
            
        # Polymorphism: The app calls record_vote without checking the poll type!
        # SingleChoicePoll cleanly handles a single string. 
        # MultiChoicePoll parses a comma-separated string of all choices.
        options_str = ",".join(selected)
        self.poll.record_vote(options_str)
        
        # Clear UI selections after voting
        for var in self.checkbox_vars:
            var.set("")
            
        self._update_results_display()

    def _reset_poll(self):
        # Simulates a reset by re-instantiating the current poll type
        self._on_poll_type_change(self.poll_type_var.get())
        
    def _update_results_display(self):
        # Clear old results
        for widget in self.results_container.winfo_children():
            widget.destroy()
            
        results = self.poll.get_results()
        for i, (opt, count) in enumerate(results.items()):
            row = ctk.CTkFrame(self.results_container, fg_color="transparent")
            row.pack(fill="x", pady=2)
            
            lbl = ctk.CTkLabel(row, text=f"{opt}: {count} votes", font=("Arial", 14), text_color="#333333")
            lbl.pack(anchor="w")
            
            # Thin light-gray divider
            if i < len(results) - 1:
                divider = ctk.CTkFrame(self.results_container, fg_color="#E5E5E5", height=1)
                divider.pack(fill="x", pady=2)
