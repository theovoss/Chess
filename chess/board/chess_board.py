# pylint: disable=R0902
# disabling too many instance attributes for now.
# once I implement enpassant and castling,
# I shouldn't need some of the FEN attributes.
from .base import Board
from .history import History
from . import json_helper

from ..move.calculator import Calculator
from ..move_pipeline import side_effects
from ..piece import Piece


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

        self._calculator = Calculator()

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
    def get_all_piece_names(self):
        return [piece.kind for piece in self.pieces]

    # validity checks
    def is_valid_move(self, start_location, end_location):
        possible_moves = self.valid_moves(start_location).keys()
        if end_location in possible_moves:
            return True
        return False

    def valid_moves(self, start_location):
        return self._calculator.get_destinations(self, start_location)

    # actually move stuff
    def move(self, start, end, save=True):
        valid_moves = self.valid_moves(start)
        if end in valid_moves:
            # TODO: add this correct color moving check to a precondition and wrap in is_valid_move
            if self.current_players_turn == 'w':
                if self[start].color == 'black':
                    print('black trying to move, but whites turn')
                    return False
            else:
                if self[start].color == 'white':
                    print('white trying to move, but blacks turn')
                    return False

            self._toggle_current_player()
            print("is valid move")

            self._move_piece(start, end, valid_moves[end], save)
            return True
        print('is not valid move start: ' + str(start) + " end: " + str(end))
        return False

    def _move_piece(self, start, end, move, save=True):
        piece = self.board[start]

        post_actions = json_helper.get_post_move_actions(move)
        effects = json_helper.get_side_effects(move)

        # Move
        captures = self._move_and_capture(start, end, move)

        # Post Move
        for action in post_actions:
            action(self, end)

        # Side Effects
        history_side_effects = []
        for effect in effects:
            method = getattr(side_effects, effect['method'])
            if method:
                history_side_effects += method(self, start, **effect['kwargs'])

        # Save to history
        if save:
            self._history.add(History.construct_history_object(start, end, piece, captures, history_side_effects))

    def _move_and_capture(self, start, end, move):
        actions = json_helper.get_capture_actions(move)
        additional_captures = json_helper.get_additional_captures(self, start, move)
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
        effected_locations = []
        move = self._history.previous()
        if not move:
            return
        moving_piece = move['piece']
        self.board[tuple(move['start'])] = Piece(moving_piece['name'], moving_piece['color'], moving_piece['moves'])
        self.board[tuple(move['end'])] = None
        effected_locations.append(move['start'])
        effected_locations.append(move['end'])

        # TODO: refactor store an undo function in history for undoing/redoing each capture/side effect/move
        if 'captures' in move:
            for capture in move['captures']:
                self.board[tuple(capture['location'])] = Piece(capture['name'], capture['color'], capture['moves'])
                effected_locations.append(capture['location'])
        if 'side_effects' in move:
            for effect in move['side_effects']:
                if effect['method'] == 'move':
                    self.board[tuple(effect['start'])] = self.board[tuple(effect['end'])]
                    self.board[tuple(effect['end'])] = None
                    effected_locations.append(effect['start'])
                    effected_locations.append(effect['end'])
        self._toggle_current_player()
