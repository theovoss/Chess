from .. import movement
from .. import capture_actions
from .. import post_move_actions

from ..chess_configurations import get_standard_chess_pieces

default_capture_actions = ['captures_destination']
default_post_move_actions = ['increment_move_count']


def get_piece_moves(name, json_data):
    return json_data['pieces'][name]['moves']


def load_json(json_data=None):
    if json_data:
        return json_data

    return get_standard_chess_pieces()


def _get_move_definition(piece, start, end):
    unit_direction = list(movement.get_unit_direction(start, end))

    for move in piece.moves:
        if unit_direction in move['directions']:
            return move
    return None


def get_capture_actions(piece, start, end):
    move = _get_move_definition(piece, start, end)

    action_names = default_capture_actions
    if move and 'capture_actions' in move:
        action_names = move['capture_actions']

    return [getattr(capture_actions, action) for action in action_names if hasattr(capture_actions, action)]


def get_post_move_actions(piece, start, end):
    move = _get_move_definition(piece, start, end)

    post_actions = default_post_move_actions
    if move and 'post_move_actions' in move:
        post_actions = move['post_move_actions']

    return [getattr(post_move_actions, action) for action in post_actions if hasattr(post_move_actions, action)]
