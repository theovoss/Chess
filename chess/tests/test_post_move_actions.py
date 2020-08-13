import unittest
from unittest.mock import Mock

from chess.board.chess_board import ChessBoard
from chess.post_move_actions import increment_move_count


class TestPostMoveActions(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_increment_move_count(self):
        end = (1, 0)

        self.chess_board[end] = Mock(move_count=5)

        increment_move_count(self.chess_board, end)

        assert self.chess_board[end].move_count == 6
