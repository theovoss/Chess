# pylint: disable=W0613
# allow unused variables so all movement functions can have same parameter definition
import operator as _operator
import copy as _copy

from chess.helpers import add_unit_direction as _add_unit_direction
from chess.move.pathfinder import PathFinder as _pathfinder


def get_all_potential_end_locations(start, directions, board):
    ends = []
    for direction in directions:
        new_start = start
        location = _add_unit_direction(new_start, direction)
        while location in board:
            ends.append(location)
            new_start = location
            location = _add_unit_direction(new_start, direction)
    return ends


def distance_of_two(args):
    return [x for x in _get_two_moves_away(args.start, args.directions) if x in args.ends]


def distance_of_one(args):
    return [x for x in _get_one_move_away(args.start, args.directions) if x in args.ends]


def cant_move_onto_threatened_square(args):
    if args.board[args.start] is None:
        return []

    threat_color = args.board[args.start].opposite_color

    board = _copy.deepcopy(args.board)
    board[args.start] = None

    return [end for end in args.ends if not args.calculator.is_threatened(board, [end], threat_color)]


def _get_two_moves_away(start, directions):
    double_unit = [_add_unit_direction(move, move) for move in directions]
    return [_add_unit_direction(start, move) for move in double_unit]


def _get_one_move_away(start, directions):
    ret_val = [_add_unit_direction(move, start) for move in directions]
    return ret_val


def alternates_landing_on_enemy_and_empty_space(args):
    ends = []
    board = args.board
    for direction in args.directions:
        new_start = args.start
        location = _add_unit_direction(new_start, direction)
        while location in board:
            initial_move = _add_unit_direction(direction, new_start)
            new_start = _add_unit_direction(direction, initial_move)
            if initial_move in args.ends and new_start in args.ends:
                # enemy piece at first move and no pices at second move
                if board[initial_move] and not board[new_start] and board[initial_move].color != board[args.start].color:
                    ends.append(new_start)
                else:
                    break
            else:
                break
    return ends


def cant_jump_pieces(args):
    end_locations = args.ends

    directions = [_pathfinder.get_unit_direction(args.start, end) for end in end_locations]

    for direction in directions:
        location_to_remove = args.start
        found_piece = False
        while True:
            location_to_remove = tuple(map(_operator.add, location_to_remove, direction))
            if location_to_remove not in args.board:
                break

            if not found_piece and args.board[location_to_remove]:
                found_piece = True
            elif found_piece and location_to_remove in end_locations:
                end_locations.remove(location_to_remove)
            else:
                # print("floating somehwere {}".format(location_to_remove))
                # print("had found piece: {}".format(found_piece))
                # print("in potential_end_locations: {}".format(location_to_remove in potential_end_locations))
                # print("in else: {}".format(potential_end_locations))
                pass
    return end_locations


def doesnt_land_on_own_piece(args):
    ends = []
    board = args.board
    for end in args.ends:
        if board[end] and board[args.start]:
            if board[args.start].color != board[end].color:
                ends.append(end)
        else:
            ends.append(end)
    return ends


def doesnt_land_on_piece(args):
    return [end for end in args.ends if not args.board[end]]


def ends_on_enemy(args):
    ends = []
    board = args.board
    for end in args.ends:
        if board[end] and board[args.start] and board[end].color != board[args.start].color:
            ends.append(end)
    return ends


def directional(args):
    return [end for end in args.ends if _is_directional(args.start, end, args.player_direction)]


def _is_directional(start, end, direction):
    direct = True
    direct = direct and _directional_helper(start[0], end[0], direction[0])
    direct = direct and _directional_helper(start[1], end[1], direction[1])
    return direct


def _directional_helper(start, end, direct):
    if direct > 0:
        if end < start:
            return False
    elif direct < 0:
        if end > start:
            return False
    return True
