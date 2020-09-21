import unittest

from chess.move.pathfinder import PathFinder


class TestMovementHelpers(unittest.TestCase):
    def test_get_diagonal_unit_direction(self):
        unit = PathFinder.get_unit_direction((2, 2), (3, 3))
        self.assertEqual(unit, (1, 1))

        unit = PathFinder.get_unit_direction((2, 2), (3, 1))
        self.assertEqual(unit, (1, -1))

        unit = PathFinder.get_unit_direction((2, 2), (1, 3))
        self.assertEqual(unit, (-1, 1))

        unit = PathFinder.get_unit_direction((2, 2), (1, 1))
        self.assertEqual(unit, (-1, -1))

    def test_get_horizontal_and_vertical_unit_direction(self):
        unit = PathFinder.get_unit_direction((2, 2), (2, 3))
        self.assertEqual(unit, (0, 1))

        unit = PathFinder.get_unit_direction((2, 2), (2, 1))
        self.assertEqual(unit, (0, -1))

        unit = PathFinder.get_unit_direction((2, 2), (3, 2))
        self.assertEqual(unit, (1, 0))

        unit = PathFinder.get_unit_direction((2, 2), (1, 2))
        self.assertEqual(unit, (-1, 0))

    def test_get_L_unit_direction(self):
        unit = PathFinder.get_unit_direction((2, 2), (3, 4))
        self.assertEqual(unit, (1, 2))

        unit = PathFinder.get_unit_direction((2, 2), (4, 3))
        self.assertEqual(unit, (2, 1))

        unit = PathFinder.get_unit_direction((2, 2), (1, 4))
        self.assertEqual(unit, (-1, 2))

        unit = PathFinder.get_unit_direction((2, 2), (1, 0))
        self.assertEqual(unit, (-1, -2))

        unit = PathFinder.get_unit_direction((2, 2), (3, 0))
        self.assertEqual(unit, (1, -2))

        unit = PathFinder.get_unit_direction((2, 2), (0, 3))
        self.assertEqual(unit, (-2, 1))

        unit = PathFinder.get_unit_direction((2, 2), (0, 1))
        self.assertEqual(unit, (-2, -1))

        unit = PathFinder.get_unit_direction((2, 2), (4, 1))
        self.assertEqual(unit, (2, -1))
