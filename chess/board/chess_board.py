# pylint: disable=R0902
# disabling too many instance attributes for now.
# once I implement enpassant and castling,
# I shouldn't need some of the FEN attributes.
from .base import Board
from .history import History
from . import json_helper

from ..move.calculator import Calculator
from ..move.manager import Manager
from ..move.endgame_analyzer import EndgameAnalyzer
from ..piece import Piece


class ChessBoard(Board):
    def __init__(self, existing_board=None):
        super().__init__(8, 8)
        self.pieces = []
        self.players = {}

        if not existing_board:
            existing_board = json_helper.load_json()

        existing_history = {'initial_board': existing_board}
        if 'history' in existing_board:
            existing_history = existing_board.get('history')

        self.end_game = existing_board['end_game']

        self._history = History(existing_history)

        self.initialize_board(existing_board)

        self.current_players_turn = "white"
        if existing_board['players']['current'] == "Player 2":
            self._toggle_current_player()

        self._calculator = Calculator()
        self._manager = Manager()
        self._endgame_analyzer = EndgameAnalyzer()

    def _toggle_current_player(self):
        if self.current_players_turn == 'white':
            self.current_players_turn = 'black'
        else:
            self.current_players_turn = 'white'

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

    def export(self):
        json_data = {}
        json_data['pieces'] = {}
        for piece in self.pieces:
            json_data['pieces'][piece.kind] = {'moves': piece.moves}

        json_data['players'] = self.players
        if self.current_players_turn == 'white':
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

    def get_endgame_piece_name(self):
        return self.end_game.get('piece')

    def get_endgame_piece_location(self, color):
        piece_name = self.get_endgame_piece_name()
        for location in self:
            if self[location] and self[location].color == color and self[location].kind == piece_name:
                return location
        return None

    def get_location_for_piece(self, name, color):
        pieces = self.get_pieces_for_color(color)
        return pieces[name]

    def get_pieces_for_color(self, color):
        for player in self.players:
            if self.players[player]['color'] == color:
                return self.players[player]
        return None

    # validity checks
    def is_valid_move(self, start_location, end_location):
        possible_moves = self.valid_moves(start_location)
        if end_location in possible_moves:
            return True
        return False

    def valid_moves(self, start):
        valid_moves = self._calculator.get_destinations(self, start)

        if self._endgame_analyzer.is_check(self, self.current_players_turn):
            check_path = self.get_check_path()
            if not check_path:
                # if there isn't a path for check ie: multiple paths to check, then remove all valid moves
                valid_moves = {}
            else:
                for move in list(valid_moves.keys()):
                    if move not in check_path:
                        valid_moves.pop(move)

        if self._endgame_analyzer.is_pinned(self, self.current_players_turn, start):
            pinned_path = self._endgame_analyzer.get_pinned_path(self, self.current_players_turn, start)
            for move in list(valid_moves.keys()):
                if move not in pinned_path:
                    valid_moves.pop(move)
        return valid_moves

    def is_check(self):
        return self._endgame_analyzer.is_check(self, self.current_players_turn)

    def get_check_path(self):
        paths = self._endgame_analyzer.get_check_paths(self, self.current_players_turn)
        return paths[0] if len(paths) == 1 else []

    # actually move stuff
    def move(self, start, end, save=True):
        success = self._manager.move(self, start, end, self._history, save)
        # self._endgame_analyzer.check_endgame_conditions()
        # if self._endgame_analyzer.is_check(self, self.current_players_turn):
        #     pass
        return success

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
