"""A unit test module for the piece class."""

import unittest
from chess.piece import Pawn, Knight, Rook, Bishop, Queen, King
from chess.piece import _pawn, _knight, _rook, _bishop, _queen, _king


class TestPiece(unittest.TestCase):

    """Test the piece class."""

    def test_pawn_str(self):
        pawn = Pawn("white")
        assert str(pawn) == "white pawn"

    def test_pawn_init(self):
        pawn = Pawn("white")
        assert pawn.kind == _pawn
        assert pawn.color == "white"

    def test_knight_init(self):
        pawn = Knight("white")
        assert pawn.kind == _knight
        assert pawn.color == "white"

    def test_rook_init(self):
        rook = Rook("white")
        assert rook.kind == _rook
        assert rook.color == "white"

    def test_bishop_init(self):
        bishop = Bishop("white")
        assert bishop.kind == _bishop
        assert bishop.color == "white"

    def test_queen_init(self):
        queen = Queen("white")
        assert queen.kind == _queen
        assert queen.color == "white"

    def test_king_init(self):
        king = King("white")
        assert king.kind == _king
        assert king.color == "white"


class TestPawnMovement(unittest.TestCase):

    def setUp(self):
        self.pawn = Pawn("white")

    def test_pawn_is_limited_to_a_vertical_row(self):
        move_forward_once = (1, 0)
        assert self.pawn.get_valid_moves() == [move_forward_once]

    def test_pawn_can_attack_diagonally(self):
        attack_diagonal = (1, 1)
        assert self.pawn.get_attack_moves() == [attack_diagonal]
