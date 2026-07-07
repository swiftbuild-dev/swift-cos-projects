# What This Does
This is a lightweight Tic-Tac-Toe desktop game built in Python using CustomTkinter. It allows a human player to play against an automated computer opponent on a clean, modern 3x3 interface.

# The Four Pillars

## Abstraction
The `Player` class defines a strict blueprint, ensuring all types of players implement their own logic for selecting a move without exposing how they do it.
```python
class Player(ABC):
    @abstractmethod
    def get_move(self, board: list[str]) -> int:
        pass
```

## Inheritance
`HumanPlayer` and `ComputerPlayer` build upon the abstract `Player` class, adopting its required structure while injecting their own specific behavior for deciding a turn.
```python
class ComputerPlayer(Player):
    def get_move(self, board: list[str]) -> int:
        empty_cells = [i for i, cell in enumerate(board) if cell == ""]
        if empty_cells:
            return random.choice(empty_cells)
        return -1
```

## Encapsulation
The `TicTacToe` class restricts direct access to the game's internal state, exposing only safe, controlled methods like `play_move` and `reset` to manage its internal lists and strings.
```python
class TicTacToe:
    def __init__(self):
        self._board = [""] * 9
        self._current_symbol = "X"
        
    def play_move(self, index: int) -> None:
        if self._board[index] == "":
            self._board[index] = self._current_symbol
            self._current_symbol = "O" if self._current_symbol == "X" else "X"
```

## Polymorphism
The user interface requests a move from whoever the active player is, relying entirely on the player object itself to respond appropriately—avoiding complex type-checking logic.
```python
# Polymorphism: We just ask the active player for their move. The game doesn't 
# need to know if it's the Human returning a click or the Computer generating one.
move = active_player.get_move(self.game.get_board())

if move != -1 and self.game.get_board()[move] == "":
    self.game.play_move(move)
```
