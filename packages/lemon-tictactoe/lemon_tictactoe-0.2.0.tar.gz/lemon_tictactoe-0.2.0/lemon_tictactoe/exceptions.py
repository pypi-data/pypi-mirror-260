class CellOccupiedException(Exception):
    """
    Raised when a chosen board cell is already occupied.
    """
    pass

class WrongPlayerException(Exception):
    """
    Raised when the wrong player was chosen for a TicTacToe action.
    """
    pass

class GameStartedException(Exception):
    """
    Raised when a TicTacToe action is taken that is disallowed after the game has started.
    """
    pass

class GameFinishedException(Exception):
    """
    Raised when a TicTacToe action is taken that is disallowed after the game has ended.
    """
    pass