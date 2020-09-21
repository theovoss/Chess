import copy
import operator as _operator

from math import gcd

from chess.helpers import add_unit_direction


class PathFinder():
    @staticmethod
    def get_all_paths_flattened(start, move, board):
        ends = []
        for direction in move['directions']:
            new_start = start
            location = add_unit_direction(new_start, direction)
            while location in board:
                ends.append(location)
                new_start = location
                location = add_unit_direction(new_start, direction)
        return ends

    @staticmethod
    def get_all_paths(start, move, board):
        ends = []
        for direction in move['directions']:
            sub_path = []
            new_start = start
            location = add_unit_direction(new_start, direction)
            while location in board:
                sub_path.append(location)
                new_start = location
                location = add_unit_direction(new_start, direction)
            ends.append(sub_path)
        return ends

    @staticmethod
    def reduce_paths_to_valid_end_locations(conditions, condition_args):
        for condition in conditions:
            condition_args.ends = condition(condition_args)

        return condition_args.ends

    @staticmethod
    def get_unit_direction(start, end):
        direction = tuple(map(_operator.sub, end, start))
        dividor = abs(gcd(direction[0], direction[1]))
        direction = tuple(map(_operator.floordiv, direction, (dividor, dividor)))
        return direction

    @staticmethod
    def get_path_between(board, start, end):
        for move in board[start].moves:
            for path in PathFinder.get_all_paths(start, move, board):
                if end in path:
                    return path
        return None
