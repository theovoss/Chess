# pylint: disable=R0902
# disabling too many instance attributes for now.
# once I implement enpassant and castling,
# I shouldn't need some of the FEN attributes.
from .base import Board
from .history import History
from . import json_helper

from ..move.calculator import Calculator
from ..move.manager import Manager
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
        self._manager = Manager()

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
        return self._manager.move(self, start, end, self._history, save)

    def promote(self, location, new_piece_name):
        self._manager.promote(self, location, new_piece_name)

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
