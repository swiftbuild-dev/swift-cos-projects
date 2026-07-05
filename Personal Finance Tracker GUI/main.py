# pyrefly: ignore [missing-import]
import customtkinter as ctk
from finance_manager import FinanceManager
from ui import FinanceTrackerUI

def main():
    # Set the overall appearance mode
    ctk.set_appearance_mode("light")
    
    # Initialize the core application components
    root = ctk.CTk()
    manager = FinanceManager()
    
    # Bind the UI to the root window and the manager
    app = FinanceTrackerUI(root, manager)
    
    # Start the event loop
    root.mainloop()

if __name__ == "__main__":
    main()
