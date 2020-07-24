"""Chess Board unit test module."""

import unittest
from unittest.mock import Mock
from chess.movement import (distance_of_one,
                            doesnt_land_on_piece,
                            doesnt_land_on_own_piece,
                            cant_jump_pieces,
                            ends_on_enemy,
                            directional,
                            first_move,
                            get_all_potential_end_locations,
                            alternates_landing_on_enemy_and_empty_space)
from chess.board.chess_board import ChessBoard


class TestMovements(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_distance_of_one_filtering_given_positions(self):
        directions = [(1, 0), (0, 1), (0, -1)]
        start_square = (1, 1)
        already_acceptable_possitions = [(1, 2), (1, 0), (2, 1), (3, 3), (5, 5), (2, 3), (9, 1)]
        positions = distance_of_one(self.chess_board, start_square, directions, potential_end_locations=already_acceptable_possitions, player_direction=Mock())
        expected_positions = [(1, 2), (1, 0), (2, 1)]
        assert len(positions) == len(expected_positions)
        for pos in positions:
            assert pos in positions

    def test_does_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.chess_board[start] = Mock(color=1)
        self.chess_board[end] = Mock(color=1)
        potential_end_locations = [end]
        ret_val = doesnt_land_on_own_piece(self.chess_board, start, None, potential_end_locations, Mock())
        assert ret_val == []

    def test_doesnt_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.chess_board[start] = Mock(color=1)
        self.chess_board[end] = Mock(color=2)
        potential_end_locations = [end]
        ret_val = doesnt_land_on_own_piece(self.chess_board, start, None, potential_end_locations, Mock())
        assert ret_val == [(1, 0)]

    def test_cant_jump_pieces(self):
        start = (2, 2)
        middle = (4, 2)

        self.chess_board[start] = Mock()
        self.chess_board[middle] = Mock()

        starting_end_locations = [(3, 2), (4, 2), (5, 2), (6, 2)]
        expected_positions = [(3, 2), (4, 2)]
        new_end_locations = cant_jump_pieces(self.chess_board, start, None, starting_end_locations, Mock())

        assert new_end_locations == expected_positions

    def test_cant_jump_own_pieces(self):
        start = (7, 2)
        middle = (4, 2)

        self.chess_board[start] = Mock(color=1)
        self.chess_board[middle] = Mock(color=1)
        self.chess_board[(6, 2)] = None
        self.chess_board[(5, 2)] = None

        starting_end_locations = [(3, 2), (4, 2), (6, 2)]
        expected_positions = [(4, 2), (6, 2)]
        new_end_locations = cant_jump_pieces(self.chess_board, start, None, starting_end_locations, Mock())

        assert new_end_locations == expected_positions

    def test_cant_jump_own_pieces_diagonally(self):
        start = (0, 2)
        middle = (1, 1)

        self.chess_board[start] = Mock(color=1)
        self.chess_board[middle] = Mock(color=1)
        self.chess_board[(2, 0)] = None

        starting_end_locations = [(1, 1), (2, 0)]
        expected_positions = [(1, 1)]
        new_end_locations = cant_jump_pieces(self.chess_board, start, None, starting_end_locations, Mock())

        assert new_end_locations == expected_positions

    def test_cant_jump_pieces_divide_by_one_error(self):
        start = (2, 2)

        self.chess_board[start] = Mock()

        starting_end_locations = [(3, 2), (1, 2)]
        expected_positions = [(3, 2), (1, 2)]
        new_end_locations = cant_jump_pieces(self.chess_board, start, None, starting_end_locations, Mock())

        assert new_end_locations == expected_positions

    def test_cant_jump_pieces_doesnt_limit_if_no_pieces_are_in_the_way(self):
        start = (1, 1)

        self.chess_board[start] = Mock()

        starting_end_locations = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]

        new_end_locations = cant_jump_pieces(self.chess_board, start, None, starting_end_locations, Mock())

        assert new_end_locations == starting_end_locations

    def test_get_potential_end_squares_vertical(self):
        start = (0, 0)
        directions = [(0, 1)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
        assert ends == expected_ends

    def test_get_potential_end_squares_horizontal(self):
        start = (0, 0)
        directions = [(1, 0)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        assert ends == expected_ends

    def test_get_potential_end_squares_diagonal(self):
        start = (0, 0)
        directions = [(1, 1)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
        assert ends == expected_ends

    def test_get_potential_end_squares_rook(self):
        start = (0, 0)
        directions = [(2, 1)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(2, 1), (4, 2), (6, 3)]
        assert ends == expected_ends

    def test_ends_on_enemy_no_enemy(self):
        start = (0, 0)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        ends = ends_on_enemy(self.chess_board, start, None, potential_end_locations, Mock())
        assert ends == []

    def test_ends_on_same_players_piece(self):
        start = (0, 0)
        self.chess_board[start] = Mock(color=1)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        for end in potential_end_locations:
            self.chess_board[end] = Mock(color=1)
        ends = ends_on_enemy(self.chess_board, start, None, potential_end_locations, Mock())
        assert ends == []

    def test_ends_on_enemy_players_piece(self):
        start = (0, 0)
        self.chess_board[start] = Mock(color=1)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        end = None
        for end in potential_end_locations:
            self.chess_board[end] = Mock(color=1)
        self.chess_board[end] = Mock(color=2)
        ends = ends_on_enemy(self.chess_board, start, None, potential_end_locations, Mock())
        assert ends == [(2, 2)]

    def test_doesnt_land_on_piece(self):
        start = (1, 1)
        potential_end_locations = [(1, 2), (1, 3), (2, 4), (1, 4), (0, 2)]
        for end in potential_end_locations:
            self.chess_board[end] = Mock(color=2)
        potential_end_locations.append((2, 3))
        ends = doesnt_land_on_piece(self.chess_board, start, None, potential_end_locations, Mock())
        assert ends == [(2, 3)]

    def test_directional_white(self):
        start = (3, 1)
        potential_end_locations = [(4, 1), (2, 1)]

        ends = directional(self.chess_board, start, None, potential_end_locations, (1, 0))
        assert ends == [(4, 1)]

    def test_directional_black(self):
        start = (3, 1)
        potential_end_locations = [(4, 1), (2, 1)]

        ends = directional(self.chess_board, start, None, potential_end_locations, (-1, 0))
        assert ends == [(2, 1)]

    def test_directional_diagonal(self):
        start = (3, 1)
        potential_end_locations = [(4, 2), (2, 2)]

        ends = directional(self.chess_board, start, None, potential_end_locations, (1, 1))
        assert ends == [(4, 2)]

    def test_first_move(self):
        start = (3, 1)
        self.chess_board[start] = Mock(move_count=0)
        potential_end_locations = [(4, 2), (4, 3), (2, 2), (2, 1), (2, 2)]

        ends = first_move(self.chess_board, start, None, potential_end_locations, Mock())

        assert ends == potential_end_locations

    def test_not_first_move(self):
        start = (3, 1)
        self.chess_board[start] = Mock(move_count=1)
        potential_end_locations = [(4, 2), (4, 3), (2, 2), (2, 1), (2, 2)]

        ends = first_move(self.chess_board, start, None, potential_end_locations, Mock())

        assert ends == []

    def test_alternates_landing_on_enemy_and_empty_space(self):
        start = (0, 0)
        self.chess_board[start] = Mock(move_count=1)
        potential_end_locations = [(1, 1), (2, 2), (3, 3)]
        self.chess_board[(1, 1)] = Mock(color="purple")

        ends = alternates_landing_on_enemy_and_empty_space(self.chess_board, start, [(1, 1)], potential_end_locations, Mock())

        assert ends == [(2, 2)]

    def test_alternates_landing_on_enemy_and_empty_space_and_switches_directions(self):
        start = (0, 0)
        self.chess_board[start] = Mock(move_count=1)
        potential_end_locations = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
        self.chess_board[(1, 1)] = Mock(color="purple")
        self.chess_board[(3, 3)] = Mock(color="purple")
        ends = alternates_landing_on_enemy_and_empty_space(self.chess_board, start, [(1, 1)], potential_end_locations, Mock())

        assert ends == [(2, 2), (4, 4)]

    # def test_take_a_piece_and_become_it(self):
    #     start = (0, 0)
    #     start = (1, 1)
    #     self.chess_board[start] = Mock(color="pink")
    #     self.chess_board[end] = Mock(color="purple")
    #     potential_end_locations = [end]
    #     ends = take_a_piece_become_the_piece(self.chess_board, start, [(1, 1)], potential_end_locations, Mock())

    #     # hmmm. assert it's in ends... how to actually move though and check that it took and became the movements.
    #     # needs more setup
