import unittest

from chess.board import ChessBoard
from chess.move.endgame_analyzer import EndgameAnalyzer


class TestEndgameAnalyzer(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()
        self.analyzer = EndgameAnalyzer()

    def test_is_check_when_no_endgame_data(self):
        self.chess_board.end_game.pop('piece')

        # no check
        self.assertFalse(self.analyzer.is_check(self.chess_board, 'white'))

        # would be in check, but no endgame data
        self.chess_board[(6, 4)] = self.chess_board[(7, 3)]
        self.chess_board[(1, 4)] = None

        self.assertFalse(self.analyzer.is_check(self.chess_board, 'white'))

    def test_is_pinned_when_no_endgame_data(self):
        # {'draw': {'conditions': ['no_piece_of_current_player_can_move']},
        # 'lose': {'conditions': ['king_cant_move', 'enemy_can_take_king', 'own_piece_cant_block_enemy_piece']}}
        self.chess_board.end_game = {}

        # no check
        self.assertFalse(self.analyzer.is_pinned(self.chess_board, 'white', (1, 4)))

        # would be in pinned, but no endgame data
        self.chess_board[(6, 4)] = self.chess_board[(7, 3)]

        self.assertFalse(self.analyzer.is_pinned(self.chess_board, 'white', (1, 4)))

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
