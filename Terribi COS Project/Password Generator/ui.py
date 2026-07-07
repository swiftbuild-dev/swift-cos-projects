# pyrefly: ignore [missing-import]
import customtkinter as ctk
from password_policy import PasswordGenerator, SimplePolicy, StrongPolicy

MAIN_FONT = ("Helvetica", 14)
PASS_FONT = ("Courier", 24, "bold")

class PasswordApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Password Generator")
        self.geometry("400x450")
        
        # UI Requirement: Pure white background for main window
        ctk.set_appearance_mode("light")
        self.configure(fg_color="#FFFFFF")
        
        self.generator = PasswordGenerator()
        self.policies = {
            "Simple": SimplePolicy(),
            "Strong": StrongPolicy()
        }
        
        self._setup_ui()
        
    def _setup_ui(self):
        # UI Requirement: Content frame with thin light-gray border, fixed max width, centered
        self.card = ctk.CTkFrame(
            self, width=360, fg_color="#FFFFFF", border_width=1, 
            border_color="#E0E0E0", corner_radius=10
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        # We need to let the frame size properly while acting as a fixed width container.
        # By setting the width in the Frame and relying on internal layout sizes, we can maintain it.
        # Using pack_propagate(False) keeps the frame from shrinking, but we need a fixed height too if we do that.
        # Instead, we just pad the internal elements consistently.
        
        self.title_label = ctk.CTkLabel(
            self.card, text="Password Generator", font=("Helvetica", 20, "bold"), text_color="#333333"
        )
        self.title_label.pack(pady=16, padx=16)
        
        self.password_display = ctk.CTkLabel(
            self.card, text="Your Password", font=PASS_FONT, width=320, height=50,
            fg_color="#F5F5F5", border_width=1, border_color="#CCCCCC", text_color="#111111", corner_radius=8
        )
        self.password_display.pack(pady=16, padx=16)
        
        self.options_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.options_frame.pack(pady=16, padx=16, fill="x")
        
        self.policy_var = ctk.StringVar(value="Strong")
        self.policy_dropdown = ctk.CTkOptionMenu(
            self.options_frame, values=["Simple", "Strong"], variable=self.policy_var,
            width=120, font=MAIN_FONT, fg_color="#FFFFFF", button_color="#FFFFFF",
            button_hover_color="#F0F0F0", text_color="#333333"
        )
        # Using generic configuration for border since older CTk might handle borders differently on option menus
        # but modern CustomTkinter supports these if passed, or we just rely on fg_color.
        self.policy_dropdown.pack(side="left", padx=(0, 10))
        
        self.slider_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        self.slider_frame.pack(side="right", fill="x", expand=True)
        
        self.length_var = ctk.IntVar(value=12)
        self.length_label = ctk.CTkLabel(self.slider_frame, text="Length: 12", font=MAIN_FONT, text_color="#555555")
        self.length_label.pack(side="top")
        
        self.length_slider = ctk.CTkSlider(
            self.slider_frame, from_=6, to=24, variable=self.length_var, number_of_steps=18,
            command=self._update_length_label, button_color="#0066FF", button_hover_color="#0052CC", progress_color="#0066FF"
        )
        self.length_slider.pack(side="bottom")
        
        self.generate_btn = ctk.CTkButton(
            self.card, text="Generate", command=self._on_generate, font=MAIN_FONT,
            fg_color="#0066FF", hover_color="#0052CC", text_color="#FFFFFF", width=320, height=40, corner_radius=8
        )
        self.generate_btn.pack(pady=16, padx=16)
        
        self.copy_btn = ctk.CTkButton(
            self.card, text="Copy to Clipboard", command=self._on_copy, font=MAIN_FONT,
            fg_color="#FFFFFF", hover_color="#F5F5F5", text_color="#0066FF",
            border_width=2, border_color="#0066FF", width=320, height=40, corner_radius=8
        )
        self.copy_btn.pack(pady=16, padx=16)
        
        self.copied_label = ctk.CTkLabel(self.card, text="", text_color="#008000", font=MAIN_FONT)
        self.copied_label.pack(pady=(0, 16))

    def _update_length_label(self, value):
        self.length_label.configure(text=f"Length: {int(value)}")

    def _on_generate(self):
        selected_policy = self.policies[self.policy_var.get()]
        length = self.length_var.get()
        password = self.generator.create_password(selected_policy, length)
        
        self.password_display.configure(text=password)
        self.copied_label.configure(text="")
        
    def _on_copy(self):
        password = self.password_display.cget("text")
        if password and password != "Your Password":
            self.clipboard_clear()
            self.clipboard_append(password)
            self.copied_label.configure(text="Copied!")
            self.after(2000, lambda: self.copied_label.configure(text=""))
