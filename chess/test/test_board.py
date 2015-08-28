"""Chess Board unit test module."""

import unittest
from chess.board import ChessBoard

starting_fen_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class TestBoard(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    @staticmethod
    def convert_default_white_spaces_to_black(white_positions):
        return [(7 - row, column) for row, column in white_positions]

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

    def test_has_pawn_at_1_3(self):
        piece = self.chess_board.board[(1, 3)]
        assert len(piece.moves) > 0

    def test_pawn_can_move_forward(self):
        assert self.chess_board.board[(2, 3)] is None
        ends = self.chess_board.end_locations_for_piece_at_location((1, 3))
        assert ends == [(2, 3)]

    def test_initial_pawn_positions(self):
        expected_white_pawn_positions = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
        self.verify_pieces_at_locations_are_correct_piece_and_color(expected_white_pawn_positions, "pawn")

    def test_initial_knight_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 1), (0, 6)], "knight")

    def test_initial_rook_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 0), (0, 7)], "rook")

    def test_initial_bishop_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 2), (0, 5)], 'bishop')

    def test_initial_queen_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 3)], "queen")

    def test_initial_king_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 4)], "king")

    def test_starting_board_export(self):
        assert self.chess_board.generate_fen() == starting_fen_board

    def test_clear_board_removes_all_pieces(self):
        self.chess_board.clear_board()
        for location in self.chess_board.board:
            assert self.chess_board.board[location] is None

    def test_starting_board_import(self):
        self.chess_board.clear_board()
        self.chess_board.import_fen_board(starting_fen_board)

        expected_white_pawn_positions = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
        self.verify_pieces_at_locations_are_correct_piece_and_color(expected_white_pawn_positions, "pawn")
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 1), (0, 6)], "knight")
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 0), (0, 7)], "rook")
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 2), (0, 5)], 'bishop')
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 3)], "queen")
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 4)], "king")


class TestValidateKnightMoves(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move_knight(self):
        result = self.chess_board.move((0, 1), (2, 0))

        assert result is True
        assert self.chess_board.board[(2, 0)].kind == 'knight'

    def test_move_knight_on_top_of_a_pawn(self):
        result = self.chess_board.move((1, 0), (3, 1))

        assert result is False
        assert self.chess_board.board[(1, 3)].kind == 'pawn'


class TestValidatePawnMoves(unittest.TestCase):

    """Chess movement unit tests."""

    def setUp(self):
        self.chess_board = ChessBoard()
