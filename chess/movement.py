import operator

moves = [(1, 1), (1, 0), (1, -1), (-1, 1), (-1, 0), (-1, -1), (0, 1), (0, -1)]


def get_all_potential_end_locations(start, directions, board):
    ends = []
    for direction in directions:
        location = tuple(map(operator.add, start, direction))
        while location in board:
            ends.append(location)
            start = location
            location = tuple(map(operator.add, start, direction))
    return ends


def distance_of_one(board, start, potential_end_locations):
    return [x for x in get_adjacent_squares(start) if x in potential_end_locations]


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


def doesnt_land_on_own_piece(board, start, potential_end_locations):
    ends = []
    for end in potential_end_locations:
        if board[end]:
            if board[start].color != board[end].color:
                ends.append(end)
    return ends


def ends_on_enemy(board, start, potential_end_locations):
    ends = []
    for end in potential_end_locations:
        if board[end] is not None and board[end].color != board[start].color:
            print("board of end is:")
            print(board[end])
            ends.append(end)
    print("Ends on these enemies:")
    print(ends)
    return ends
