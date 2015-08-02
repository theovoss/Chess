"""Chess Board unit test module."""

import unittest
from chess.board import ChessBoard
from chess.piece import _pawn


class TestBoard(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_init(self):
        assert len(self.chess_board.board) == 64


class TestValidatePawnMoves(unittest.TestCase):

    """Chess movement unit tests."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move_pawn_forward_once(self):
        start = (6, 4)
        end = (5, 4)
        assert self.chess_board.board[start].kind == _pawn
        assert self.chess_board.board[end] is None
        is_valid_move = self.chess_board.move(start, end)
        assert is_valid_move is True
        assert self.chess_board.board[start] is None
        assert self.chess_board.board[end].kind == _pawn

    def test_can_not_move_pawn_forward_3_spaces(self):
        start = (6, 4)
        end = (3, 4)
        assert self.chess_board.board[start].kind == _pawn
        is_valid_move = self.chess_board.move(start, end)
        assert is_valid_move is False
        assert self.chess_board.board[start].kind == _pawn
        assert self.chess_board.board[end] is None

    def test_pawn_can_not_move_backwards(self):
        start = (6, 4)
        end = (7, 4)
        assert self.chess_board.board[start].kind == _pawn
        is_valid_move = self.chess_board.move(start, end)
        assert is_valid_move is False
        assert self.chess_board.board[start].kind == _pawn
        assert self.chess_board.board[end] is None
