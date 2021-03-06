# pylint: disable=R0201

import unittest
from chess.piece.directions import convert_shorthand_directions


class TestDirections(unittest.TestCase):

    """Chess unit test class."""

    def test_converts_shorthand_directions(self):
        expected = [[1, 0], [-1, 0]]
        actual = convert_shorthand_directions("vertical")

        self.assertEqual(expected, actual)

    def test_doesnt_convert_non_shorthand_directions(self):
        actual = convert_shorthand_directions("hello")

        self.assertEqual(["hello"], actual)
