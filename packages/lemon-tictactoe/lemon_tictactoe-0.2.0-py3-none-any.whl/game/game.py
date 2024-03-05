from lemon_tictactoe.utils.validator import validate_in_between

MIN_BOARD_SIZE = 3
MAX_BOARD_SIZE = 100

class Game():
    """
    A class designed to encapsulate all TicTacToe game mechanics.
    It acts as an API to start and control custom TicTacToe games.
    """    
    def __init__(self, board_size: int = 3) -> None:
        """
        Will create a fresh new TicTacToe game instance.

        Args:
            board_size (int, optional): The horizontal and vertical size of the TicTacToe board. Defaults to 3.
        """
        validate_in_between(board_size, MIN_BOARD_SIZE, MAX_BOARD_SIZE, "board_size")
        self.board_size = board_size