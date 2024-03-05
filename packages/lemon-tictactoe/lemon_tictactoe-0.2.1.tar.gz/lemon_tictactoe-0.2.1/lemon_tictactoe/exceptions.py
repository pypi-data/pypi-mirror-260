class CellOccupiedError(Exception):
    """
    Raised when a chosen board cell is already occupied.
    """
    pass

class WrongPlayerError(Exception):
    """
    Raised when the wrong player was chosen for a TicTacToe action.
    """
    pass

class GameStartedError(Exception):
    """
    Raised when a TicTacToe action is taken that is disallowed after the game has started.
    """
    pass

class GameFinishedError(Exception):
    """
    Raised when a TicTacToe action is taken that is disallowed after the game has ended.
    """
    pass