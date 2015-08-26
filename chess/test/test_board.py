"""Chess Board unit test module."""

import unittest
from chess.board import ChessBoard


class TestBoard(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def convert_default_white_spaces_to_black(self, white_positions):
        return [(x, 7 - y) for x, y in white_positions]

    def verify_pieces_at_locations_are_correct_piece_and_color(self, white_positions, piece):
        for location in white_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "white"

        black_positions = self.convert_default_white_spaces_to_black(white_positions)
        for location in black_positions:
            assert self.chess_board.board[location].kind == piece
            assert self.chess_board.board[location].color == "black"

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
        self.verify_pieces_at_locations_are_correct_piece_and_color(expected_white_pawn_positions, "pawn")

    def test_initial_knight_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(1, 0), (6, 0)], "knight")

    def test_initial_rook_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 0), (7, 0)], "rook")

    def test_initial_bishop_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(2, 0), (5, 0)], 'bishop')

    def test_initial_queen_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(3, 0)], "queen")

    def test_initial_king_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(4, 0)], "king")


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
