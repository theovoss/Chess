import unittest

from chess.board import ChessBoard
from chess.move.endgame_analyzer import EndgameAnalyzer


class TestEndgameAnalyzer(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.analyzer = EndgameAnalyzer()

    def test_get_check_path(self):
        self.chess_board[(6, 4)] = self.chess_board[(7, 3)]
        self.chess_board[(1, 4)] = None

        expected = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4)]

        actual = self.analyzer.get_check_paths(self.chess_board, 'white')

        self.assertEqual(set(expected), set(actual[0]))

    def test_get_pin_path(self):
        self.chess_board[(6, 4)] = self.chess_board[(7, 3)]
        self.chess_board[(1, 4)] = self.chess_board[(0, 2)]

        expected = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4)]

        self.assertTrue(self.analyzer.is_pinned(self.chess_board, 'white', (1, 4)))

        actual = self.analyzer.get_pinned_path(self.chess_board, 'white', (1, 4))

        self.assertEqual(set(expected), set(actual))
