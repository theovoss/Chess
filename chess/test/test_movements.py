"""Chess Board unit test module."""

import unittest
from unittest.mock import Mock
from chess import movement
from chess.board.chess_board import ChessBoard


class TestMovements(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.board = ChessBoard().board
        self.distance_of_one = getattr(movement, "distance_of_one")
        self.doesnt_land_on_own_piece = getattr(movement, "doesnt_land_on_own_piece")
        self.cant_jump_pieces = getattr(movement, "cant_jump_pieces")
        self.get_all_potential_end_locations = getattr(movement, "get_all_potential_end_locations")
        self.ends_on_enemy = getattr(movement, "ends_on_enemy")
        self.doesnt_land_on_piece = getattr(movement, "doesnt_land_on_piece")

    def test_distance_of_one_filtering_given_positions(self):
        directions = [(1, 0), (0, 1), (0, -1)]
        start_square = (1, 1)
        already_acceptable_possitions = [(1, 2), (1, 0), (2, 1), (3, 3), (5, 5), (2, 3), (9, 1)]
        positions = self.distance_of_one(self.board, start_square, directions, potential_end_locations=already_acceptable_possitions)
        expected_positions = [(1, 2), (1, 0), (2, 1)]
        assert len(positions) == len(expected_positions)
        for pos in positions:
            assert pos in positions

    def test_does_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.board[start] = Mock(color=1)
        self.board[end] = Mock(color=1)
        potential_end_locations = [end]
        ret_val = self.doesnt_land_on_own_piece(self.board, start, None, potential_end_locations)
        assert ret_val == []

    def test_doesnt_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.board[start] = Mock(color=1)
        self.board[end] = Mock(color=2)
        potential_end_locations = [end]
        ret_val = self.doesnt_land_on_own_piece(self.board, start, None, potential_end_locations)
        assert ret_val == [(1, 0)]

    def test_cant_jump_pieces(self):
        start = (2, 2)
        middle = (4, 2)

        self.board[start] = Mock()
        self.board[middle] = Mock()

        starting_end_locations = [(3, 2), (4, 2), (5, 2), (6, 2)]
        expected_positions = [(3, 2), (4, 2)]
        new_end_locations = self.cant_jump_pieces(self.board, start, None, starting_end_locations)

        assert new_end_locations == expected_positions

    def test_cant_jump_pieces_doesnt_limit_if_no_pieces_are_in_the_way(self):
        start = (1, 1)

        self.board[start] = Mock()

        starting_end_locations = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]

        new_end_locations = self.cant_jump_pieces(self.board, start, None, starting_end_locations)

        assert new_end_locations == starting_end_locations

    def test_get_potential_end_squares_vertical(self):
        start = (0, 0)
        directions = [(0, 1)]
        ends = self.get_all_potential_end_locations(start, directions, self.board)

        expected_ends = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
        assert ends == expected_ends

    def test_get_potential_end_squares_horizontal(self):
        start = (0, 0)
        directions = [(1, 0)]
        ends = self.get_all_potential_end_locations(start, directions, self.board)

        expected_ends = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        assert ends == expected_ends

    def test_get_potential_end_squares_diagonal(self):
        start = (0, 0)
        directions = [(1, 1)]
        ends = self.get_all_potential_end_locations(start, directions, self.board)

        expected_ends = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
        assert ends == expected_ends

    def test_get_potential_end_squares_rook(self):
        start = (0, 0)
        directions = [(2, 1)]
        ends = self.get_all_potential_end_locations(start, directions, self.board)

        expected_ends = [(2, 1), (4, 2), (6, 3)]
        assert ends == expected_ends

    def test_ends_on_enemy_no_enemy(self):
        start = (0, 0)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        ends = self.ends_on_enemy(self.board, start, None, potential_end_locations)
        assert ends == []

    def test_ends_on_same_players_piece(self):
        start = (0, 0)
        self.board[start] = Mock(color=1)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        for end in potential_end_locations:
            self.board[end] = Mock(color=1)
        ends = self.ends_on_enemy(self.board, start, None, potential_end_locations)
        assert ends == []

    def test_ends_on_enemy_players_piece(self):
        start = (0, 0)
        self.board[start] = Mock(color=1)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        for end in potential_end_locations:
            self.board[end] = Mock(color=1)
        self.board[end] = Mock(color=2)
        ends = self.ends_on_enemy(self.board, start, None, potential_end_locations)
        assert ends == [(2, 2)]

    def test_doesnt_land_on_piece(self):
        start = (1, 1)
        potential_end_locations = [(1, 2), (1, 3), (2, 4), (1, 4), (0, 2)]
        for end in potential_end_locations:
            self.board[end] = Mock(color=2)
        potential_end_locations.append((2, 3))
        ends = self.doesnt_land_on_piece(self.board, start, None, potential_end_locations)
        assert ends == [(2, 3)]
