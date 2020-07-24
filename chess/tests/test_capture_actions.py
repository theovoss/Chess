"""Chess Board unit test module."""

import unittest
from unittest.mock import Mock
from chess.capture_actions import (replace,
                                   becomes_piece,
                                   increment_move_count,
                                   explode)
from chess.board.chess_board import ChessBoard
from chess.chess import Chess


class TestCaptureActions(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_replace_moves_piece(self):
        start = (1, 1)
        end = (1, 0)

        piece = Mock(color=1)
        self.chess_board[start] = piece
        self.chess_board[end] = None

        replace(self.chess_board, start, end)

        assert self.chess_board[start] is None
        assert self.chess_board[end] == piece

    def test_replace_moves_piece_and_captures(self):
        start = (1, 1)
        end = (1, 0)

        piece = Mock(color=1)
        self.chess_board[start] = piece
        self.chess_board[end] = Mock(color=2)

        replace(self.chess_board, start, end)

        assert self.chess_board[start] is None
        assert self.chess_board[end] == piece

    def test_becomes_piece(self):
        start = (1, 1)
        end = (1, 0)

        piece2_moves = ['d', 'e', 'f']
        piece2_kind = 'pawn'
        piece1_move_count = 5
        piece = Mock(
            color=1,
            moves=['a', 'b', 'c'],
            kind='queen',
            move_count=piece1_move_count)
        self.chess_board[start] = piece
        self.chess_board[end] = Mock(
            color=2,
            moves=piece2_moves,
            capture_actions=piece2_moves,
            kind=piece2_kind,
            move_count=0)

        becomes_piece(self.chess_board, start, end)

        new_piece = self.chess_board[end]
        assert self.chess_board[start] is None
        assert new_piece.moves == piece2_moves
        assert new_piece.capture_actions == piece2_moves
        assert new_piece.color == 1
        assert new_piece.move_count == piece1_move_count

    def test_becomes_piece_replaces__when_not_capturing(self):
        start = (1, 1)
        end = (1, 0)

        piece = Mock(
            color=1,
            moves=['a', 'b', 'c'],
            kind='queen',
            move_count=1)
        self.chess_board[start] = piece
        self.chess_board[end] = None

        becomes_piece(self.chess_board, start, end)

        new_piece = self.chess_board[end]
        assert new_piece == piece

    def test_increment_move_count(self):
        start = (1, 1)
        end = (1, 0)

        self.chess_board[end] = Mock(move_count=5)

        increment_move_count(self.chess_board, start, end)

        assert self.chess_board[end].move_count == 6

    def test_increment_move_count_when_no_piece__does_nothing(self):
        start = (1, 1)
        end = (1, 0)

        self.chess_board[end] = None

        increment_move_count(self.chess_board, start, end)

        assert self.chess_board[end] is None

    def test_explode_center_of_board(self):
        self._populate_mock_board()
        start = Chess.convert_to_internal_indexes('D5')
        end = Chess.convert_to_internal_indexes('D4')

        explode(self.chess_board, start, end)

        expected_empties = ['D3', 'D4', 'D5', 'C3', 'C4', 'C5', 'E3', 'E4', 'E5']

        self._assert_empties(expected_empties)

    def test_explode_edge_of_board(self):
        self._populate_mock_board()
        start = Chess.convert_to_internal_indexes('D2')
        end = Chess.convert_to_internal_indexes('D1')

        explode(self.chess_board, start, end)

        expected_empties = ['D1', 'D2', 'C1', 'C2', 'E1', 'E2']

        self._assert_empties(expected_empties)

    def test_explode_corner_of_board(self):
        self._populate_mock_board()
        start = Chess.convert_to_internal_indexes('A2')
        end = Chess.convert_to_internal_indexes('A1')

        explode(self.chess_board, start, end)

        expected_empties = ['A1', 'A2', 'B1', 'B2']

        self._assert_empties(expected_empties)

    def test_explode_replaces__when_not_capturing(self):
        self._populate_mock_board()

        start = Chess.convert_to_internal_indexes('A2')
        end = Chess.convert_to_internal_indexes('A3')

        self.chess_board[end] = None

        explode(self.chess_board, start, end)

        expected_empties = ['A2']

        self._assert_empties(expected_empties)

    def _populate_mock_board(self):
        for place in self.chess_board.board.keys():
            self.chess_board[place] = Mock()

    def _assert_empties(self, expected_empties):
        empties = [Chess.convert_to_internal_indexes(empty) for empty in expected_empties]
        for place in self.chess_board.board.keys():
            if place in empties:
                assert self.chess_board[place] is None, "Board location %s is not None" % str(place)
            else:
                assert self.chess_board[place] is not None, "Board location %s is None" % str(place)
