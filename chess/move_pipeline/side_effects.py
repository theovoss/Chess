from chess.board.json_helper import add_unit_direction
from chess.board.history import History


def move(board, initial_location, **kwargs):
    start = add_unit_direction(initial_location, kwargs['start'])
    end = add_unit_direction(initial_location, kwargs['end'])
    board[end] = board[start]
    board[start] = None

    return History.construct_side_effect("move", start=start, end=end)
