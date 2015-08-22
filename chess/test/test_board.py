"""Chess Board unit test module."""

import unittest
from chess.board import ChessBoard


class TestBoard(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_init(self):
        assert len(self.chess_board.board) == 64

    def test_has_pawn_at_3_1(self):
        piece = self.chess_board.board[(3, 1)]
        assert len(piece.moves) > 0

    def test_pawn_can_move_forward(self):
        # piece = self.chess_board.board[(3, 1)]
        ends = self.chess_board.end_locations_for_piece_at_location((3, 1))
        assert ends == [(3, 2)]


class TestValidatePawnMoves(unittest.TestCase):

    """Chess movement unit tests."""

    def setUp(self):
        self.chess_board = ChessBoard()
