# pylint: disable=R0902
# disabling too many instance attributes for now.
# once I implement enpassant and castling,
# I shouldn't need some of the FEN attributes.
from .base import Board
from .history import History
from . import json_helper

from .. import movement
from ..piece import Piece

from ..movement import get_all_potential_end_locations


map_fen_to_piece_name = {
    'k': "king",
    'q': "queen",
    'n': "knight",
    'b': "bishop",
    'r': "rook",
    'p': "pawn"
}


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

        # FEN data I should take into account
        self.castling_opportunities = "KQkq"
        self.en_passant_target_square = "-"
        self.half_move_clock = 0
        self.full_move_number = 1

    def generate_fen(self):
        """Generate a FEN representation of the board."""
        board = ""
        # FEN notation starts in the top left
        for row in range(self.rows - 1, -1, -1):
            num_missing = 0
            for column in range(0, self.columns):
                key = (row, column)
                piece = self[key]

                if piece:
                    prepend = ''
                    if num_missing:
                        prepend = str(num_missing)
                    board += prepend + repr(piece)
                    num_missing = 0
                else:
                    num_missing += 1
            if num_missing:
                board += str(num_missing)
            board += "/"

        other_info = " {cpt} {co} {epts} {hmc} {fmn}".format(cpt=self.current_players_turn,
                                                             co=self.castling_opportunities,
                                                             epts=self.en_passant_target_square,
                                                             hmc=self.half_move_clock,
                                                             fmn=self.full_move_number)
        fen = board[0:-1] + other_info
        return fen

    def import_fen_board(self, fen_board):
        json_data = json_helper.load_json()
        board_data, self.current_players_turn, self.castling_opportunities,\
            self.en_passant_target_square, self.half_move_clock,\
            self.full_move_number = fen_board.split(' ')
        rows = board_data.split('/')
        for row in range(self.rows - 1, -1, -1):
            fen_row = rows[7 - row]
            actual_column = 0
            for column in range(0, len(fen_row)):
                try:
                    num_missing = int(fen_row[actual_column])
                    for _ in range(0, num_missing):
                        self[(row, actual_column)] = None
                        actual_column += 1
                except ValueError:
                    name = map_fen_to_piece_name[fen_row[actual_column].lower()]
                    color = "black" if fen_row[actual_column].islower() else "white"
                    moves = json_helper.get_piece_moves(name, json_data)
                    self[(row, column)] = Piece(name, color, moves)
                    actual_column += 1

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
                    json_board[player][piece.kind].append({"position": list(location), "move_count": piece.move_count})
                else:
                    json_board[player][piece.kind] = [{"position": list(location), "move_count": piece.move_count}]

        json_data['board'] = json_board

        json_data['end_game'] = self.end_game

        json_data['history'] = self._history.json

        return json_data

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
                    self[tuple(location)] = a_piece

        if json_data['players']['current'] == "Player 1":
            self.current_players_turn = 'w'
        else:
            self.current_players_turn = 'b'

    def all_end_locations_for_color(self, color):
        ends = []
        for location, piece in self._board.items():
            if piece and piece.color == color:
                ends += self.end_locations_for_piece_at_location(location)
        return ends

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
            directions = move['directions']
            conditions = [getattr(movement, condition) for condition in move['conditions'] if hasattr(movement, condition)]
            ends = get_all_potential_end_locations(start_location, directions, self)
            for condition in conditions:
                print("ends before condition: {} are: {}".format(condition, ends))
                ends = condition(self, start_location, directions, ends, player_direction)
                print("ends after condition: {} are: {}".format(condition, ends))
            all_end_points += ends
        return all_end_points

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
        if 'captures' in move:
            for capture in move['captures']:
                self.board[tuple(capture['location'])] = Piece(capture['name'], capture['color'], capture['moves'])

        self._toggle_current_player()

    def _toggle_current_player(self):
        if self.current_players_turn == 'w':
            self.current_players_turn = 'b'
        else:
            self.current_players_turn = 'w'

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
                self.full_move_number += 1

            self._toggle_current_player()
            print("is valid move")
            is_capture = self[end_location] is not None

            self._move_piece(start_location, end_location, is_capture, save)

            if self[end_location].kind != "pawn" and not is_capture:
                self.half_move_clock += 1
            else:
                self.half_move_clock = 0
            return True
        print('is not valid move start: ' + str(start_location) + " end: " + str(end_location))
        return False

    def _move_piece(self, start_location, end_location, is_capture, save=True):
        piece = self.board[start_location]

        actions = json_helper.get_capture_actions(piece, start_location, end_location)
        post_actions = json_helper.get_post_move_actions(piece, start_location, end_location)

        captures = []
        if is_capture:
            for action in actions:
                captureds = action(self.board, start_location, end_location)
                captures += History.construct_capture_obj(captureds)

            for capture in captures:
                capture_location = capture['location']
                self.board[capture_location] = None

        self.board[end_location] = self.board[start_location]
        self.board[start_location] = None

        print("end location: {}, start location: {}".format(end_location, start_location))
        for action in post_actions:
            action(self.board, end_location)

        if save:
            self._history.add(History.construct_history_object(start_location, end_location, piece, captures))

    def is_valid_move(self, start_location, end_location):
        possible_moves = self.valid_moves(start_location)
        if end_location in possible_moves:
            return True
        return False

    def valid_moves(self, start_location):
        return self.end_locations_for_piece_at_location(start_location)
