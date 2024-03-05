# Lemon-TicTacToe
A tic tac toe python library aiming to make it easy to implement TicTacToe into whatever project you like.  
My first attempt at making a python library.

## Features
- Creating TicTacToe games of various board sizes
- Interacting with the game without a forced event loop

## Requirements
- Python 3.9 or higher

## Getting started
```
pip install lemon-tictactoe
```

---

# Usage
## Setting up the game
You can easily create a game by instantiating the Game class.  
The default options will result in a traditional TicTacToe game.  
```py
from lemon_tictactoe import Game

game = Game()
```

But you are also able to pass various configuration options to get a more custom experience:  
```py
from lemon_tictactoe import Game

game = Game(board_size=10, player_count=5, starting_player=2)
```

## Grid coordinates
The coordinates (0, 0) are at the top left of the board.  
Here is a visual representation of the board coordinates (x, y) with board_size=3:  
<img src="/images/TicTacToe_Grid.png" width="300" height="300">

## Playing moves
You can use the Game.move method, specifying a player and x,y coordinates to play a move.  
This will make Player 1 play their move on x=1 and y=2:  
```py
win = game.move(1, 1, 2)
```
The move method will return True if it lead to a win of the specified player.  

## Handling invalid move input
Sometimes players might do moves which are not allowed, you can catch errors to handle these cases:  
```py
from lemon_tictactoe import Game, CellOccupiedError, WrongPlayerError

game = Game()

try:
    game.move(1, 1, 2)
except ValueError:
    print("Move out of bounds or otherwise invalid input.")
except CellOccupiedError:
    print("The specified cell is already occupied.")
except WrongPlayerError:
    print("Wrong player tried to play a turn.")
```
