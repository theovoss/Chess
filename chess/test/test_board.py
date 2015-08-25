"""Chess Board unit test module."""

import unittest
from chess.board import ChessBoard


class TestBoard(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def convert_default_white_spaces_to_black(self, white_positions):
        return [(x, 7 - y) for x, y in white_positions]

    def test_init(self):
        assert len(self.chess_board.board) == 64

    def test_has_pawn_at_3_1(self):
        piece = self.chess_board.board[(3, 1)]
        assert len(piece.moves) > 0

    def test_pawn_can_move_forward(self):
        assert self.chess_board.board[(3, 2)] is None
        ends = self.chess_board.end_locations_for_piece_at_location((3, 1))
        assert ends == [(3, 2)]

    def test_initial_pawn_positions(self):
        expected_white_pawn_positions = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        piece = "pawn"
        for location in expected_white_pawn_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "white"

        expected_black_pawn_positions = self.convert_default_white_spaces_to_black(expected_white_pawn_positions)
        for location in expected_black_pawn_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "black"

    def test_initial_knight_positions(self):
        expected_knight_positions = [(1, 0), (6, 0)]
        piece = "knight"
        for location in expected_knight_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "white"

        expected_black_knight_positions = self.convert_default_white_spaces_to_black(expected_knight_positions)
        for location in expected_black_knight_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "black"

    def test_initial_rook_positions(self):
        expected_rook_positions = [(0, 0), (7, 0)]
        piece = "rook"
        for location in expected_rook_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "white"

        expected_black_rook_positions = self.convert_default_white_spaces_to_black(expected_rook_positions)
        for location in expected_black_rook_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "black"

    def test_initial_bishop_positions(self):
        expected_bishop_positions = [(2, 0), (5, 0)]
        for location in expected_bishop_positions:
            assert self.chess_board.board[location].kind == "bishop"

    def test_initial_queen_positions(self):
        expected_queen_positions = [(3, 0)]
        for location in expected_queen_positions:
            assert self.chess_board.board[location].kind == "queen"

    def test_initial_king_positions(self):
        expected_king_positions = [(4, 0)]
        for location in expected_king_positions:
            assert self.chess_board.board[location].kind == "king"


class TestValidateKnightMoves(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move_knight(self):
        result = self.chess_board.move((1, 0), (0, 2))

        assert result is True
        assert self.chess_board.board[(0, 2)].kind == 'knight'

    def test_move_knight_on_top_of_a_pawn(self):
        result = self.chess_board.move((1, 0), (3, 1))

        assert result is False
        assert self.chess_board.board[(3, 1)].kind == 'pawn'


class TestValidatePawnMoves(unittest.TestCase):

    """Chess movement unit tests."""

    def setUp(self):
        self.chess_board = ChessBoard()
