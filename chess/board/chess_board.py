# pylint: disable=R0902
# disabling too many instance attributes for now.
# once I implement enpassant and castling,
# I shouldn't need some of the FEN attributes.
import os
import json

from .base import Board
from ..piece import Piece

from ..movement import get_all_potential_end_locations
from .. import movement

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

        script_dir = os.path.dirname(__file__)
        self.standard_chess = os.path.join(script_dir, '..', 'chess_game.json')

        if not existing_board:
            existing_board = self.load_json()

        self.initialize_board(existing_board)

        # FEN data I should take into account
        self.current_players_turn = "w"
        self.castling_opportunities = "KQkq"
        self.en_passant_target_square = "-"
        self.half_move_clock = 0
        self.full_move_number = 1

    def generate_fen(self):
        """Generates a FEN representation of the board."""
        board = ""
        # FEN notation starts in the top left
        for row in range(self.rows - 1, -1, -1):
            num_missing = 0
            for column in range(0, self.columns):
                key = (row, column)
                piece = self.board[key]

                if piece:
                    prepend = ''
                    if num_missing:
                        prepend = str(num_missing)
                    board += prepend + repr(piece)
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
        json_data = self.load_json()
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
                    for column in range(0, num_missing):
                        self.board[(row, actual_column)] = None
                        actual_column += 1
                except ValueError:
                    name = map_fen_to_piece_name[fen_row[actual_column].lower()]
                    color = "black" if fen_row[actual_column].islower() else "white"
                    moves = self.get_piece_moves(name, json_data)
                    self.board[(row, column)] = Piece(name, color, moves)
                    actual_column += 1

    def export(self):
        json_data = {}
        json_data['pieces'] = {}
        for piece in self.pieces:
            json_data['pieces'][piece.kind] = {'moves': piece.moves}

        json_data['players'] = self.players
        map_color_to_name = {}
        json_board = {}
        for player in self.players:
            map_color_to_name[self.players[player]['color']] = player
            json_board[player] = {}

        for location in self.board:
            piece = self.board[location]
            if piece:
                player = map_color_to_name[piece.color]
                if piece.kind in json_board[player]:
                    json_board[player][piece.kind].append(list(location))
                else:
                    json_board[player][piece.kind] = [list(location)]

        json_data['board'] = json_board

        json_data['end_game'] = self.end_game

        print("export data is:")
        print(json_data)
        return json_data

    def initialize_board(self, json_data):
        json_board = json_data['board']

        self.end_game = json_data['end_game']
        for player in json_board:
            players_data = json_data['players']
            color = players_data[player]['color']

            self.players[player] = players_data[player]

            player_pieces = json_board[player]
            for piece in player_pieces:
                name = piece
                moves = self.get_piece_moves(name, json_data)
                a_piece = Piece(name, color, moves)

                self.pieces.append(a_piece)

                for location in player_pieces[piece]:
                    self.board[tuple(location)] = a_piece

    def clear_board(self):
        for location in self.board:
            self.board[location] = None

    @staticmethod
    def get_piece_moves(name, json_data):
        return json_data['pieces'][name]['moves']

    def load_json(self):
        filename = self.standard_chess
        data = None
        with open(filename) as data_file:
            data = json.load(data_file)

        return data

    def end_locations_for_piece_at_location(self, start_location):
        piece = self.board[start_location]
        all_end_points = []
        for move in piece.moves:
            directions = move['directions']
            conditions = [getattr(movement, condition) for condition in move['conditions'] if hasattr(movement, condition)]
            ends = get_all_potential_end_locations(start_location, directions, self.board)
            for condition in conditions:
                print("ends before condition: {} are: {}".format(condition, ends))
                ends = condition(self.board, start_location, directions, ends)
                print("ends after condition: {} are: {}".format(condition, ends))
            all_end_points += ends
        return all_end_points

    def move(self, start_location, end_location):
        possible_moves = self.end_locations_for_piece_at_location(start_location)

        if end_location in possible_moves:
            is_capture = self.board[end_location] is not None
            self.board[end_location] = self.board[start_location]
            self.board[start_location] = None
            if self.current_players_turn == 'w':
                self.current_players_turn = 'b'
            else:
                self.full_move_number += 1
                self.current_players_turn = 'w'
            if self.board[end_location].kind != "pawn" and not is_capture:
                self.half_move_clock += 1
            else:
                self.half_move_clock = 0
            return True
        return False

    def is_valid_move(self, start_location, end_location):
        piece = self.board[start_location]
        for move in piece.get_valid_moves():
            valid_end_location = tuple(map(lambda x, y: x + y, start_location, move))

            if valid_end_location == end_location:
                return True
            valid_end_location = tuple(map(lambda x, y: x - y, start_location, move))

            if valid_end_location == end_location:
                return True

        return False

    @property
    def board(self):
        return self._board
