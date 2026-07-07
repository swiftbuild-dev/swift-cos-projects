# pyrefly: ignore [missing-import]
import customtkinter as ctk
from typing import Optional
from user import UserManager, Account

ACCENT_COLOR = "#0066CC"
TEXT_COLOR = "#333333"
BG_COLOR = "#FFFFFF"
ERROR_COLOR = "#CC0000"
BORDER_COLOR = "#E0E0E0"
FONT_MAIN = ("Inter", 14)
FONT_TITLE = ("Inter", 24, "bold")

class LoginApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.user_manager = UserManager()
        self.current_user: Optional[Account] = None
        
        self.title("Authentication")
        self.geometry("400x500")
        self.configure(fg_color=BG_COLOR)
        
        self.card = ctk.CTkFrame(self, fg_color=BG_COLOR, width=320, height=450, corner_radius=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)
        
        self.show_login_screen()

    def clear_card(self) -> None:
        for widget in self.card.winfo_children():
            widget.destroy()

    def create_input(self, placeholder: str, is_password: bool = False) -> ctk.CTkEntry:
        return ctk.CTkEntry(
            self.card, placeholder_text=placeholder, font=FONT_MAIN,
            fg_color=BG_COLOR, text_color=TEXT_COLOR, border_color=BORDER_COLOR,
            border_width=1, height=40, show="*" if is_password else ""
        )

    def show_error(self, message: str) -> None:
        if hasattr(self, 'error_label') and self.error_label.winfo_exists():
            self.error_label.configure(text=message)
        else:
            self.error_label = ctk.CTkLabel(self.card, text=message, text_color=ERROR_COLOR, font=("Inter", 12))
            self.error_label.pack(pady=(0, 10))

    def show_login_screen(self) -> None:
        self.clear_card()
        ctk.CTkLabel(self.card, text="Log In", font=FONT_TITLE, text_color=TEXT_COLOR).pack(pady=(20, 30))
        
        self.login_user = self.create_input("Username")
        self.login_pass = self.create_input("Password", is_password=True)
        for widget in [self.login_user, self.login_pass]:
            widget.pack(fill="x", pady=(0, 16))
        
        ctk.CTkButton(self.card, text="Log In", font=FONT_MAIN, fg_color=ACCENT_COLOR, text_color="#FFFFFF", height=40, command=self.handle_login).pack(fill="x", pady=(10, 16))
        ctk.CTkButton(self.card, text="Don't have an account? Sign up", font=FONT_MAIN, fg_color="transparent", text_color=ACCENT_COLOR, hover=False, command=self.show_signup_screen).pack(pady=(10, 0))

    def show_signup_screen(self) -> None:
        self.clear_card()
        ctk.CTkLabel(self.card, text="Create Account", font=FONT_TITLE, text_color=TEXT_COLOR).pack(pady=(10, 20))
        
        self.reg_user = self.create_input("Username")
        self.reg_pass = self.create_input("Password", is_password=True)
        self.reg_pass2 = self.create_input("Confirm Password", is_password=True)
        for widget in [self.reg_user, self.reg_pass, self.reg_pass2]:
            widget.pack(fill="x", pady=(0, 12))
        
        self.reg_role = ctk.CTkOptionMenu(self.card, values=["Standard User", "Administrator"], font=FONT_MAIN, fg_color=BG_COLOR, text_color=TEXT_COLOR, button_color=BORDER_COLOR)
        self.reg_role.pack(fill="x", pady=(0, 12))
        
        ctk.CTkButton(self.card, text="Sign Up", font=FONT_MAIN, fg_color=ACCENT_COLOR, text_color="#FFFFFF", height=40, command=self.handle_signup).pack(fill="x", pady=(10, 12))
        ctk.CTkButton(self.card, text="Already have an account? Log in", font=FONT_MAIN, fg_color="transparent", text_color=ACCENT_COLOR, hover=False, command=self.show_login_screen).pack()

    def show_welcome_screen(self) -> None:
        self.clear_card()
        # Polymorphism: We call get_role_label() without checking the account type. 
        # The correct method for StandardUser or AdminUser runs automatically.
        role_label = self.current_user.get_role_label()
        
        ctk.CTkLabel(self.card, text=f"Welcome, {self.current_user.username}", font=FONT_TITLE, text_color=TEXT_COLOR).pack(pady=(50, 10))
        ctk.CTkLabel(self.card, text=f"({role_label})", font=FONT_MAIN, text_color=TEXT_COLOR).pack(pady=(0, 30))
        ctk.CTkButton(self.card, text="Log Out", font=FONT_MAIN, fg_color=ACCENT_COLOR, text_color="#FFFFFF", height=40, command=self.handle_logout).pack(fill="x")

    def handle_login(self) -> None:
        username, password = self.login_user.get().strip(), self.login_pass.get()
        if not username or not password:
            return self.show_error("Please fill in all fields")
            
        self.current_user = self.user_manager.login(username, password)
        if self.current_user:
            self.show_welcome_screen()
        else:
            self.show_error("Invalid username or password")

    def handle_signup(self) -> None:
        user, pwd, conf = self.reg_user.get().strip(), self.reg_pass.get(), self.reg_pass2.get()
        if not user or not pwd or not conf:
            return self.show_error("Please fill in all fields")
        if pwd != conf:
            return self.show_error("Passwords do not match")
            
        if self.user_manager.register(user, pwd, self.reg_role.get() == "Administrator"):
            self.show_login_screen()
        else:
            self.show_error("Username already exists")

    def handle_logout(self) -> None:
        self.current_user = None
        self.show_login_screen()
