from chess.piece import Pawn
from .base import Board


class ChessBoard(Board):

    def __init__(self):
        super().__init__(8, 8)
        self.initialize_board()

    def initialize_board(self):
        self.board[(6, 4)] = Pawn("white")

    def move(self, start_location, end_location):
        if self.is_valid_move(start_location, end_location):
            self.board[end_location] = self._board[start_location]
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
