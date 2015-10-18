# pylint: disable=W0613
# allow unused variables so all movement functions can have same parameter definition
import operator


def get_all_potential_end_locations(start, directions, board):
    ends = []
    for direction in directions:
        new_start = start
        location = tuple(map(operator.add, new_start, direction))
        while location in board:
            ends.append(location)
            new_start = location
            location = tuple(map(operator.add, new_start, direction))
    return ends


def distance_of_one(board, start, directions, potential_end_locations, player_direction):
    return [x for x in get_one_move_away(start, directions) if x in potential_end_locations]


def get_one_move_away(start, directions):
    ret_val = [tuple(map(operator.add, move, start)) for move in directions]
    return ret_val


def cant_jump_pieces(board, start, directions, potential_end_locations, player_directionv):
    locations_with_pieces = [location for location in potential_end_locations if location in board and board[location]]
    for location in locations_with_pieces:
        # get a direction from start
        # remove all locations beyond location
        direction = tuple(map(operator.sub, location, start))
        direction = tuple(map(operator.floordiv, direction, (max(direction), max(direction))))
        location_to_remove = location
        while True:
            location_to_remove = tuple(map(operator.add, location_to_remove, direction))
            if location_to_remove not in potential_end_locations:
                break
            else:
                potential_end_locations.remove(location_to_remove)
    return potential_end_locations


def doesnt_land_on_own_piece(board, start, directions, potential_end_locations, player_direction):
    ends = []
    for end in potential_end_locations:
        if board[end]:
            if board[start].color != board[end].color:
                ends.append(end)
        else:
            ends.append(end)
    return ends


def doesnt_land_on_piece(board, start, directions, potential_end_locations, player_direction):
    return [end for end in potential_end_locations if not board[end]]


def ends_on_enemy(board, start, directions, potential_end_locations, player_direction):
    ends = []
    for end in potential_end_locations:
        if board[end] is not None and board[end].color != board[start].color:
            ends.append(end)
    return ends


def directional(board, start, directions, potential_end_locations, player_direction):
    return [end for end in potential_end_locations if is_directional(start, end, player_direction)]


def is_directional(start, end, direction):
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
