from finance_manager import FinanceManager
from ui import FinanceTrackerUI

def main():
    # Encapsulation: The system state is initialized in an isolated manager.
    manager = FinanceManager()
    
    # We pass the manager to the UI, avoiding global variables.
    app = FinanceTrackerUI(manager)
    
    app.mainloop()

if __name__ == "__main__":
    main()
