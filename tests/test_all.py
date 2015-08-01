"""Sample integration test module."""
# pylint: disable=no-self-use

import unittest

from chess import chess
from chess.piece import _pawn
from chess.board import initial_board


class TestChess(unittest.TestCase):

    """Sample integration test class."""

    def test_set_board_sets_the_initial_board(self):
        chess.set_board()
        assert chess.get_board() == initial_board

    def test_opening_move_updates_board(self):
        chess.set_board()
        assert chess.board["d2"].kind == _pawn
        chess.move("d2", "d3")
        assert chess.board["d3"].kind == _pawn
