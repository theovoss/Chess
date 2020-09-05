# pylint: disable=R0201

import unittest
from chess.chess_configurations import get_movement_rules, get_capture_action_rules, get_movement_directions, get_standard_chess_pieces, get_post_move_actions_rules


class TestChessConfigurer(unittest.TestCase):

    def test_get_movements(self):
        rules = get_movement_rules()
        self.assertGreater(len(rules), 7)
        self.assertIn('distance_of_one', rules)
        self.assertIn('cant_jump_pieces', rules)
        self.assertIn('doesnt_land_on_piece', rules)
        self.assertIn('ends_on_enemy', rules)
        self.assertIn('directional', rules)

    def test_get_capture_action_rules(self):
        rules = get_capture_action_rules()
        self.assertGreater(len(rules), 2)
        self.assertIn('explode', rules)
        self.assertIn('becomes_piece', rules)
        self.assertIn('captures_destination', rules)

    def test_get_post_move_action_rules(self):
        rules = get_post_move_actions_rules()
        self.assertGreater(len(rules), 1)
        self.assertIn('increment_move_count', rules)
        self.assertIn('promotable', rules)

    def test_get_movement_directions(self):
        directions = get_movement_directions()
        self.assertGreater(len(directions), 4)
        self.assertIn('horizontal', directions)
        self.assertIn('vertical', directions)
        self.assertIn('diagonal', directions)
        self.assertIn('L', directions)
        self.assertIn('extended L', directions)

    def test_get_standard_chess_pieces(self):
        chess_json = get_standard_chess_pieces()
        self.assertIn('board', chess_json.keys())
        self.assertIn('pieces', chess_json.keys())
