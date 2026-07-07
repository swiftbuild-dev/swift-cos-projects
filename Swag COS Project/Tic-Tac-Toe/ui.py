# pyrefly: ignore [missing-import]
import customtkinter as ctk
from main import TicTacToe, HumanPlayer, ComputerPlayer

class TicTacToeUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Tic-Tac-Toe")
        self.geometry("380x480")
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")
        
        self.game = TicTacToe()
        self.players = {
            "X": HumanPlayer(),
            "O": ComputerPlayer()
        }
        
        self.accent = "#3B82F6"  
        self.neutral = "#4B5563"
        self.font_main = ("Inter", 16, "bold")
        self.font_large = ("Inter", 36, "bold")
        
        self.card = ctk.CTkFrame(
            self, width=340, height=440, fg_color="#FFFFFF",
            border_color="#E5E7EB", border_width=2, corner_radius=12
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.grid_propagate(False)
        self.card.pack_propagate(False)
        
        self.status = ctk.CTkLabel(
            self.card, text="Player X's Turn", font=self.font_main, text_color="#111827"
        )
        self.status.pack(pady=(20, 10))
        
        self.board_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.board_frame.pack(padx=20, pady=10)
        
        self.buttons = []
        for i in range(9):
            btn = ctk.CTkButton(
                self.board_frame, text="", width=90, height=90,
                fg_color="#FFFFFF", hover_color="#F3F4F6",
                border_color="#E5E7EB", border_width=2,
                corner_radius=8, font=self.font_large,
                command=lambda idx=i: self.on_click(idx)
            )
            btn.grid(row=i//3, column=i%3, padx=4, pady=4)
            self.buttons.append(btn)
            
        self.reset_btn = ctk.CTkButton(
            self.card, text="Play Again", width=200, height=40,
            fg_color=self.accent, hover_color="#2563EB", text_color="#FFFFFF",
            font=self.font_main, corner_radius=8, command=self.reset_game
        )
        self.reset_btn.pack(pady=(20, 0))
        
    def on_click(self, index: int):
        self.process_turn(index)
        
    def process_turn(self, index: int | None = None):
        if self.game.check_winner() or self.game.is_full():
            return
            
        active_player = self.players[self.game.get_current_symbol()]
        active_player.clicked_index = index
        
        # Polymorphism: We just ask the active player for their move. The game doesn't 
        # need to know if it's the Human returning a click or the Computer generating one.
        move = active_player.get_move(self.game.get_board())
        
        if move != -1 and self.game.get_board()[move] == "":
            self.game.play_move(move)
            self.update_ui()
            
            if not self.game.check_winner() and not self.game.is_full():
                self.after(500, self.process_turn)
                
    def update_ui(self):
        for i, cell in enumerate(self.game.get_board()):
            color = self.accent if cell == "X" else self.neutral
            self.buttons[i].configure(text=cell, text_color=color)
            
        winner = self.game.check_winner()
        if winner:
            self.status.configure(text=f"{winner} Wins!", text_color=self.accent if winner == "X" else self.neutral)
        elif self.game.is_full():
            self.status.configure(text="It's a Draw!", text_color="#111827")
        else:
            current = self.game.get_current_symbol()
            self.status.configure(text=f"Player {current}'s Turn", text_color="#111827")
            
    def reset_game(self):
        self.game.reset()
        for player in self.players.values():
            player.clicked_index = None
        self.update_ui()

if __name__ == "__main__":
    app = TicTacToeUI()
    app.mainloop()
