# pylint: disable=R0902
# disabling too many instance attributes for now.
# once I implement enpassant and castling,
# I shouldn't need some of the FEN attributes.
from .base import Board
from .history import History
from . import json_helper

from ..move_pipeline import movement, pre_move_checks, side_effects
from ..piece import Piece
from ..helpers import add_unit_direction

from ..move_pipeline.movement import get_all_potential_end_locations


class ChessBoard(Board):

    def __init__(self, existing_board=None):
        super().__init__(8, 8)
        self.pieces = []
        self.players = {}
        self.end_game = {}

        if not existing_board:
            existing_board = json_helper.load_json()

        existing_history = {'initial_board': existing_board}
        if 'history' in existing_board:
            existing_history = existing_board.get('history')

        self._history = History(existing_history)

        self.initialize_board(existing_board)
        if existing_board and existing_board['players']['current'] == "Player 1":
            self.current_players_turn = "w"
        else:
            self.current_players_turn = "b"

    def _toggle_current_player(self):
        if self.current_players_turn == 'w':
            self.current_players_turn = 'b'
        else:
            self.current_players_turn = 'w'

    def initialize_board(self, json_data):
        json_board = json_data['board']

        for piece in json_data['pieces']:
            name = piece
            moves = json_helper.get_piece_moves(name, json_data)

            self.pieces.append(Piece(name, "white", moves))

        self.end_game = json_data['end_game']
        for player in ['Player 1', 'Player 2']:
            players_data = json_data['players']
            color = players_data[player]['color']

            self.players[player] = players_data[player]

            player_pieces = json_board[player]
            for piece in player_pieces:
                name = piece
                moves = json_helper.get_piece_moves(name, json_data)

                for position_moves_dict in player_pieces[piece]:
                    a_piece = Piece(name, color, moves)
                    location = position_moves_dict['position']
                    a_piece.move_count = position_moves_dict['move_count']
                    a_piece.promote_me_daddy = position_moves_dict.get('promote_me_daddy', False)
                    self[tuple(location)] = a_piece

        if json_data['players']['current'] == "Player 1":
            self.current_players_turn = 'w'
        else:
            self.current_players_turn = 'b'

    def export(self):
        json_data = {}
        json_data['pieces'] = {}
        for piece in self.pieces:
            json_data['pieces'][piece.kind] = {'moves': piece.moves}

        json_data['players'] = self.players
        if self.current_players_turn == 'w':
            json_data['players']['current'] = "Player 1"
        else:
            json_data['players']['current'] = "Player 2"

        map_color_to_name = {}
        json_board = {}
        for player in self.players:
            if player != 'current':
                map_color_to_name[self.players[player]['color']] = player
                json_board[player] = {}

        for location in self:
            piece = self[location]
            if piece:
                player = map_color_to_name[piece.color]
                if piece.kind in json_board[player]:
                    json_board[player][piece.kind].append({"position": list(location), "move_count": piece.move_count, "promote_me_daddy": piece.promote_me_daddy})
                else:
                    json_board[player][piece.kind] = [{"position": list(location), "move_count": piece.move_count, "promote_me_daddy": piece.promote_me_daddy}]

        json_data['board'] = json_board

        json_data['end_game'] = self.end_game

        json_data['history'] = self._history.json

        return json_data

    # Calculate Destinations, don't actually move
    def end_locations_for_piece_at_location(self, start_location):
        piece = self[start_location]
        if not piece:
            return []
        player_direction = None
        for player in self.players:
            if piece.color == self.players[player]['color']:
                player_direction = self.players[player]['direction']
                break

        all_end_points = []
        for move in piece.moves:
            # Pre Move Checks
            if not self._do_prechecks_pass(start_location, move):
                # pre checks don't pass, so it's not a valid move, continue to next move
                continue

            # Directions and limitations
            ends = self._get_end_locations_for_move(move, start_location, player_direction)

            all_end_points += ends
        return all_end_points

    def _get_end_locations_for_move(self, move, start, player_direction):
        directions = move['directions']
        conditions = [getattr(movement, condition) for condition in move['conditions'] if hasattr(movement, condition)]

        ends = get_all_potential_end_locations(start, directions, self)
        for condition in conditions:
            print("ends before condition: {} are: {}".format(condition, ends))
            ends = condition(self, start, directions, ends, player_direction)
            print("ends after condition: {} are: {}".format(condition, ends))

        return ends

    def _do_prechecks_pass(self, start, move):
        passed_pre_check = True
        if 'pre_move_checks' in move:
            for check_definition in move['pre_move_checks']:
                locations = [add_unit_direction(start, relative_location) for relative_location in check_definition['locations']]

                checks = check_definition['checks']
                passed = [getattr(pre_move_checks, check)(self, locations, self._history) for check in checks if hasattr(pre_move_checks, check)]
                if False in passed:
                    passed_pre_check = False
        return passed_pre_check

    def all_end_locations_for_color(self, color):
        ends = []
        for location, piece in self._board.items():
            if piece and piece.color == color:
                ends += self.end_locations_for_piece_at_location(location)
        return ends

    def get_all_piece_names(self):
        return [piece.kind for piece in self.pieces]

    # validity checks
    def is_valid_move(self, start_location, end_location):
        possible_moves = self.valid_moves(start_location)
        if end_location in possible_moves:
            return True
        return False

    def valid_moves(self, start_location):
        return self.end_locations_for_piece_at_location(start_location)

    # actually move stuff
    def move(self, start_location, end_location, save=True):
        if self.is_valid_move(start_location, end_location):
            # TODO: add this correct color moving check to a precondition and wrap in is_valid_move
            if self.current_players_turn == 'w':
                if self[start_location].color == 'black':
                    print('black trying to move, but whites turn')
                    return False
            else:
                if self[start_location].color == 'white':
                    print('white trying to move, but blacks turn')
                    return False

            self._toggle_current_player()
            print("is valid move")

            self._move_piece(start_location, end_location, save)

            return True
        print('is not valid move start: ' + str(start_location) + " end: " + str(end_location))
        return False

    def _move_piece(self, start_location, end_location, save=True):
        piece = self.board[start_location]

        post_actions = json_helper.get_post_move_actions(self, piece, start_location, end_location)
        effects = json_helper.get_side_effects(self, piece, start_location, end_location)

        # Move
        captures = self._move_and_capture(piece, start_location, end_location)

        # Post Move
        for action in post_actions:
            action(self, end_location)

        # Side Effects
        history_side_effects = []
        for effect in effects:
            method = getattr(side_effects, effect['method'])
            if method:
                history_side_effects += method(self, start_location, **effect['kwargs'])

        # Save to history
        if save:
            self._history.add(History.construct_history_object(start_location, end_location, piece, captures, history_side_effects))

    def _move_and_capture(self, piece, start, end):
        actions = json_helper.get_capture_actions(self, piece, start, end)
        additional_captures = json_helper.get_additional_captures(self, piece, start, end)
        captures = []
        if self[end] is not None:
            # capturing piece!
            for action in actions:
                captureds = action(self, start, end)
                captures += History.construct_capture_obj(captureds)

        if additional_captures:
            captures += History.construct_capture_obj(additional_captures)

        for capture in captures:
            capture_location = capture['location']
            self.board[capture_location] = None

        self.board[end] = self.board[start]
        self.board[start] = None

        return captures

    def promote(self, location, new_piece_name):
        if self[location].promote_me_daddy:
            color = self[location].color
            promoted = [piece for piece in self.pieces if piece.kind == new_piece_name][0]
            promoted.color = color

            self[location] = promoted

    # History related methods
    def get_history(self):
        return self._history.all()

    def first(self):
        self.clear_board()
        self.initialize_board(self._history.initial_board)
        self._history.first()

    def next(self):
        move = self._history.next()
        if move:
            self.move(tuple(move['start']), tuple(move['end']), save=False)

    def previous(self):
        move = self._history.previous()
        if not move:
            return
        moving_piece = move['piece']
        self.board[tuple(move['start'])] = Piece(moving_piece['name'], moving_piece['color'], moving_piece['moves'])
        self.board[tuple(move['end'])] = None

        # TODO: refactor store an undo function in history for undoing/redoing each capture/side effect/move
        if 'captures' in move:
            for capture in move['captures']:
                self.board[tuple(capture['location'])] = Piece(capture['name'], capture['color'], capture['moves'])
        if 'side_effects' in move:
            print("Move side effects")
            print(move['side_effects'])
            for effect in move['side_effects']:
                if effect['method'] == 'move':
                    self.board[tuple(effect['start'])] = self.board[tuple(effect['end'])]
                    self.board[tuple(effect['end'])] = None
        self._toggle_current_player()
