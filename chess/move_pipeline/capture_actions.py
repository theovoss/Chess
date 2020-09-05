# pylint: disable=W0613
# allow unused variables so all capture action functions can have same parameter definition
from chess.helpers import add_unit_direction


def capture(board, start, end, **kwargs):
    ret_val = {}
    locations = [add_unit_direction(start, location) for location in kwargs['locations']]
    for location in locations:
        ret_val[location] = board[location]
    return ret_val


def captures_destination(board, start, end, **kwargs):
    return {end: board[end]}


def becomes_piece(board, start, end, **kwargs):
    captured = {end: board[end]}
    enemy_piece = board[end]
    moving_piece = board[start]

    enemy_piece.color = moving_piece.color
    enemy_piece.move_count = moving_piece.move_count

    board[start] = enemy_piece

    return captured


def explode(board, start, end, **kwargs):
    captured = {end: board[end]}

    for place in board.get_surrounding_locations(end):
        if place[0] < 0 or place[1] < 0:
            continue
        if board[place]:
            captured[place] = board[place]
    return captured
