"""Chess Board unit test module."""

import unittest
from unittest.mock import Mock
from chess.move_pipeline.movement import (
    distance_of_one,
    distance_of_two,
    doesnt_land_on_piece,
    doesnt_land_on_own_piece,
    cant_jump_pieces,
    ends_on_enemy,
    directional,
    get_all_potential_end_locations,
    alternates_landing_on_enemy_and_empty_space
)
from chess.board.chess_board import ChessBoard
from chess.move_pipeline.data import ConditionArgs


class TestMovements(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_distance_of_one_filtering_given_positions(self):
        move = {'directions': [(1, 0), (0, 1), (0, -1)]}
        start_square = (1, 1)
        already_acceptable_possitions = [(1, 2), (1, 0), (2, 1), (3, 3), (5, 5), (2, 3), (9, 1)]

        args = ConditionArgs.generate(self.chess_board, move, start_square, already_acceptable_possitions, Mock())
        positions = distance_of_one(args)
        expected_positions = [(1, 2), (1, 0), (2, 1)]
        self.assertEqual(len(positions), len(expected_positions))
        for pos in positions:
            self.assertIn(pos, positions)

    def test_distance_of_two_filtering_given_positions(self):
        move = {'directions': [(1, 0), (0, 1), (0, -1)]}
        start_square = (1, 1)
        already_acceptable_possitions = [(1, 2), (1, 0), (2, 1), (3, 3), (5, 5), (2, 3), (9, 1), (3, 1), (1, 3)]

        args = ConditionArgs.generate(self.chess_board, move, start_square, already_acceptable_possitions, Mock())
        positions = distance_of_two(args)
        expected_positions = [(1, 3), (3, 1)]
        self.assertEqual(len(positions), len(expected_positions))
        for pos in positions:
            self.assertIn(pos, positions)

    def test_does_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.chess_board[start] = Mock(color=1)
        self.chess_board[end] = Mock(color=1)
        potential_end_locations = [end]

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, Mock())
        ret_val = doesnt_land_on_own_piece(args)
        self.assertEqual(ret_val, [])

    def test_doesnt_end_on_own_piece(self):
        start = (1, 1)
        end = (1, 0)
        self.chess_board[start] = Mock(color=1)
        self.chess_board[end] = Mock(color=2)
        potential_end_locations = [end]

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, Mock())
        ret_val = doesnt_land_on_own_piece(args)
        self.assertEqual(ret_val, [(1, 0)])

    def test_cant_jump_pieces(self):
        start = (2, 2)
        middle = (4, 2)

        self.chess_board[start] = Mock()
        self.chess_board[middle] = Mock()

        starting_end_locations = [(3, 2), (4, 2), (5, 2), (6, 2)]
        expected_positions = [(3, 2), (4, 2)]

        args = ConditionArgs.generate(self.chess_board, {}, start, starting_end_locations, Mock())

        new_end_locations = cant_jump_pieces(args)

        self.assertEqual(new_end_locations, expected_positions)

    def test_cant_jump_own_pieces(self):
        start = (7, 2)
        middle = (4, 2)

        self.chess_board[start] = Mock(color=1)
        self.chess_board[middle] = Mock(color=1)
        self.chess_board[(6, 2)] = None
        self.chess_board[(5, 2)] = None

        starting_end_locations = [(3, 2), (4, 2), (6, 2)]
        expected_positions = [(4, 2), (6, 2)]

        args = ConditionArgs.generate(self.chess_board, {}, start, starting_end_locations, Mock())

        new_end_locations = cant_jump_pieces(args)

        self.assertEqual(new_end_locations, expected_positions)

    def test_cant_jump_own_pieces_diagonally(self):
        start = (0, 2)
        middle = (1, 1)

        self.chess_board[start] = Mock(color=1)
        self.chess_board[middle] = Mock(color=1)
        self.chess_board[(2, 0)] = None

        starting_end_locations = [(1, 1), (2, 0)]
        expected_positions = [(1, 1)]

        args = ConditionArgs.generate(self.chess_board, {}, start, starting_end_locations, Mock())

        new_end_locations = cant_jump_pieces(args)

        self.assertEqual(new_end_locations, expected_positions)

    def test_cant_jump_pieces_divide_by_one_error(self):
        start = (2, 2)

        self.chess_board[start] = Mock()

        starting_end_locations = [(3, 2), (1, 2)]
        expected_positions = [(3, 2), (1, 2)]

        args = ConditionArgs.generate(self.chess_board, {}, start, starting_end_locations, Mock())

        new_end_locations = cant_jump_pieces(args)

        self.assertEqual(new_end_locations, expected_positions)

    def test_cant_jump_pieces_doesnt_limit_if_no_pieces_are_in_the_way(self):
        start = (1, 1)

        self.chess_board[start] = Mock()
        self.chess_board[(6, 1)] = None
        self.assertIsNone(self.chess_board[(6, 1)])

        starting_end_locations = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]

        args = ConditionArgs.generate(self.chess_board, {}, start, starting_end_locations, Mock())
        new_end_locations = cant_jump_pieces(args)

        self.assertEqual(new_end_locations, starting_end_locations)

    def test_get_potential_end_squares_vertical(self):
        start = (0, 0)
        directions = [(0, 1)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
        self.assertEqual(ends, expected_ends)

    def test_get_potential_end_squares_horizontal(self):
        start = (0, 0)
        directions = [(1, 0)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        self.assertEqual(ends, expected_ends)

    def test_get_potential_end_squares_diagonal(self):
        start = (0, 0)
        directions = [(1, 1)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
        self.assertEqual(ends, expected_ends)

    def test_get_potential_end_squares_rook(self):
        start = (0, 0)
        directions = [(2, 1)]
        ends = get_all_potential_end_locations(start, directions, self.chess_board)

        expected_ends = [(2, 1), (4, 2), (6, 3)]
        self.assertEqual(ends, expected_ends)

    def test_ends_on_enemy_no_enemy(self):
        start = (0, 0)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, Mock())

        ends = ends_on_enemy(args)
        self.assertEqual(ends, [])

    def test_ends_on_same_players_piece(self):
        start = (0, 0)
        self.chess_board[start] = Mock(color=1)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        for end in potential_end_locations:
            self.chess_board[end] = Mock(color=1)

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, Mock())

        ends = ends_on_enemy(args)
        self.assertEqual(ends, [])

    def test_ends_on_enemy_players_piece(self):
        start = (0, 0)
        self.chess_board[start] = Mock(color=1)
        potential_end_locations = [(1, 0), (2, 0), (2, 2)]
        end = None
        for end in potential_end_locations:
            self.chess_board[end] = Mock(color=1)
        self.chess_board[end] = Mock(color=2)

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, Mock())

        ends = ends_on_enemy(args)
        self.assertEqual(ends, [(2, 2)])

    def test_doesnt_land_on_piece(self):
        start = (1, 1)
        potential_end_locations = [(1, 2), (1, 3), (2, 4), (1, 4), (0, 2)]
        for end in potential_end_locations:
            self.chess_board[end] = Mock(color=2)
        potential_end_locations.append((2, 3))

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, Mock())

        ends = doesnt_land_on_piece(args)
        self.assertEqual(ends, [(2, 3)])

    def test_directional_white(self):
        start = (3, 1)
        potential_end_locations = [(4, 1), (2, 1)]

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, (1, 0))

        ends = directional(args)
        self.assertEqual(ends, [(4, 1)])

    def test_directional_black(self):
        start = (3, 1)
        potential_end_locations = [(4, 1), (2, 1)]

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, (-1, 0))

        ends = directional(args)
        self.assertEqual(ends, [(2, 1)])

    def test_directional_diagonal(self):
        start = (3, 1)
        potential_end_locations = [(4, 2), (2, 2)]

        args = ConditionArgs.generate(self.chess_board, {}, start, potential_end_locations, (1, 1))

        ends = directional(args)
        self.assertEqual(ends, [(4, 2)])

    def test_alternates_landing_on_enemy_and_empty_space(self):
        start = (0, 0)
        self.chess_board[start] = Mock(move_count=1)
        potential_end_locations = [(1, 1), (2, 2), (3, 3)]
        self.chess_board[(1, 1)] = Mock(color="purple")

        args = ConditionArgs.generate(self.chess_board, {'directions': [(1, 1)]}, start, potential_end_locations, Mock())

        ends = alternates_landing_on_enemy_and_empty_space(args)

        self.assertEqual(ends, [(2, 2)])

    def test_alternates_landing_on_enemy_and_empty_space_and_switches_directions(self):
        start = (0, 0)
        self.chess_board[start] = Mock(move_count=1)
        potential_end_locations = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
        self.chess_board[(1, 1)] = Mock(color="purple")
        self.chess_board[(3, 3)] = Mock(color="purple")

        args = ConditionArgs.generate(self.chess_board, {'directions': [(1, 1)]}, start, potential_end_locations, Mock())

        ends = alternates_landing_on_enemy_and_empty_space(args)

        self.assertEqual(ends, [(2, 2), (4, 4)])
