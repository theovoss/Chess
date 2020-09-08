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
            # TODO: add this correct color moving check to a precondition and wrap in is_valid_move
            if board.current_players_turn == 'w':
                if board[start].color == 'black':
                    print('black trying to move, but whites turn')
                    return False
            else:
                if board[start].color == 'white':
                    print('white trying to move, but blacks turn')
                    return False

            board._toggle_current_player()
            print("is valid move")

            self._move_piece(board, start, end, valid_moves[end], history, save)
            return True
        print('is not valid move start: ' + str(start) + " end: " + str(end))
        return False

    def _move_piece(self, board, start, end, move, history, save=True):
        piece = board[start]

        post_actions = json_helper.get_post_move_actions(move)
        effects = json_helper.get_side_effects(move)

        # Move
        captures = self._move_and_capture(board, start, end, move)

        # Post Move
        for action in post_actions:
            action(board, end)

        # Side Effects
        history_side_effects = []
        for effect in effects:
            method = getattr(side_effects, effect['method'])
            if method:
                history_side_effects += method(board, start, **effect['kwargs'])

        # Save to history
        if save:
            history.add(History.construct_history_object(start, end, piece, captures, history_side_effects))

    def _move_and_capture(self, board, start, end, move):
        actions = json_helper.get_capture_actions(move)
        additional_captures = json_helper.get_additional_captures(board, start, move)
        captures = []
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

        board[end] = board[start]
        board[start] = None

        return captures
