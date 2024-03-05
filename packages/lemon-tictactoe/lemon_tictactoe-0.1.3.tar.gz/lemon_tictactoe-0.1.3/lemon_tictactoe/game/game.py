from lemon_tictactoe.constants.exceptions import TicTacToeValidationError
from lemon_tictactoe.utils.validator import validate_in_between, validate_of_type

MIN_BOARD_SIZE = 3
MAX_BOARD_SIZE = 100

class Game():
    """
    A class designed to encapsulate all TicTacToe game mechanics.
    It acts as an API to start and control custom TicTacToe games.
    """    
    def __init__(self, board_size: int = 3, log_moves: bool = False) -> None:
        """Will create a fresh new TicTacToe game instance.

        Args:
            board_size (int, optional): The horizontal and vertical size of the TicTacToe board. Has to be in between 3 and 100. Defaults to 3.
            log_moves (bool, optional): If moves should be kept track of. Defaults to False.
        """
        try:
            validate_in_between(board_size, MIN_BOARD_SIZE, MAX_BOARD_SIZE, "board_size")
            validate_of_type(log_moves, bool, "log_moves")
        except ValueError as e:
            raise TicTacToeValidationError(f"An error occured while trying to initialize TicTacToe game: {e}")
        
        self.board_size = board_size
        self.log_moves = log_moves