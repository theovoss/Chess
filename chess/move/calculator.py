import copy
from collections import defaultdict
from chess.helpers import add_unit_direction
from chess.move_pipeline import movement, pre_move_checks


class Calculator():
    # Public methods for after calling calculate all destinations
    def get_destinations(self, board, start):
        return self._calculate_destinations(board, start)

    def is_threatened(self, board, locations, threatened_by_color):
        print("Is threatened color is: " + threatened_by_color)
        for location in locations:
            if self._location_is_threatened(board, location, threatened_by_color):
                return True
        return False

    def _location_is_threatened(self, board, location, threatened_by_color):
        for piece in board.pieces:
            paths = []
            for move in piece.moves:
                paths += self._get_all_paths(location, move, board)
            if self._path_has_specific_enemy_piece_targeting_location(board, piece, paths, location, threatened_by_color):
                return True
        return False

    def _path_has_specific_enemy_piece_targeting_location(self, board, piece, path, location, threatened_by_color):
        for path_location in path:
            if self._location_has_enemy_piece(board, piece, path_location, threatened_by_color):
                # there is an enemy piece along path. see if it's destinations includes the location we care about
                destinations = self._calculate_destinations(board, path_location, include_threatened=False)
                if location in destinations.keys():
                    print("Piece {} at location {} is threatening".format(piece.kind, path_location))
                    return True
        return False

    def _location_has_enemy_piece(self, board, piece, location, threatened_by_color):
        return board[location] and \
                board[location].kind == piece.kind and \
                board[location].color == threatened_by_color

    # private methods for calculating destinations
    def _calculate_destinations(self, board, start, include_threatened=True):
        piece = board[start]

        player_direction = self._get_player_direction(board.players, piece.color)

        # handle mocked pieces that aren't needed for moving
        all_end_points = {}

        for move in piece.moves:
            # Pre Move Checks
            if not self._do_prechecks_pass(board, start, move, include_threatened):
                # pre checks don't pass, so it's not a valid move, continue to next move
                continue

            # Directions and limitations
            paths = self._get_all_paths(start, move, board)
            ends = self._reduce_paths_to_valid_end_locations(board, move, start, player_direction, paths)

            for end in ends:
                all_end_points[end] = move

        return all_end_points

    def _get_player_direction(self, players, color):
        for player in players:
            if color == players[player]['color']:
                player_direction = players[player]['direction']
                return player_direction
        return None

    def _do_prechecks_pass(self, board, start, move, include_threatened):
        passed_pre_check = True

        if 'pre_move_checks' in move and include_threatened:
            for check_definition in move['pre_move_checks']:
                enemy_color = 'black'
                if board[start].color == 'black':
                    enemy_color = 'white'

                locations = [add_unit_direction(start, relative_location) for relative_location in check_definition['locations']]

                checks = check_definition['checks']
                passed = [getattr(pre_move_checks, check)(board, locations, board._history, board[start].color) for check in checks if hasattr(pre_move_checks, check)]
                if 'is_not_threatened' in checks:
                    passed.append(not self.is_threatened(board, locations, enemy_color))
                if False in passed:
                    passed_pre_check = False
        return passed_pre_check

    # getting path and end locations
    def _get_all_paths(self, start, move, board):
        ends = []
        for direction in move['directions']:
            new_start = start
            location = add_unit_direction(new_start, direction)
            while location in board:
                ends.append(location)
                new_start = location
                location = add_unit_direction(new_start, direction)
        return ends

    def _reduce_paths_to_valid_end_locations(self, board, move, start, player_direction, paths):
        ends = copy.deepcopy(paths)
        directions = move['directions']
        conditions = [getattr(movement, condition) for condition in move['conditions'] if hasattr(movement, condition)]

        for condition in conditions:
            ends = condition(board, start, directions, ends, player_direction)

        return ends
