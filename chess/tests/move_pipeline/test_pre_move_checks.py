import unittest
from unittest.mock import Mock
from chess.move_pipeline.pre_move_checks import (
    has_not_moved,
    has_moved_once,
    is_empty,
    is_not_empty,
    moved_last,
    is_not_threatened,
)
from chess.board.chess_board import ChessBoard
from chess.board.history import History


class TestPreMoveChecksAboutMovement(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_has_not_moved(self):
        start = (3, 1)
        self.chess_board[start] = Mock(move_count=0)

        self.assertTrue(has_not_moved(self.chess_board, [start], Mock()))
        self.assertFalse(has_moved_once(self.chess_board, [start], Mock()))

    def test_moved_once(self):
        start = (3, 1)
        self.chess_board[start] = Mock(move_count=1)

        self.assertFalse(has_not_moved(self.chess_board, [start], Mock()))
        self.assertTrue(has_moved_once(self.chess_board, [start], Mock()))

    def test_moved_twice(self):
        start = (3, 1)
        self.chess_board[start] = Mock(move_count=2)

        self.assertFalse(has_not_moved(self.chess_board, [start], Mock()))
        self.assertFalse(has_moved_once(self.chess_board, [start], Mock()))


class TestPreMoveChecksAboutHistory(unittest.TestCase):
    def setUp(self):
        self.start = [1, 1]
        self.end = [2, 1]

        self.chess_board = ChessBoard()
        self.history = History()
        self.history.add(History.construct_history_object(self.start, self.end, Mock()))

    def test_moved_last_no_history(self):
        start = (3, 1)

        self.assertFalse(moved_last(self.chess_board, [start], History()))

    def test_moved_last_with_history_not_last_move(self):
        start = (3, 1)

        self.assertFalse(moved_last(self.chess_board, [start], self.history))

    def test_moved_last_with_history_was_last_move(self):
        start = self.end

        self.assertTrue(moved_last(self.chess_board, [start], self.history))


class TestPreMoveChecksAboutBoardLocation(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_is_empty(self):
        empty = (4, 4)
        pawn = (1, 0)
        rook = (0, 0)
        knight = (0, 1)
        bishop = (0, 2)
        queen = (0, 3)
        king = (0, 4)
        pieces = [pawn, rook, knight, bishop, queen, king]
        out_of_range = (10, 10)

        self.assertTrue(is_empty(self.chess_board, [empty], Mock()))
        self.assertFalse(is_not_empty(self.chess_board, [empty], Mock()))
        for location in pieces:
            self.assertFalse(is_empty(self.chess_board, [location], Mock()))
            self.assertTrue(is_not_empty(self.chess_board, [location], Mock()))

        self.assertFalse(is_empty(self.chess_board, pieces, Mock()))
        self.assertTrue(is_not_empty(self.chess_board, pieces, Mock()))

        self.assertTrue(is_empty(self.chess_board, [out_of_range], Mock()))
        self.assertFalse(is_not_empty(self.chess_board, [out_of_range], Mock()))

    def test_is_not_threatened(self):
        # TODO: Feature still in progress
        self.assertTrue(is_not_threatened(Mock(), Mock(), Mock()))
