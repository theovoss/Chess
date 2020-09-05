# pylint: disable=W0212

import unittest
from unittest.mock import Mock

from chess.board.json_helper import *
from chess.board.json_helper import _get_move_definition
from chess.chess_configurations import get_standard_chess_pieces
from chess.piece import Piece


class TestBoard(unittest.TestCase):
    def test_load_json(self):
        expected = {'hello': 'goodbye'}
        self.assertEqual(expected, load_json(expected))

    def test_load_json_standard_chess_when_nothing_supplied(self):
        self.assertEqual(load_json(), get_standard_chess_pieces())

    def test_get_move_definition_with_no_match(self):
        definition = get_standard_chess_pieces()
        knight_moves = definition['pieces']['knight']['moves']
        knight = Piece('knight', 'white', knight_moves)
        actual = _get_move_definition(Mock(), knight, (1, 1), (1, 2))
        self.assertIsNone(actual)

    def test_get_capture_actions_with_no_match(self):
        definition = get_standard_chess_pieces()
        knight_moves = definition['pieces']['knight']['moves']
        knight = Piece('knight', 'white', knight_moves)
        actual = get_capture_actions(Mock(), knight, (1, 1), (1, 2))
        self.assertEqual(actual, [capture_actions.captures_destination])

    def test_get_post_move_actions_with_no_match(self):
        definition = get_standard_chess_pieces()
        knight_moves = definition['pieces']['knight']['moves']
        knight = Piece('knight', 'white', knight_moves)
        actual = get_post_move_actions(Mock(), knight, (1, 1), (1, 2))
        self.assertEqual(actual, [post_move_actions.increment_move_count])

    def test_get_post_move_actions_with_match(self):
        definition = get_standard_chess_pieces()
        knight_moves = definition['pieces']['knight']['moves']
        knight_moves[0] = {'directions': ['vertical', 'horizontal'], 'post_move_actions': ['doesnt_survive']}
        knight = Piece('knight', 'white', knight_moves)
        actual = get_post_move_actions(Mock(), knight, (1, 1), (1, 2))
        self.assertEqual(actual, [post_move_actions.doesnt_survive])
