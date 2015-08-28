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


def distance_of_one(board, start, directions, potential_end_locations):
    return [x for x in get_one_move_away(start, directions) if x in potential_end_locations]


def get_one_move_away(start, directions):
    ret_val = [tuple(map(operator.add, move, start)) for move in directions]
    return ret_val


def cant_jump_pieces(board, start, directions, potential_end_locations):
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


def doesnt_land_on_own_piece(board, start, directions, potential_end_locations):
    ends = []
    for end in potential_end_locations:
        if board[end]:
            if board[start].color != board[end].color:
                ends.append(end)
        else:
            ends.append(end)
    return ends


def doesnt_land_on_piece(board, start, directions, potential_end_locations):
    return [end for end in potential_end_locations if not board[end]]


def ends_on_enemy(board, start, directions, potential_end_locations):
    ends = []
    for end in potential_end_locations:
        if board[end] is not None and board[end].color != board[start].color:
            ends.append(end)
    return ends
