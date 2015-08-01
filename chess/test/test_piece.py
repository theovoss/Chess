"""A unit test module for the piece class."""

import unittest
from chess.piece import Pawn, _pawn


class TestPiece(unittest.TestCase):

    """Test the piece class."""

    def test_pawn_init(self):
        pawn = Pawn("white")
        assert pawn.kind == _pawn
        assert pawn.color == "white"
