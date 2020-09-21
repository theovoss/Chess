import unittest
from unittest.mock import Mock
from chess.move_pipeline.side_effects import (
    move,
)

from chess.board.chess_board import ChessBoard


class TestPreMoveChecksAboutMovement(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move(self):
        kwargs = {
            'start': [0, 1],
            'end': [1, 1]
        }
        move(self.chess_board, (1, 1), **kwargs)
        self.assertIsNone(self.chess_board[(1, 2)])
        self.assertEqual(self.chess_board[(2, 2)].kind, 'pawn')
