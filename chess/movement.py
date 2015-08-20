import operator

moves = [(1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]


def get_all_potential_end_locations(start, directions, board):
    return [location for direction in directions for location in tuple(map(operator.add, start, direction)) if location in board]


def distance_of_one(start, potential_end_locations=None):
    if potential_end_locations:
        return [x for x in get_adjacent_squares(start) if x in potential_end_locations]
    else:
        return get_adjacent_squares(start)


def get_adjacent_squares(start):
    ret_val = [tuple(map(operator.add, move, start)) for move in moves]
    return ret_val


def cant_jump_pieces(board, start, potential_end_locations):
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
                # if not potential_end_locations:
                #     break
    return potential_end_locations


# Boolean methods for final verification
def doesnt_land_on_own_piece(board, end_square, start_square):  # make this return potential end locations
    if board[end_square] and board[start_square]:
        return board[end_square].owner != board[start_square].owner
    else:
        return True
