"""Chess unit test module."""

import unittest
from chess.chess import Chess


class TestChess(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess = Chess()

    def test_init(self):
        assert type(self.chess.board) == dict

    def test_move_pawn_forward_once(self):
        start = (6, 4)
        end = (5, 4)
        # assert self.chess.board[start]
        # self.chess.move(start, end)
        # assert self.chess.board[end]
