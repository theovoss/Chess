"""Sample integration test module."""
# pylint: disable=no-self-use

import unittest

from chess.chess import Chess


class TestChess(unittest.TestCase):

    """Sample integration test class."""

    def setUp(self):
        self.chess = Chess()
