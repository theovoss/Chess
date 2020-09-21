import unittest

from chess.board import ChessBoard
from chess.move.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.calculator = Calculator()

    def test_is_threatened(self):
        self.assertTrue(self.calculator.is_threatened(self.chess_board, [(2, 2)], "white"))

    def test_get_threat_location(self):
        self.chess_board[(6, 4)] = self.chess_board[(7, 3)]
        self.chess_board[(1, 4)] = None

        threat_location = self.calculator.get_threatening_piece_location(self.chess_board, (0, 4), 'black')
        self.assertIsNotNone(threat_location)
        self.assertEqual(threat_location, [(6, 4)])

        threat_location = self.calculator.get_threatening_piece_location(self.chess_board, (4, 2), 'black')
        self.assertEqual(threat_location, [(6, 4)])
        threat_location = self.calculator.get_threatening_piece_location(self.chess_board, (4, 6), 'black')
        self.assertEqual(threat_location, [(6, 4)])

        self.assertEqual(self.calculator.get_threatening_piece_location(self.chess_board, (0, 0), 'black'), [])
