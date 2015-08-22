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

    def test_initial_pawn_positions(self):
        expected_pawn_positions = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        for location in expected_pawn_positions:
            assert self.chess_board.board[location].kind == "pawn"


class TestValidatePawnMoves(unittest.TestCase):

    """Chess movement unit tests."""

    def setUp(self):
        self.chess_board = ChessBoard()
