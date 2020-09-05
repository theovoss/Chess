# pylint: disable=R0201

import unittest
from chess.piece.piece import Piece


class TestPiece(unittest.TestCase):

    """Chess unit test class."""

    def test_converts_shorthand_directions(self):
        moves = [
            {
                "directions": ["vertical", "horizontal"],
                "conditions": ["first_move", "distance_one"]
            },
            {
                "directions": ["diagonal"],
                "conditions": ["first_move", "distance_one"]
            }
        ]

        expected_moves = [
            {
                "directions": [[1, 0], [-1, 0], [0, 1], [0, -1]],
                "conditions": ["first_move", "distance_one"]
            },
            {
                "directions": [[-1, -1], [1, 1], [-1, 1], [1, -1]],
                "conditions": ["first_move", "distance_one"]
            }
        ]

        piece = Piece("None", "None", moves)

        self.assertEqual(piece.moves, expected_moves)

    def test_converts_shorthand_and_non_shorthand_directions(self):
        moves = [
            {
                "directions": ["vertical", "horizontal", [5, 1]],
                "conditions": ["first_move", "distance_one"]
            },
            {
                "directions": ["diagonal"],
                "conditions": ["first_move", "distance_one"]
            }
        ]

        expected_moves = [
            {
                "directions": [[1, 0], [-1, 0], [0, 1], [0, -1], [5, 1]],
                "conditions": ["first_move", "distance_one"]
            },
            {
                "directions": [[-1, -1], [1, 1], [-1, 1], [1, -1]],
                "conditions": ["first_move", "distance_one"]
            }
        ]

        piece = Piece("None", "None", moves)

        self.assertEqual(piece.moves, expected_moves)
