from abc import ABC, abstractmethod
import random

# Abstraction: Player serves as a blueprint. The game doesn't care how 
# a player decides their move, only that they implement get_move().
class Player(ABC):
    @abstractmethod
    def get_move(self, board: list[str]) -> int:
        pass

# Inheritance: HumanPlayer inherits the requirements of Player but provides
# its own specific implementation driven by UI clicks.
class HumanPlayer(Player):
    def __init__(self):
        self.clicked_index: int | None = None
        
    def get_move(self, board: list[str]) -> int:
        if self.clicked_index is not None:
            move = self.clicked_index
            self.clicked_index = None 
            return move
        return -1

# Inheritance: ComputerPlayer inherits from Player and implements automated logic.
class ComputerPlayer(Player):
    def get_move(self, board: list[str]) -> int:
        empty_cells = [i for i, cell in enumerate(board) if cell == ""]
        if empty_cells:
            return random.choice(empty_cells)
        return -1

# Encapsulation: TicTacToe hides its internal state (_board, _current_symbol) 
# and provides controlled methods to interact with the game.
class TicTacToe:
    def __init__(self):
        self._board = [""] * 9
        self._current_symbol = "X"
        
    def play_move(self, index: int) -> None:
        if self._board[index] == "":
            self._board[index] = self._current_symbol
            self._current_symbol = "O" if self._current_symbol == "X" else "X"
            
    def check_winner(self) -> str | None:
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), 
            (0, 3, 6), (1, 4, 7), (2, 5, 8), 
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in lines:
            if self._board[a] and self._board[a] == self._board[b] == self._board[c]:
                return self._board[a]
        return None
        
    def is_full(self) -> bool:
        return "" not in self._board
        
    def reset(self) -> None:
        self._board = [""] * 9
        self._current_symbol = "X"
        
    def get_board(self) -> list[str]:
        return self._board.copy()
        
    def get_current_symbol(self) -> str:
        return self._current_symbol
