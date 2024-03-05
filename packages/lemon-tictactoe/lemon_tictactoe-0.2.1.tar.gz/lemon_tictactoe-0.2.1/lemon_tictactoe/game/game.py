from typing import Optional
from lemon_tictactoe import exceptions
from lemon_tictactoe.utils.validator import validate_in_between, validate_items_of_type, validate_maximum, validate_of_type

MAX_BOARD_SIZE = 100

class Game():
    """
    A class designed to encapsulate all TicTacToe game mechanics.
    It acts as an API to start and control custom TicTacToe games.

    Board coordinates start in the upper left with (0, 0).
    """    
    def __init__(self, board_size: int = 3, player_count: int = 2, starting_player: int = 1, player_names: Optional[list[str]] = None, log_moves: bool = False) -> None:    
        """Will create a new TicTacToe game instance.

        Args:
            board_size (int, optional): The horizontal and vertical size of the TicTacToe board. Has to be in between 3 and 100. Defaults to 3.
            player_count (int, optional): The amount of players that will participate at the game. Cannot be greater than the board size. Defaults to 2.
            starting_player (int, optional): The player number of the player who is supposed to start the game. Defaults to 1.
            player_names (Optional[list[str]], optional): Will set the provided player names on initialization. No player has to be named, use set_player_name for manual name customization. Defaults to None.
            log_moves (bool, optional): If moves should be kept track of. Defaults to False.
        Raises:
            ValueError: On invalid input.
        """
        player_names = player_names if player_names is not None else []

        try:
            validate_in_between(board_size, 3, MAX_BOARD_SIZE, "board_size")
            validate_in_between(player_count, 2, board_size, "player_count")
            validate_in_between(starting_player, 1, player_count, "starting_player")
            validate_maximum(len(player_names), player_count, "length of player_names")
            validate_items_of_type(player_names, str, "player_names", "names")
            validate_of_type(log_moves, bool, "log_moves")
        except ValueError as e:
            raise ValueError(f"An error occured while trying to initialize TicTacToe game: {e}")
        
        self.board_size = board_size
        self.player_count = player_count
        self.log_moves = log_moves

        # INITIALIZATION
        self.players: dict[int, str] = {i: f"Player {i}" for i in range(1, player_count + 1)}
        for i, name in enumerate(player_names):
            self.players[i+1] = name

        self._board = [[0]*board_size for _ in range(board_size)]
        self._next_moving_player = starting_player
        self._started = False
        self._finished = False
        self.winner = 0

        # WIN CONDITION HANDLING
        # Prevents the use of loops to check win conditions
        self._row_counts = [{i: 0 for i in range(1, player_count + 1)} for _ in range(board_size)]
        self._column_counts = [{i: 0 for i in range(1, player_count + 1)} for _ in range(board_size)]
        self._topleft_bottomright = {i: 0 for i in range(1, player_count + 1)}
        self._bottomleft_topright = {i: 0 for i in range(1, player_count + 1)}

    def _increment_player(self) -> None:
        self._next_moving_player += 1
        if self._next_moving_player > self.player_count:
            self._next_moving_player = 1

    def _check_game_not_started(self) -> None:
        if self._finished:
            raise exceptions.GameStartedError()

    def _check_game_not_finished(self) -> None:
        if self._finished:
            raise exceptions.GameFinishedError()

    # Returns true if one of the win conditions is met
    def _count_win_condition(self, player_number: int, x: int, y: int) -> bool:
        win = self._add_column_count(row=x, player_number=player_number)
        if win:
            return True
        
        win = self._add_row_count(row=y, player_number=player_number)
        if win:
            return True
        
        if x == y:
            win = self._add_topleft_bottomright(player_number=player_number)
            if win:
                return True
        
        if x + y == self.board_size - 1:
            win = self._add_bottomleft_topright(player_number=player_number)
            if win:
                return True
        
        return False

    # Returns true if the win condition is met
    def _add_row_count(self, row: int, player_number: int) -> bool:
        self._row_counts[row][player_number] += 1
        if self._row_counts[row][player_number] == self.board_size:
            return True
        return False
    
    # Returns true if the win condition is met
    def _add_column_count(self, row: int, player_number: int) -> bool:
        self._column_counts[row][player_number] += 1
        if self._column_counts[row][player_number] == self.board_size:
            return True
        return False
    
    # Returns true if the win condition is met
    def _add_topleft_bottomright(self, player_number: int) -> bool:
        self._topleft_bottomright[player_number] += 1
        if self._topleft_bottomright[player_number] == self.board_size:
            return True
        return False
    
    # Returns true if the win condition is met
    def _add_bottomleft_topright(self, player_number: int) -> bool:
        self._bottomleft_topright[player_number] += 1
        if self._bottomleft_topright[player_number] == self.board_size:
            return True
        return False
    
    def _start_game(self) -> None:
        self._started = True
    
    def _end_game(self, player_number: int) -> None:
        self._finished = True
        self.winner = player_number

    def set_player_name(self, player_number: int, name: str) -> None:
        """Will set the specified players name to the provided name

        Args:
            player_number (int): The number of the player to set the name of. Starts at 1.
            name (str): The name you want to assign to the player.

        Raises:
            ValueError: On invalid input.
            GameStartedError: When the game has already started.
            GameFinishedError: When the game has already finished.
        """
        self._check_game_not_started()
        self._check_game_not_finished()
        validate_in_between(player_number, 1, self.player_count, "player_number")
        validate_of_type(name, str, "name")
        self.players[player_number] = name

    def set_player_names(self, player_names: list[str]) -> None:
        """Will set the specified players names to the provided names

        Args:
            player_names (list[str]): The names you want to assign to the players. Does not have to include names for all players.

        Raises:
            ValueError: On invalid input.
            GameStartedError: When the game has already started.
            GameFinishedError: When the game has already finished.
        """
        self._check_game_not_started()
        self._check_game_not_finished()
        validate_maximum(len(player_names), self.player_count, "length of player_names")
        validate_items_of_type(player_names, str, "player_names", "names")
        for i, name in enumerate(player_names):
            self.set_player_name(player_number=i+1, name=name)

    def move(self, player_number: int, x: int, y: int) -> bool:       
        """
        Play a move for the specified player into a cell of the specified coordinates.
        Coordinates start with (0,0) in the top left.

        Args:
            player_number (int): The number of the player that is supposed to move. Has to be specified to ensure the correct player is moving.
            x (int): X-coordinate of the cell the specified player plays their move.
            y (int): Y-coordinate of the cell the specified player plays their move.

        Raises:
            ValueError: On invalid input.
            GameFinishedError: When the game has already finished.
            CellOccupiedError: When the specified cell coordinates are already occupied.
            WrongPlayerError: When the specified player is not supposed to move.

        Returns:
            bool: True if a win condition has been met, false if the game continues.
        """
        self._check_game_not_finished()
        self._start_game()
        validate_coordinates(self.board_size, x, y)
        if player_number != self._next_moving_player:
            raise exceptions.WrongPlayerError(f"Invalid move: next player is supposed to be {self._next_moving_player}")
        if self._board[x][y] != 0:
            raise exceptions.CellOccupiedError(f"Invalid move: cell ({x}, {y}) is already occupied")

        self._board[x][y] = player_number
        self._increment_player()

        win = self._count_win_condition(player_number=player_number, x=x, y=y)
        if win:
            self._end_game(player_number=player_number)

        return win

def validate_coordinates(size: int, x: int, y: int):
    validate_in_between(x, 0, size-1, "x")
    validate_in_between(y, 0, size-1, "y")