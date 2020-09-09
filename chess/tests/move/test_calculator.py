import unittest

from chess.board import ChessBoard
from chess.move.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.calculator = Calculator()

    def test_is_threatened(self):
        self.assertTrue(self.calculator.is_threatened(self.chess_board, [(2, 2)], "white"))

