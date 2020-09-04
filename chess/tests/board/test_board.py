# pylint: disable=W0212

import unittest

from chess.board import ChessBoard
from chess.board.json_helper import load_json

starting_fen_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class TestBoard(unittest.TestCase):

    """Chess unit test class."""

    def setUp(self):
        self.chess_board = ChessBoard()

    @staticmethod
    def convert_default_white_spaces_to_black(white_positions):
        return [(7 - row, column) for row, column in white_positions]

    def verify_pieces_at_locations_are_correct_piece_and_color(self, white_positions, piece):
        for location in white_positions:
            assert self.chess_board[location].kind == piece
            assert self.chess_board[location].color == "white"

        black_positions = self.convert_default_white_spaces_to_black(white_positions)
        for location in black_positions:
            assert self.chess_board[location].kind == piece
            assert self.chess_board[location].color == "black"

    def test_init(self):
        assert len(self.chess_board) == 64
        assert len(self.chess_board._history) == 0

    def test_has_pawn_at_1_3(self):
        piece = self.chess_board[(1, 3)]
        assert len(piece.moves) > 0

    def test_initial_pawn_positions(self):
        expected_white_pawn_positions = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
        self.verify_pieces_at_locations_are_correct_piece_and_color(expected_white_pawn_positions, "pawn")

    def test_initial_knight_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 1), (0, 6)], "knight")

    def test_initial_rook_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 0), (0, 7)], "rook")

    def test_initial_bishop_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 2), (0, 5)], 'bishop')

    def test_initial_queen_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 3)], "queen")

    def test_initial_king_positions(self):
        self.verify_pieces_at_locations_are_correct_piece_and_color([(0, 4)], "king")

    def test_pawns_are_all_different_instances(self):
        assert self.chess_board[(1, 0)] is not self.chess_board[(1, 1)]

    def test_clear_board_removes_all_pieces(self):
        self.chess_board.clear_board()
        for location in self.chess_board.board:
            assert self.chess_board[location] is None

    def test_can_get_all_piece_names(self):
        expected = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        actual = self.chess_board.get_all_piece_names()
        self.assertEqual(actual, expected)

    @unittest.skip(reason="need to convert directions to internal output, or output a friendlier version")
    def test_starting_board_custom_export(self):
        expected_json = load_json()
        exported_json = self.chess_board.export()
        self.compare_boards(exported_json['board'], expected_json['board'])
        exported_json.pop('board')
        for key, value in exported_json.items():
            assert expected_json[key] == value
        assert len(expected_json) == len(exported_json) + 1

    @staticmethod
    def compare_boards(board1, board2):
        for player in board1:
            assert player in board2
            for piece in board1[player]:
                assert piece in board2[player]
                piece_locations1 = board1[player][piece]
                piece_locations2 = board2[player][piece]
                assert len(piece_locations1) == len(piece_locations2)
                for location in piece_locations1:
                    assert location in piece_locations2


class TestValidateKnightMoves(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move_knight(self):
        result = self.chess_board.move((0, 1), (2, 0))

        assert result
        assert self.chess_board[(2, 0)].kind == 'knight'
        assert self.chess_board._history.json['history'] == [{
            'start': (0, 1),
            'end': (2, 0),
            'piece': {
                'name': 'knight',
                'color': 'white',
                'moves': self.chess_board[(2, 0)].moves
            }}]

    def test_move_knight_on_top_of_own_pawn(self):
        assert not self.chess_board.is_valid_move((0, 1), (1, 3))
        result = self.chess_board.move((0, 1), (1, 3))

        assert not result
        assert self.chess_board[(1, 3)].kind == 'pawn'

    def test_move_knight_on_top_of_opponent_pawn(self):
        some_moves = ['move over here', 'move over there']
        self.chess_board[(1, 3)].color = 'black'
        self.chess_board[(1, 3)].moves = some_moves
        assert self.chess_board.is_valid_move((0, 1), (1, 3))
        result = self.chess_board.move((0, 1), (1, 3))

        assert result
        assert self.chess_board[(1, 3)].kind == 'knight'

        print(self.chess_board._history.json)
        self.assertEqual(self.chess_board._history.json['history'], [{
            'start': (0, 1),
            'end': (1, 3),
            'piece': {
                'name': 'knight',
                'color': 'white',
                'moves': self.chess_board[(1, 3)].moves
            },
            'captures': [
                {
                    'name': 'pawn',
                    'color': 'black',
                    'moves': some_moves,
                    'location': (1, 3)
                }
            ]
        }])


class TestValidateRookMoves(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_destinations_rook_horizontally_no_pieces_in_way(self):
        # move rook over a bit
        self.chess_board[(0, 5)] = self.chess_board[(0, 7)]
        # delete pieces to right so it has space to move back to where it started
        self.chess_board[(0, 6)] = None
        self.chess_board[(0, 7)] = None

        result = self.chess_board.end_locations_for_piece_at_location((0, 5))

        assert result == [(0, 6), (0, 7)]


class TestValidatePieceExplodes(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move_can_explode(self):
        self.chess_board[(1, 3)] = None
        self.chess_board[(0, 3)].moves[0]['capture_actions'] = ['explode']
        self.chess_board.move((0, 3), (6, 3))

        assert self.chess_board[(6, 3)].kind == 'queen'


# @unittest.skip(reason="Not yet implemented")
class TestValidateCastling(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_castling_white_king_side(self):
        self.chess_board[(0, 5)] = None
        self.chess_board[(0, 6)] = None

        assert self.chess_board[(0, 4)].kind == 'king'

        self.chess_board.move((0, 4), (0, 6))

        assert self.chess_board[(0, 6)].kind == 'king'
        assert self.chess_board[(0, 5)].kind == 'rook'
        self.assertIsNone(self.chess_board[(0, 7)])

    def test_castling_white_queen_side(self):
        self.chess_board[(0, 1)] = None
        self.chess_board[(0, 2)] = None
        self.chess_board[(0, 3)] = None

        assert self.chess_board[(0, 4)].kind == 'king'

        self.chess_board.move((0, 4), (0, 2))

        assert self.chess_board[(0, 2)].kind == 'king'
        assert self.chess_board[(0, 3)].kind == 'rook'
        self.assertIsNone(self.chess_board[(0, 0)])

    def test_castling_black_king_side(self):
        # move white so it's black's turn
        self.chess_board.move((1, 1), (2, 1))

        self.chess_board[(7, 5)] = None
        self.chess_board[(7, 6)] = None

        assert self.chess_board[(7, 4)].kind == 'king'

        self.chess_board.move((7, 4), (7, 6))

        assert self.chess_board[(7, 6)].kind == 'king'
        assert self.chess_board[(7, 5)].kind == 'rook'
        self.assertIsNone(self.chess_board[(7, 7)])

    def test_castling_black_queen_side(self):
        # move white so it's black's turn
        self.chess_board.move((1, 1), (2, 1))

        self.chess_board[(7, 1)] = None
        self.chess_board[(7, 2)] = None
        self.chess_board[(7, 3)] = None

        assert self.chess_board[(7, 4)].kind == 'king'

        self.chess_board.move((7, 4), (7, 2))

        assert self.chess_board[(7, 2)].kind == 'king'
        assert self.chess_board[(7, 3)].kind == 'rook'
        self.assertIsNone(self.chess_board[(7, 0)])


class TestBecomesPieceCaptureAction(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_rook_becomes_pawn(self):
        # change pawn in front of rook to opposite color
        self.chess_board[(1, 7)].color = 'black'
        # add becomes_piece to rook's capture actions
        self.chess_board[(0, 7)].moves[0]['capture_actions'] = ['becomes_piece']

        # make sure a black pawn is where we think it is
        assert self.chess_board[(1, 7)].kind == "pawn"
        assert self.chess_board[(1, 7)].color == "black"
        assert self.chess_board[(0, 7)].color != "black"

        self.chess_board.move((0, 7), (1, 7))

        assert self.chess_board[(1, 7)].kind == "pawn"
        assert self.chess_board[(1, 7)].color == "white"


class TestValidatePawnMoves(unittest.TestCase):

    """Chess movement unit tests."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_pawn_can_move_forward(self):
        assert self.chess_board[(2, 3)] is None
        ends = self.chess_board.end_locations_for_piece_at_location((1, 3))
        assert ends == [(2, 3), (3, 3)]

    def test_pawn_cant_move_forward_twice_if_not_first_move(self):
        assert self.chess_board[(2, 3)] is None
        assert self.chess_board[(3, 3)] is None
        self.chess_board[(1, 3)].move_count = 1
        ends = self.chess_board.end_locations_for_piece_at_location((1, 3))
        assert ends == [(2, 3)]

    def test_white_pawn_promotion(self):
        # move white pawn 1 away

        promotion_location = (7, 2)  # diagonal capture for promotion
        self.chess_board[(6, 1)] = self.chess_board[(1, 1)]
        self.chess_board.move((6, 1), promotion_location)

        self.assertTrue(self.chess_board[promotion_location].promote_me_daddy)

        self.chess_board.promote(promotion_location, 'rook')
        self.assertEqual(self.chess_board[promotion_location].kind, 'rook')

    def test_pawn_cant_promote_just_anywhere(self):
        # move white pawn 1 away
        promotion_location = (2, 1)
        self.chess_board.move((1, 1), promotion_location)

        self.assertFalse(self.chess_board[promotion_location].promote_me_daddy)

        self.chess_board.promote(promotion_location, 'rook')
        self.assertEqual(self.chess_board[promotion_location].kind, 'pawn')


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_first(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))
        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(2, 1)] is None
        assert self.chess_board[(1, 1)] is None
        self.chess_board.first()
        assert self.chess_board[(1, 1)] is not None
        assert self.chess_board[(2, 1)] is None
        assert self.chess_board[(3, 1)] is None

    def test_next(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))

        assert self.chess_board[(1, 1)] is None
        assert self.chess_board[(6, 2)] is None

        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(4, 2)] is not None

        self.chess_board.first()

        assert self.chess_board[(1, 1)] is not None
        assert self.chess_board[(6, 2)] is not None

        self.chess_board.next()  # 1,1 -> 2, 1

        assert self.chess_board[(1, 1)] is None
        assert self.chess_board[(2, 1)] is not None

        self.chess_board.next()  # 6,2 -> 5, 2

        assert self.chess_board[(6, 2)] is None
        assert self.chess_board[(5, 2)] is not None

        self.chess_board.next()  # 2, 1 -> 3, 1

        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(2, 1)] is None

        self.chess_board.next()  # 5, 2 -> 4, 2

        assert self.chess_board[(5, 2)] is None
        assert self.chess_board[(4, 2)] is not None

        self.chess_board.next()
        self.chess_board.next()
        self.chess_board.next()

        assert self.chess_board[(1, 1)] is None
        assert self.chess_board[(6, 2)] is None

        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(4, 2)] is not None

    def test_previous(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))
        assert self.chess_board[(4, 2)] is not None
        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(5, 2)] is None
        assert self.chess_board[(2, 1)] is None

        self.chess_board.previous()

        assert self.chess_board[(4, 2)] is None
        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(5, 2)] is not None
        assert self.chess_board[(2, 1)] is None

        self.chess_board.previous()

        assert self.chess_board[(4, 2)] is None
        assert self.chess_board[(3, 1)] is None
        assert self.chess_board[(5, 2)] is not None
        assert self.chess_board[(2, 1)] is not None

        self.chess_board.previous()
        self.chess_board.previous()
        self.chess_board.previous()
        self.chess_board.previous()
        self.chess_board.previous()

        self.chess_board.next()

        assert self.chess_board[(2, 1)] is not None
        assert self.chess_board[(1, 1)] is None

    def test_can_undo_and_redo_last_move(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))
        assert self.chess_board[(4, 2)] is not None
        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(5, 2)] is None
        assert self.chess_board[(2, 1)] is None

        self.chess_board.previous()

        assert self.chess_board[(4, 2)] is None
        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(5, 2)] is not None
        assert self.chess_board[(2, 1)] is None

        self.chess_board.next()

        assert self.chess_board[(4, 2)] is not None
        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(5, 2)] is None
        assert self.chess_board[(2, 1)] is None

    def test_export_includes_history(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))
        assert self.chess_board[(4, 2)] is not None
        assert self.chess_board[(3, 1)] is not None
        assert self.chess_board[(5, 2)] is None
        assert self.chess_board[(2, 1)] is None

        export = self.chess_board.export()
        new_board = ChessBoard(export)

        assert len(new_board._history) == 4
        assert new_board._history._index == 3

        assert new_board[(4, 2)] is not None
        assert new_board[(3, 1)] is not None
        assert new_board[(5, 2)] is None
        assert new_board[(2, 1)] is None

        new_board.previous()

        assert new_board[(4, 2)] is None
        assert new_board[(3, 1)] is not None
        assert new_board[(5, 2)] is not None
        assert new_board[(2, 1)] is None

        new_board.previous()

        assert new_board[(4, 2)] is None
        assert new_board[(3, 1)] is None
        assert new_board[(5, 2)] is not None
        assert new_board[(2, 1)] is not None


class TestExportImport(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_initialize_and_export_doesnt_lose_data(self):
        exported_data = self.chess_board.export()

        # simulating all the pawns having been captured
        exported_data['board']['Player 1'].pop('pawn', None)
        exported_data['board']['Player 2'].pop('pawn', None)

        self.assertIn('pawn', exported_data['pieces'])
        self.assertNotIn('pawn', exported_data['board']['Player 1'])
        self.assertNotIn('pawn', exported_data['board']['Player 2'])

        chess_board = ChessBoard(exported_data)

        new_exported_data = chess_board.export()

        self.assertIn('pawn', new_exported_data['pieces'])
        self.assertNotIn('pawn', exported_data['board']['Player 1'])
        self.assertNotIn('pawn', exported_data['board']['Player 2'])

    def test_initialize_and_export_includes_promotable(self):
        # move white pawn to end
        self.chess_board[(6, 1)] = self.chess_board[(1, 1)]
        self.chess_board.move((6, 1), (7, 2))
        self.assertTrue(self.chess_board[(7, 2)].promote_me_daddy)

        exported_data = self.chess_board.export()

        chess_board = ChessBoard(exported_data)

        self.assertTrue(chess_board[(7, 2)].promote_me_daddy)
