# pylint: disable=W0613
# allow unused variables so all movement functions can have same parameter definition
import operator as _operator


def get_all_potential_end_locations(start, directions, board, targetted_locations=[]):
    ends = []
    for direction in directions:
        new_start = start
        location = tuple(map(_operator.add, new_start, direction))
        while location in board:
            ends.append(location)
            new_start = location
            location = tuple(map(_operator.add, new_start, direction))
    return ends


def distance_of_two(board, start, directions, potential_end_locations, player_direction):
    return [x for x in _get_two_moves_away(start, directions) if x in potential_end_locations]


def distance_of_one(board, start, directions, potential_end_locations, player_direction):
    return [x for x in _get_one_move_away(start, directions) if x in potential_end_locations]


def cant_move_onto_threatened_square(board, start, directions, potential_end_locations, player_direction):
    pass


def _get_two_moves_away(start, directions):
    double_unit = [tuple(map(_operator.add, move, move)) for move in directions]
    return [tuple(map(_operator.add, start, move)) for move in double_unit]


def _get_one_move_away(start, directions):
    ret_val = [tuple(map(_operator.add, move, start)) for move in directions]
    return ret_val


def alternates_landing_on_enemy_and_empty_space(board, start, directions, potential_end_locations, player_direction):
    ends = []
    for direction in directions:
        new_start = start
        location = tuple(map(_operator.add, new_start, direction))
        while location in board:
            initial_move = tuple(map(_operator.add, direction, new_start))
            new_start = tuple(map(_operator.add, direction, initial_move))
            if initial_move in potential_end_locations and new_start in potential_end_locations:
                # enemy piece at first move and no pices at second move
                if board[initial_move] and not board[new_start] and board[initial_move].color != board[start].color:
                    ends.append(new_start)
                else:
                    break
            else:
                break
    return ends


def cant_jump_pieces(board, start, directions, potential_end_locations, player_direction):
    end_locations = potential_end_locations
    for location in potential_end_locations:
        # get a direction from start
        # remove all locations beyond location
        direction = tuple(map(_operator.sub, location, start))
        dividor = max(map(abs, direction))
        direction = tuple(map(_operator.floordiv, direction, (dividor, dividor)))
        location_to_remove = start
        found_piece = False
        while True:
            location_to_remove = tuple(map(_operator.add, location_to_remove, direction))
            if not found_piece and board[location_to_remove]:
                found_piece = True
            elif location_to_remove in end_locations and found_piece:
                end_locations.remove(location_to_remove)
            elif location_to_remove not in board:
                print("{} not in board".format(location_to_remove))
                break
            else:
                # print("floating somehwere {}".format(location_to_remove))
                # print("had found piece: {}".format(found_piece))
                # print("in potential_end_locations: {}".format(location_to_remove in potential_end_locations))
                # print("in else: {}".format(potential_end_locations))
                pass
    return end_locations


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
    return [end for end in potential_end_locations if _is_directional(start, end, player_direction)]


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


def first_move(board, start, directions, potential_end_locations, player_direction):
    return potential_end_locations if board[start].move_count == 0 else []
