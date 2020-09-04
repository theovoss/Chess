import unittest
from unittest.mock import Mock

from chess.board.chess_board import ChessBoard
from chess.move_pipeline.post_move_actions import increment_move_count, promotable


class TestPostMoveActions(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_increment_move_count(self):
        end = (1, 0)

        self.chess_board[end] = Mock(move_count=5)

        increment_move_count(self.chess_board, end)

        assert self.chess_board[end].move_count == 6

    def test_promotable(self):
        location = (1, 1)
        self.chess_board[location] = Mock()
        promotable(self.chess_board, location)
        self.assertFalse(self.chess_board[location].promote_me_daddy)

        location = (0, 1)
        self.chess_board[location] = Mock()
        promotable(self.chess_board, location)
        self.assertTrue(self.chess_board[location].promote_me_daddy)

        location = (6, 1)
        self.chess_board[location] = Mock()
        promotable(self.chess_board, location)
        self.assertFalse(self.chess_board[location].promote_me_daddy)

        location = (7, 1)
        self.chess_board[location] = Mock()
        promotable(self.chess_board, location)
        self.assertTrue(self.chess_board[location].promote_me_daddy)
