# pylint: disable=R0201

import unittest
from chess.chess import Chess


class TestChess(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess = Chess()

    def test_init(self):
        assert isinstance(self.chess.board, dict)

    def test_convert_to_internal_notation(self):
        expected = {
            "A1": (0, 0),
            "B1": (0, 1),
            "C1": (0, 2),
            "D1": (0, 3),
            "E1": (0, 4),
            "F1": (0, 5),
            "G1": (0, 6),
            "H1": (0, 7),
            "A2": (1, 0),
            "B2": (1, 1),
            "C2": (1, 2),
            "D2": (1, 3),
            "E2": (1, 4),
            "F2": (1, 5),
            "G2": (1, 6),
            "H2": (1, 7),
        }
        for key, value in expected.items():
            assert Chess.convert_to_internal_indexes(key) == value, 'expected: {}\nactual: {}'.format(value, Chess.convert_to_internal_indexes(key))

    def test_move_pawn_forward_once(self):
        start = "A2"
        end = "A3"
        internal_start = Chess.convert_to_internal_indexes(start)
        internal_end = Chess.convert_to_internal_indexes(end)
        assert self.chess.board[internal_end] is None
        assert self.chess.board[internal_start]
        self.chess.move(start, end)
        assert self.chess.board[internal_end]

    def test_take_piece_become_piece__queen_to_pawn(self):
        queen_pawn = "D2"
        queen = "D1"
        enemy_queen_pawn = "D7"

        internal_queen_pawn = Chess.convert_to_internal_indexes(queen_pawn)
        internal_queen = Chess.convert_to_internal_indexes(queen)
        internal_enemy_queen_pawn = Chess.convert_to_internal_indexes(enemy_queen_pawn)

        self.chess.board[internal_queen].moves[0]['capture_actions'] = ['becomes_piece']
        self.chess.board[internal_queen_pawn] = None
        self.chess.move(queen, enemy_queen_pawn)

        former_queen = self.chess.board[internal_enemy_queen_pawn]
        print("former_queen")
        print(former_queen)
        assert former_queen.color == "white"
        assert former_queen.kind == "pawn"
