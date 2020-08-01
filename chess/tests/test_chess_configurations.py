# pylint: disable=R0201

import unittest
from chess.chess_configurations import get_movement_rules, get_capture_action_rules, get_movement_directions, get_standard_chess_pieces


class TestChessConfigurer(unittest.TestCase):

    def test_get_movements(self):
        rules = get_movement_rules()
        assert len(rules) >= 8
        assert 'distance_of_one' in rules
        assert 'cant_jump_pieces' in rules
        assert 'doesnt_land_on_piece' in rules
        assert 'ends_on_enemy' in rules
        assert 'directional' in rules

    def test_get_capture_action_rules(self):
        rules = get_capture_action_rules()
        assert len(rules) > 3
        assert 'explode' in rules
        assert 'replace' in rules
        assert 'becomes_piece' in rules
        assert 'increment_move_count' in rules

    def test_get_movement_directions(self):
        directions = get_movement_directions()
        assert len(directions) >= 5
        assert 'horizontal' in directions
        assert 'vertical' in directions
        assert 'diagonal' in directions
        assert 'L' in directions
        assert 'extended L' in directions

    def test_get_standard_chess_pieces(self):
        chess_json = get_standard_chess_pieces()
        assert 'board' in chess_json.keys()
        assert 'pieces' in chess_json.keys()
