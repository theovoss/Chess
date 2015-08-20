"""Chess Board unit test module."""

import unittest
from unittest.mock import Mock
from chess.movement import (distance_of_one,
                            doesnt_land_on_own_piece,
                            cant_jump_pieces)
from chess.board.chess_board import ChessBoard


class TestMovements(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.board = ChessBoard().board

    def test_distance_of_one(self):
        start_square = (1, 1)
        positions = distance_of_one(start_square)
        expected_positions = [(1, 2), (1, 0), (2, 1), (2, 2), (2, 0), (0, 1), (0, 0), (0, 2)]
        assert len(positions) == len(expected_positions)
        for pos in positions:
            assert pos in positions

    def test_distance_of_one_filtering_given_positions(self):
        start_square = (1, 1)
        already_acceptable_possitions = [(1, 2), (1, 0), (2, 1), (3, 3), (5, 5), (2, 3), (9, 1)]
        positions = distance_of_one(start_square, potential_end_locations=already_acceptable_possitions)
        expected_positions = [(1, 2), (1, 0), (2, 1)]
        assert len(positions) == len(expected_positions)
        for pos in positions:
            assert pos in positions

    def test_does_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.board[start] = Mock(owner=1)
        self.board[end] = Mock(owner=1)
        ret_val = doesnt_land_on_own_piece(self.board, end, start)
        assert ret_val is False

    def test_doesnt_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.board[start] = Mock(owner=1)
        self.board[end] = Mock(owner=2)
        ret_val = doesnt_land_on_own_piece(self.board, end, start)
        assert ret_val is True

    def test_cant_jump_pieces(self):
        start = (1, 1)
        middle = (3, 1)

        self.board[start] = Mock()
        self.board[middle] = Mock()

        starting_end_locations = [(2, 1), (3, 1), (4, 1), (5, 1)]
        expected_positions = [(2, 1), (3, 1)]
        new_end_locations = cant_jump_pieces(self.board, start, starting_end_locations)

        assert new_end_locations == expected_positions

    def test_cant_jump_pieces_doesnt_limit_if_no_pieces_are_in_the_way(self):
        start = (1, 1)

        self.board[start] = Mock()

        starting_end_locations = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]

        new_end_locations = cant_jump_pieces(self.board, start, starting_end_locations)

        assert new_end_locations == starting_end_locations
