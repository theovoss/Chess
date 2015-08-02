"""Sample integration test module."""
# pylint: disable=no-self-use

import unittest

from chess.chess import Chess
from chess.piece import _pawn
# from chess.board import initial_board


class TestChess(unittest.TestCase):

    """Sample integration test class."""

    def setUp(self):
        self.chess = Chess()

    def test_opening_move_updates_board(self):
        assert self.chess.board[(6, 4)].kind == _pawn
        self.chess.move((6, 4), (5, 4))
        assert self.chess.board[(5, 4)].kind == _pawn
        assert self.chess.board[(6, 4)] is None
