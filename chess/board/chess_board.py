import json
from pprint import pprint

from .base import Board
from ..piece import Piece

from ..movement import get_all_potential_end_locations
from .. import movement


class ChessBoard(Board):

    def __init__(self):
        super().__init__(8, 8)
        self.json_file = "chess/chess_game.json"
        self.initialize_board()

    def __str__(self):
        """Generates a FEN representation of the board."""
        board = ""
        # FEN notation starts in the top left
        for column in range(self.columns - 1, -1, -1):
            num_missing = 0
            for row in range(0, self.rows):
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
        return board[0:-1]

    def initialize_board(self):
        json_data = self.load_json()
        json_board = json_data['board']
        for player in json_board:
            players_data = json_data['players']
            color = players_data[player]['color']
            player_pieces = json_board[player]
            for piece in player_pieces:
                name = piece
                moves = self.get_piece_moves(name, json_data)
                a_piece = Piece(name, color, moves)
                for location in player_pieces[piece]:
                    self.board[tuple(location)] = a_piece

    def get_piece_moves(self, name, json_data):
        return json_data['pieces'][name]['moves']

    def load_json(self):
        filename = self.json_file
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
            self.board[end_location] = self.board[start_location]
            self.board[start_location] = None
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
