"""Chess Board unit test module."""

import unittest
from unittest.mock import Mock
from chess.move_pipeline.capture_actions import (becomes_piece,
                                                 explode,
                                                 captures_destination)
from chess.board.chess_board import ChessBoard
from chess.chess import Chess


class TestCaptureActions(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_becomes_piece(self):
        start = (1, 1)
        end = (1, 0)

        piece2_moves = ['d', 'e', 'f']
        piece2_kind = 'pawn'
        piece1_move_count = 5
        end_piece = Mock(
            color=2,
            moves=piece2_moves,
            capture_actions=piece2_moves,
            kind=piece2_kind,
            move_count=0)
        piece = Mock(
            color=1,
            moves=['a', 'b', 'c'],
            kind='queen',
            move_count=piece1_move_count)
        self.chess_board[start] = piece
        self.chess_board[end] = end_piece

        captures = becomes_piece(self.chess_board, start, end)
        self.assertEqual(captures, {end: end_piece})
        new_piece = self.chess_board[start]

        self.assertEqual(new_piece.moves, piece2_moves)
        self.assertEqual(new_piece.capture_actions, piece2_moves)
        self.assertEqual(new_piece.color, 1)
        self.assertEqual(new_piece.move_count, piece1_move_count)

    def test_explode_center_of_board(self):
        self._populate_mock_board()
        start = Chess.convert_to_internal_indexes('D5')
        end = Chess.convert_to_internal_indexes('D4')

        explode(self.chess_board, start, end)

        captures = explode(self.chess_board, start, end)

        expected_captures = ['D3', 'D4', 'D5', 'C3', 'C4', 'C5', 'E3', 'E4', 'E5']
        expected_internal_captures = [Chess.convert_to_internal_indexes(empty) for empty in expected_captures]

        self.assertEqual(set(captures.keys()), set(expected_internal_captures))

    def test_explode_edge_of_board(self):
        self._populate_mock_board()
        start = Chess.convert_to_internal_indexes('D2')
        end = Chess.convert_to_internal_indexes('D1')

        captures = explode(self.chess_board, start, end)

        expected_captures = ['D1', 'D2', 'C1', 'C2', 'E1', 'E2']
        expected_internal_captures = [Chess.convert_to_internal_indexes(empty) for empty in expected_captures]

        self.assertEqual(set(captures.keys()), set(expected_internal_captures))

    def test_explode_corner_of_board(self):
        self._populate_mock_board()
        start = Chess.convert_to_internal_indexes('A2')
        end = Chess.convert_to_internal_indexes('A1')

        captures = explode(self.chess_board, start, end)

        expected_captures = ['A1', 'A2', 'B1', 'B2']
        expected_internal_captures = [Chess.convert_to_internal_indexes(empty) for empty in expected_captures]

        self.assertEqual(set(captures.keys()), set(expected_internal_captures))

    def test_captures_destination(self):
        end = (5, 6)
        piece = Mock(name="this piece")
        self.chess_board[end] = piece
        captures = captures_destination(self.chess_board, (1, 4), end)
        self.assertEqual(captures, {end: piece})

    def _populate_mock_board(self):
        for place in self.chess_board.board.keys():
            self.chess_board[place] = Mock()
