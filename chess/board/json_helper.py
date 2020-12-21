from chess.move_pipeline import capture_actions, post_move_actions

from chess.helpers import add_unit_direction
from chess.chess_configurations import get_standard_chess_pieces

default_capture_actions = ['captures_destination']
default_post_move_actions = ['increment_move_count']
default_side_effects = []


def get_piece_moves(name, json_data):
    return json_data['pieces'][name]['moves']


def load_json(json_data=None):
    if json_data:
        return json_data

    return get_standard_chess_pieces()


def get_capture_actions(move):
    action_names = default_capture_actions
    if move and 'capture_actions' in move:
        action_names = move['capture_actions']

    return [getattr(capture_actions, action) for action in action_names if hasattr(capture_actions, action)]


def get_additional_captures(board, start, move):
    if move and 'capture_at' in move:
        ret_val = {}
        for relative_direction in move['capture_at']:
            location = add_unit_direction(start, relative_direction)
            ret_val[location] = board[location]
        return ret_val
    return []


def get_post_move_actions(move):
    post_actions = default_post_move_actions
    if move and 'post_move_actions' in move:
        post_actions = move['post_move_actions']

    return [getattr(post_move_actions, action) for action in post_actions if hasattr(post_move_actions, action)]


def get_side_effects(move):
    if move and 'side_effects' in move:
        return move['side_effects']

    return default_side_effects
