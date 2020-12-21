import copy
from collections import defaultdict
from chess.helpers import add_unit_direction
from chess.move_pipeline import movement, pre_move_checks
from chess.move_pipeline.move_pipeline_accessor import MovePipelineAccessor
from chess.move_pipeline.data import ConditionArgs
from chess.move.pathfinder import PathFinder


class Calculator():
    ignore_when_verifying_threats = ['cant_move_onto_threatened_square', 'ends_on_enemy', 'doesnt_land_on_own_piece']
    ignore_when_finding_threats = ['cant_move_onto_threatened_square', 'ends_on_enemy', 'doesnt_land_on_own_piece', 'directional']

    # Public methods for after calling calculate all destinations
    def get_destinations(self, board, start):
        return self._calculate_destinations(board, start)

    def get_threatening_piece_location(self, board, location, threatened_by_color):
        return self._get_location_for_piece_threatening_location(board, location, threatened_by_color)

    def is_threatened(self, board, locations, threatened_by_color):
        for location in locations:
            if self._get_location_for_piece_threatening_location(board, location, threatened_by_color):
                return True
        return False

    def _get_location_for_piece_threatening_location(self, board, location, threatened_by_color):
        # concept: for each move in every piece, follow the path outward from the location we're checking for threats
        #          - ignore rules for checking is_threatened (to prevent recursion)
        #          - ignore rules for directionality (so we don't have to take player direction into account)
        threatening_locations = []
        for piece in board.pieces:
            for move in piece.moves:
                # TODO: paths is list of lists here from pathfinder, have to loop over each and see if we find piece.
                possible_threat_paths = PathFinder.get_all_paths(location, move, board)
                for path in possible_threat_paths:
                    condition_args = ConditionArgs.generate(board, move, location, path, (1, 0))

                    ends = self._reduce_paths_to_valid_end_locations(move, condition_args, ignore_conditions=self.ignore_when_finding_threats)

                    threatening_location = self._get_location_for_threatening_piece_in_path(board, piece, ends, location, threatened_by_color)
                    if threatening_location is not None and threatening_location not in threatening_locations:
                        threatening_locations.append(threatening_location)
        return threatening_locations

    def _get_location_for_threatening_piece_in_path(self, board, piece, path, location, threatened_by_color):
        for path_location in path:
            if self._location_has_enemy_piece(board, piece, path_location, threatened_by_color):
                # there is an enemy piece along path. see if it's destinations includes the location we care about
                destinations = self._calculate_destinations(board, path_location, include_threatened=False, ignore_conditions=self.ignore_when_verifying_threats)
                if location in destinations.keys():
                    return path_location
        return None

    def _location_has_enemy_piece(self, board, piece, location, threatened_by_color):
        return board[location] and \
            board[location].kind == piece.kind and \
            board[location].color == threatened_by_color

    # private methods for calculating destinations
    def _calculate_destinations(self, board, start, include_threatened=True, ignore_conditions=[]):
        piece = board[start]

        player_direction = self._get_player_direction(board.players, piece.color)

        all_end_points = {}

        for move in piece.moves:
            # Pre Move Checks
            if not self._do_prechecks_pass(board, start, move, include_threatened):
                # pre checks don't pass, so it's not a valid move, continue to next move
                continue

            # Directions and limitations
            paths = PathFinder.get_all_paths_flattened(start, move, board)

            condition_args = ConditionArgs.generate(board, move, start, paths, player_direction)

            ends = self._reduce_paths_to_valid_end_locations(move, condition_args, ignore_conditions=ignore_conditions)

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

        if 'pre_move_checks' in move:
            for check_definition in move['pre_move_checks']:
                enemy_color = 'black'
                if board[start].color == 'black':
                    enemy_color = 'white'

                locations = [add_unit_direction(start, relative_location) for relative_location in check_definition['locations']]

                precheck_names = check_definition['checks']
                precheck_functions = MovePipelineAccessor.get_attributes(pre_move_checks, precheck_names)

                passed = [check(board, locations, board._history, board[start].color) for check in precheck_functions]

                if 'is_not_threatened' in precheck_names and include_threatened:
                    passed.append(not self.is_threatened(board, locations, enemy_color))
                if False in passed:
                    return False
        return passed_pre_check

    # getting path and end locations
    def _reduce_paths_to_valid_end_locations(self, move, condition_args, ignore_conditions=None):
        conditions = MovePipelineAccessor.get_attributes(movement, move['conditions'], ignore_conditions)

        return PathFinder.reduce_paths_to_valid_end_locations(conditions, condition_args)
