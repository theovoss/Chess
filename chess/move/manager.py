from chess.board.history import History
from chess.board import json_helper
from chess.move_pipeline import side_effects


class Manager():
    def promote(self, board, location, new_piece_name):
        if board[location].promote_me_daddy:
            color = board[location].color
            promoted = [piece for piece in board.pieces if piece.kind == new_piece_name][0]
            promoted.color = color

            board[location] = promoted

    def move(self, board, start, end, history, save=True):
        valid_moves = board.valid_moves(start)

        if end in valid_moves:
            if board[start].color != board.current_players_turn:
                print("{} tyring to move, but {}'s turn".format(board[start].color, board.current_players_turn))
                return False

            board._toggle_current_player()

            self._move_piece(board, start, end, valid_moves[end], history, save)

            self._analyze_board_for_endgame(board)

            return True
        print('is not valid move start: ' + str(start) + " end: " + str(end))
        return False

    def _analyze_board_for_endgame(self, board):
        pass

    def _move_piece(self, board, start, end, move, history, save=True):
        piece = board[start]

        # Calculate any captures
        captures = self._calculate_captures(board, start, end, move)

        # Actually move from start to end
        self._move(board, start, end)

        # Post Move
        self._run_post_move_actions(board, end, move)

        # Side Effects
        effects = self._run_side_effects(board, start, end, move)

        # Save to history
        if save:
            history.add(History.construct_history_object(start, end, piece, captures, effects))

    def _calculate_captures(self, board, start, end, move):
        captures = []

        actions = json_helper.get_capture_actions(move)
        additional_captures = json_helper.get_additional_captures(board, start, move)

        if board[end] is not None:
            # capturing piece!
            for action in actions:
                captureds = action(board, start, end)
                captures += History.construct_capture_obj(captureds)

        if additional_captures:
            captures += History.construct_capture_obj(additional_captures)

        for capture in captures:
            capture_location = capture['location']
            board[capture_location] = None

        return captures

    def _move(self, board, start, end):
        board[end] = board[start]
        board[start] = None

    def _run_post_move_actions(self, board, end, move):
        for action in json_helper.get_post_move_actions(move):
            action(board, end)

    def _run_side_effects(self, board, start, end, move):
        history_side_effects = []
        for effect in json_helper.get_side_effects(move):
            method = getattr(side_effects, effect['method'])
            if method:
                history_side_effects += method(board, start, **effect['kwargs'])
        return history_side_effects
