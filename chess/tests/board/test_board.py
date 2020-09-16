# pylint: disable=W0212

import unittest
from parameterized import parameterized

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

    def test_init(self):
        self.assertEqual(len(self.chess_board), 64)
        self.assertEqual(len(self.chess_board._history), 0)

    def test_has_pawn_at_1_3(self):
        piece = self.chess_board[(1, 3)]
        self.assertGreater(len(piece.moves), 0)

    # locations, piece kind
    @parameterized.expand([
        ([(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)], 'pawn'),
        ([(0, 1), (0, 6)], "knight"),
        ([(0, 0), (0, 7)], "rook"),
        ([(0, 2), (0, 5)], 'bishop'),
        ([(0, 3)], "queen"),
        ([(0, 4)], "king")
    ])
    def test_initial_piece_positions(self, white_positions, piece):
        for location in white_positions:
            self.assertEqual(self.chess_board[location].kind, piece)
            self.assertEqual(self.chess_board[location].color, "white")

        black_positions = self.convert_default_white_spaces_to_black(white_positions)
        for location in black_positions:
            self.assertEqual(self.chess_board[location].kind, piece)
            self.assertEqual(self.chess_board[location].color, "black")

    def test_pawns_are_all_different_instances(self):
        self.assertIsNot(self.chess_board[(1, 0)], self.chess_board[(1, 1)])

    def test_black_cant_move_when_whites_turn(self):
        self.assertFalse(self.chess_board.move((6, 3), (5, 3)))

    def test_white_cant_move_when_blacks_turn(self):
        self.chess_board.move((1, 1), (2, 1))
        self.assertFalse(self.chess_board.move((2, 1), (3, 1)))

    def test_clear_board_removes_all_pieces(self):
        self.chess_board.clear_board()
        for location in self.chess_board.board:
            self.assertIsNone(self.chess_board[location])

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
            self.assertEqual(expected_json[key], value)
        self.assertEqual(len(expected_json), len(exported_json) + 1)

    def compare_boards(self, board1, board2):
        for player in board1:
            self.assertIn(player, board2)
            for piece in board1[player]:
                self.assertIn(piece, board2[player])
                piece_locations1 = board1[player][piece]
                piece_locations2 = board2[player][piece]
                self.assertEqual(len(piece_locations1), len(piece_locations2))
                for location in piece_locations1:
                    self.assertIn(location, piece_locations2)


class TestEndgame(unittest.TestCase):
    def setUp(self):
        self.chess_board = ChessBoard()

    def test_endgame(self):
        self.chess_board.check_endgame_conditions()

class TestKnightMoves(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move_knight(self):
        result = self.chess_board.move((0, 1), (2, 0))

        self.assertTrue(result)
        self.assertEqual(self.chess_board[(2, 0)].kind, 'knight')
        self.assertEqual(self.chess_board._history.json['history'], [{
            'start': (0, 1),
            'end': (2, 0),
            'piece': {
                'name': 'knight',
                'color': 'white',
                'moves': self.chess_board[(2, 0)].moves
            }}])

    def test_move_knight_on_top_of_own_pawn(self):
        self.assertIsNotNone(self.chess_board[(1, 3)])
        self.assertEqual(self.chess_board[(0, 1)].color, self.chess_board[(1, 3)].color)
        self.assertFalse(self.chess_board.is_valid_move((0, 1), (1, 3)))
        result = self.chess_board.move((0, 1), (1, 3))

        self.assertFalse(result)
        self.assertEqual(self.chess_board[(1, 3)].kind, 'pawn')

    def test_move_knight_on_top_of_opponent_pawn(self):
        self.chess_board[(1, 3)].color = 'black'
        self.assertTrue(self.chess_board.is_valid_move((0, 1), (1, 3)))
        result = self.chess_board.move((0, 1), (1, 3))

        self.assertTrue(result)
        self.assertEqual(self.chess_board[(1, 3)].kind, 'knight')

        actual = self.chess_board._history.json['history'][0]
        expected = {
            'start': (0, 1),
            'end': (1, 3),
            'piece': {
                'name': 'knight',
                'color': 'white',
                'moves': self.chess_board[(1, 3)].moves
            }
        }
        self.assertEqual(actual['start'], expected['start'])
        self.assertEqual(actual['end'], expected['end'])
        self.assertEqual(actual['piece'], expected['piece'])
        self.assertEqual(len(actual['captures']), 1)


class TestRookMoves(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_destinations_rook_horizontally_no_pieces_in_way(self):
        # move rook over a bit
        self.chess_board[(0, 5)] = self.chess_board[(0, 7)]
        # delete pieces to right so it has space to move back to where it started
        self.chess_board[(0, 6)] = None
        self.chess_board[(0, 7)] = None

        result = list(self.chess_board.valid_moves((0, 5)).keys())

        self.assertEqual(result, [(0, 6), (0, 7)])


class TestPieceExplodes(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_move_can_explode(self):
        self.chess_board[(1, 3)] = None
        self.chess_board[(0, 3)].moves[0]['capture_actions'] = ['explode']
        self.chess_board.move((0, 3), (6, 3))

        self.assertEqual(self.chess_board[(6, 3)].kind, 'queen')


class TestEnPassant(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_en_passant_king_side_black_captures(self):
        # move black pawn in range of white row for en pessante
        self.chess_board[(3, 3)] = self.chess_board[(6, 3)]
        self.chess_board[(6, 3)] = None

        # move white pawn forward by two
        self.chess_board.move((1, 4), (3, 4))

        # move en passant with black pawn
        self.chess_board.move((3, 3), (2, 4))

        self.assertEqual(self.chess_board[(2, 4)].kind, 'pawn')
        self.assertEqual(self.chess_board[(2, 4)].color, 'black')
        self.assertIsNone(self.chess_board[(3, 3)])
        self.assertIsNone(self.chess_board[(3, 4)])

    def test_en_passant_queen_side_black_captures(self):
        # move black pawn in range of white row for en pessante
        self.chess_board[(3, 3)] = self.chess_board[(6, 3)]
        self.chess_board[(6, 3)] = None

        # move white pawn forward by two
        self.chess_board.move((1, 2), (3, 2))

        # move en passant with black pawn
        self.chess_board.move((3, 3), (2, 2))

        self.assertEqual(self.chess_board[(2, 2)].kind, 'pawn')
        self.assertEqual(self.chess_board[(2, 2)].color, 'black')
        self.assertIsNone(self.chess_board[(3, 3)])
        self.assertIsNone(self.chess_board[(3, 2)])


class TestCastling(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    @parameterized.expand([
        ([], [], 'white', 'king', True, 'white king side castling is successful'),
        ([], [], 'white', 'queen', True, 'white queen side castling is successful'),
        ([], [], 'black', 'king', True, 'black king side castling is successful'),
        ([], [], 'black', 'queen', True, 'black queen side castling is successful'),
        ([(1, 4)], [{'start': (7, 3), 'end': (6, 4)}], 'white', 'king', False, "castling not allowed: white king in check by queen"),
        ([(6, 4)], [{'start': (0, 3), 'end': (1, 4)}], 'black', 'king', False, "castling not allowed: black king in check by queen"),
        ([(1, 5)], [{'start': (7, 3), 'end': (6, 5)}], 'white', 'king', False, "castling not allowed: first square threatened by queen"),
        ([(1, 6)], [{'start': (7, 3), 'end': (6, 6)}], 'white', 'king', False, "castling not allowed: second square threatened by queen"),
        ([(1, 7)], [{'start': (7, 3), 'end': (6, 7)}], 'white', 'king', True, "castling allowed: rook threatened by queen"),
        ([], [{'start': (7, 4), 'end': (1, 1)}], 'white', 'queen', False, "castling not allowed: second square queen side threatend by king"),
        ([], [{'start': (0, 4), 'end': (6, 1)}], 'black', 'queen', False, "castling not allowed: second square queen side threatend by king"),
        ([(1, 1), (1, 2)], [{'start': (6, 1), 'end': (2, 1)}], 'white', 'queen', True, "castling allowed: enemy pawns double move on first move should not block castling - makes sure prechecks are run"),
    ])
    def test_castling(self, delete_positions, setup_moves, color, side, successful, message):
        for position in delete_positions:
            self.chess_board[position] = None

        for move in setup_moves:
            self.chess_board[move['end']] = self.chess_board[move['start']]

        self.verify_castling(color, side, successful, message)

    def verify_castling(self, color, side, is_successful, message):
        row = 0
        if color == 'black':
            self.chess_board._toggle_current_player()
            row = 7

        start = (row, 4)

        if side == 'king':
            self.chess_board[(row, 5)] = None
            self.chess_board[(row, 6)] = None
            end = (row, 6)
            rook_start = (row, 7)
            rook_end = (row, 5)
        else:
            self.chess_board[(row, 1)] = None
            self.chess_board[(row, 2)] = None
            self.chess_board[(row, 3)] = None
            end = (row, 2)
            rook_start = (row, 0)
            rook_end = (row, 3)

        self.chess_board.move(start, end)

        if is_successful:
            self.assertEqual(self.chess_board[end].kind, 'king', message)
            self.assertEqual(self.chess_board[rook_end].kind, 'rook', message)

            self.assertIsNone(self.chess_board[start], message)
            self.assertIsNone(self.chess_board[rook_start], message)
        else:
            self.assertEqual(self.chess_board[start].kind, 'king', message)
            self.assertEqual(self.chess_board[rook_start].kind, 'rook', message)


class TestBecomesPieceCaptureAction(unittest.TestCase):

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_rook_becomes_pawn(self):
        # change pawn in front of rook to opposite color
        self.chess_board[(1, 7)].color = 'black'

        # add becomes_piece to rook's capture actions
        self.chess_board[(0, 7)].moves[0]['capture_actions'] = ['becomes_piece']

        # make sure a black pawn is where we think it is
        self.assertEqual(self.chess_board[(1, 7)].kind, "pawn")
        self.assertEqual(self.chess_board[(1, 7)].color, "black")
        self.assertNotEqual(self.chess_board[(0, 7)].color, "black")

        self.chess_board.move((0, 7), (1, 7))

        self.assertEqual(self.chess_board[(1, 7)].kind, "pawn")
        self.assertEqual(self.chess_board[(1, 7)].color, "white")


class TestPawnMoves(unittest.TestCase):
    """Chess movement unit tests."""

    def setUp(self):
        self.chess_board = ChessBoard()

    def test_pawn_can_move_forward(self):
        self.assertIsNone(self.chess_board[(2, 3)])
        ends = list(self.chess_board.valid_moves((1, 3)).keys())
        self.assertEqual(ends, [(2, 3), (3, 3)])

    def test_pawn_cant_move_forward_twice_if_not_first_move(self):
        self.assertIsNone(self.chess_board[(2, 3)])
        self.assertIsNone(self.chess_board[(3, 3)])
        self.assertIsNone(self.chess_board[(4, 3)])
        self.chess_board.move((1, 3), (2, 3))
        ends = list(self.chess_board.valid_moves((2, 3)).keys())
        self.assertEqual(ends, [(3, 3)])

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
        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNone(self.chess_board[(2, 1)])
        self.assertIsNone(self.chess_board[(1, 1)])
        self.chess_board.first()
        self.assertIsNotNone(self.chess_board[(1, 1)])
        self.assertIsNone(self.chess_board[(2, 1)])
        self.assertIsNone(self.chess_board[(3, 1)])

    def test_next(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))

        self.assertIsNone(self.chess_board[(1, 1)])
        self.assertIsNone(self.chess_board[(6, 2)])

        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNotNone(self.chess_board[(4, 2)])

        self.chess_board.first()

        self.assertIsNotNone(self.chess_board[(1, 1)])
        self.assertIsNotNone(self.chess_board[(6, 2)])

        self.chess_board.next()  # 1,1 -> 2, 1

        self.assertIsNone(self.chess_board[(1, 1)])
        self.assertIsNotNone(self.chess_board[(2, 1)])

        self.chess_board.next()  # 6,2 -> 5, 2

        self.assertIsNone(self.chess_board[(6, 2)])
        self.assertIsNotNone(self.chess_board[(5, 2)])

        self.chess_board.next()  # 2, 1 -> 3, 1

        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNone(self.chess_board[(2, 1)])

        self.chess_board.next()  # 5, 2 -> 4, 2

        self.assertIsNone(self.chess_board[(5, 2)])
        self.assertIsNotNone(self.chess_board[(4, 2)])

        self.chess_board.next()
        self.chess_board.next()
        self.chess_board.next()

        self.assertIsNone(self.chess_board[(1, 1)])
        self.assertIsNone(self.chess_board[(6, 2)])

        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNotNone(self.chess_board[(4, 2)])

    def test_previous(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))
        self.assertIsNotNone(self.chess_board[(4, 2)])
        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNone(self.chess_board[(5, 2)])
        self.assertIsNone(self.chess_board[(2, 1)])

        self.chess_board.previous()

        self.assertIsNone(self.chess_board[(4, 2)])
        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNotNone(self.chess_board[(5, 2)])
        self.assertIsNone(self.chess_board[(2, 1)])

        self.chess_board.previous()

        self.assertIsNone(self.chess_board[(4, 2)])
        self.assertIsNone(self.chess_board[(3, 1)])
        self.assertIsNotNone(self.chess_board[(5, 2)])
        self.assertIsNotNone(self.chess_board[(2, 1)])

        self.chess_board.previous()
        self.chess_board.previous()
        self.chess_board.previous()
        self.chess_board.previous()
        self.chess_board.previous()

        self.chess_board.next()

        self.assertIsNotNone(self.chess_board[(2, 1)])
        self.assertIsNone(self.chess_board[(1, 1)])

    def test_can_undo_and_redo_last_move(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))
        self.assertIsNotNone(self.chess_board[(4, 2)])
        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNone(self.chess_board[(5, 2)])
        self.assertIsNone(self.chess_board[(2, 1)])

        self.chess_board.previous()

        self.assertIsNone(self.chess_board[(4, 2)])
        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNotNone(self.chess_board[(5, 2)])
        self.assertIsNone(self.chess_board[(2, 1)])

        self.chess_board.next()

        self.assertIsNotNone(self.chess_board[(4, 2)])
        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNone(self.chess_board[(5, 2)])
        self.assertIsNone(self.chess_board[(2, 1)])

    def test_export_includes_history(self):
        self.chess_board.move((1, 1), (2, 1))
        self.chess_board.move((6, 2), (5, 2))
        self.chess_board.move((2, 1), (3, 1))
        self.chess_board.move((5, 2), (4, 2))
        self.assertIsNotNone(self.chess_board[(4, 2)])
        self.assertIsNotNone(self.chess_board[(3, 1)])
        self.assertIsNone(self.chess_board[(5, 2)])
        self.assertIsNone(self.chess_board[(2, 1)])

        export = self.chess_board.export()
        new_board = ChessBoard(export)

        self.assertEqual(len(new_board._history), 4)
        self.assertEqual(new_board._history._index, 3)

        self.assertIsNotNone(new_board[(4, 2)])
        self.assertIsNotNone(new_board[(3, 1)])
        self.assertIsNone(new_board[(5, 2)])
        self.assertIsNone(new_board[(2, 1)])

        new_board.previous()

        self.assertIsNone(new_board[(4, 2)])
        self.assertIsNotNone(new_board[(3, 1)])
        self.assertIsNotNone(new_board[(5, 2)])
        self.assertIsNone(new_board[(2, 1)])

        new_board.previous()

        self.assertIsNone(new_board[(4, 2)])
        self.assertIsNone(new_board[(3, 1)])
        self.assertIsNotNone(new_board[(5, 2)])
        self.assertIsNotNone(new_board[(2, 1)])

    def test_castling_is_undoable_when_navigating_history(self):
        self.chess_board[(0, 5)] = None
        self.chess_board[(0, 6)] = None

        self.chess_board.move((0, 4), (0, 6))

        self.assertIsNone(self.chess_board[(0, 7)])
        self.assertIsNone(self.chess_board[(0, 4)])

        self.chess_board.previous()

        self.assertIsNotNone(self.chess_board[(0, 7)])
        self.assertIsNotNone(self.chess_board[(0, 4)])
        self.assertIsNone(self.chess_board[(0, 5)])
        self.assertIsNone(self.chess_board[(0, 6)])

        self.chess_board.next()

        self.assertIsNone(self.chess_board[(0, 7)])
        self.assertIsNone(self.chess_board[(0, 4)])
        self.assertIsNotNone(self.chess_board[(0, 5)])
        self.assertIsNotNone(self.chess_board[(0, 6)])


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
