# Tic-Tac-Toe GUI

## 🚀 Core Functionality
A classic Tic-Tac-Toe game where you play as **X** against a computer opponent (**O**). Click any empty cell to make your move. The computer responds automatically after half a second. The game detects wins and draws, and you can reset for another round with the "Play Again" button.

## 🧠 The Four Pillars of OOP (Object-Oriented Programming)

### 1. 🔒 Abstraction — *Hiding the complex details*
Abstraction is like ordering food at a restaurant — you ask for a burger without knowing how the kitchen makes it. `Player` is the abstract blueprint that says: *"any player must be able to provide a move"*. It hides whether that move comes from a human click or a computer algorithm.

```python
# Every player type MUST be able to return a move.
# The base Player class doesn't say HOW — that's up to each player type.
class Player(ABC):
    @abstractmethod
    def get_move(self, board: list[str]) -> int:
        pass
```

### 2. 👪 Inheritance — *Passing down traits*
Inheritance is like a child using their parent's name. `HumanPlayer` and `ComputerPlayer` both inherit the structure of `Player`. They are recognized as valid players by the game, and they each just fill in the `get_move()` logic in their own way.

```python
# HumanPlayer inherits from Player and returns whatever cell the user clicked.
class HumanPlayer(Player):
    def get_move(self, board: list[str]) -> int:
        move = self.clicked_index
        self.clicked_index = None
        return move if move is not None else -1

# ComputerPlayer inherits from Player and picks a random empty cell.
class ComputerPlayer(Player):
    def get_move(self, board: list[str]) -> int:
        empty_cells = [i for i, cell in enumerate(board) if cell == ""]
        return random.choice(empty_cells) if empty_cells else -1
```

### 3. 🔄 Polymorphism — *Many forms, one call*
Polymorphism is the most powerful feature in this game. When processing a turn, the game calls `get_move()` on the active player. It doesn't need to know if it's a human or a computer — the right logic runs automatically. This is what lets the computer play right after the human without any special checks.

```python
# One line handles BOTH human and computer turns perfectly.
# Python knows which type 'active_player' is and calls the right method.
move = active_player.get_move(self.game.get_board())
```

### 4. 📦 Encapsulation — *Protecting the data*
Encapsulation keeps the game state safe. The `TicTacToe` class stores the board (`_board`) and whose turn it is (`_current_symbol`) as private variables. The UI cannot directly change them — it must go through `play_move()` and `reset()`, which enforce the game's rules.

```python
class TicTacToe:
    def __init__(self):
        # Private variables. The UI must use play_move() to make changes.
        self._board = [""] * 9
        self._current_symbol = "X"
```
