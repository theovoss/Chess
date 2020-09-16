import copy
from chess.move_pipeline import endgame
from chess.move_pipeline.move_pipeline_accessor import MovePipelineAccessor


class EndgameAnalyzer():
    def is_pinned(self, board, calculator, color, location):
        new_board = copy.deepcopy(board)
        new_board[location] = None
        return self.is_check(new_board, calculator, color)

    def get_pinned_path(self, calculator, color, start):
        # calculator.get_
        # PathFinder.get_path_between
        return []

    def is_check(self, board, calculator, color):
        # TODO: pass in endgame piece location too?
        check_conditions = MovePipelineAccessor.get_attributes(endgame, board.end_game['check'])
        results = [cond(board, calculator, color) for cond in check_conditions]
        return any(results)

    def get_check_path(self, board, calculator, color):
        # return calculator.get_threatened_path(_get_endgame_piece_location)
        pass

    def is_checkmate(self, board, calculator, color):
        # if empty
        if not calculator.get_destinations(board, self._get_endgame_piece_location(board, color)):
            # and nothing can block. Does Calculator check that??
            pass
        pass

    def _get_endgame_piece_location(self, board, color):
        piece_name = board.end_game['piece']
        for location in board:
            if board[location] and board[location].color == color and board[location].kind == piece_name:
                return location
