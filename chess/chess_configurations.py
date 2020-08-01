import json
import inspect
from chess import movement
from chess import capture_actions
from chess import standard_chess_json
from chess.piece.directions import get_direction_shorthands


def get_movement_rules():
    movements = inspect.getmembers(movement)
    return [rule[0] for rule in movements if rule[0][0] != '_' and rule[0] != "get_all_potential_end_locations"]


def get_capture_action_rules():
    actions = inspect.getmembers(capture_actions)
    return [rule[0] for rule in actions if rule[0][0] != '_']


def get_movement_directions():
    return get_direction_shorthands()


def get_standard_chess_pieces():
    filename = standard_chess_json
    data = None
    with open(filename) as data_file:
        data = json.load(data_file)

    return data
