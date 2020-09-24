import copy
from chess.move.calculator import Calculator
from chess.move.pathfinder import PathFinder
from chess.move_pipeline import endgame
from chess.move_pipeline.move_pipeline_accessor import MovePipelineAccessor
from chess.move_pipeline import movement


class EndgameAnalyzer():
    def __init__(self):
        self._calculator = Calculator()

    def _get_check_conditions(self, board):
        if 'check' in board.end_game:
            return MovePipelineAccessor.get_attributes(endgame, board.end_game['check']['conditions'])
        else:
            return []

    def is_pinned(self, board, color, location):
        assert board[location] is not None, "Board location {} should have a piece to calculate pinning but doesn't".format(location)

        if board[location].kind != board.get_endgame_piece_name():
            new_board = copy.deepcopy(board)
            new_board[location] = None
            assert board[location] is not None, "Deep copy didn't work"
            paths = self.get_check_paths(new_board, color)
            for path in paths:
                if location in path:
                    return True
            return False
        # moving endgame piece, so by definition it can't be pinning the endgame piece
        return False

    def get_pinned_path(self, board, color, location):
        assert board[location] is not None, "Board location {} should have a piece to calculate pinning but doesn't".format(location)
        new_board = copy.deepcopy(board)
        new_board[location] = None

        paths = self.get_check_paths(new_board, color)

        for path in paths:
            if location in path:
                return path
        return []

    def is_check(self, board, color):
        # TODO: pass in endgame piece location too?
        check_conditions = self._get_check_conditions(board)
        results = [cond(board, self._calculator, color) for cond in check_conditions]
        return any(results)

    def get_check_paths(self, board, color):
        endgame_piece_location = board.get_endgame_piece_location(color)
        threatened_by_color = 'white'
        if color == threatened_by_color:
            threatened_by_color = 'black'
        threat_locations = self._calculator.get_threatening_piece_location(board, endgame_piece_location, threatened_by_color)

        valid_threat_paths = []
        for threat_location in threat_locations:
            threat_path = PathFinder.get_path_between(board, threat_location, endgame_piece_location)

            valid_moves = self._calculator.get_destinations(board, threat_location)

            valid_threat_path = [move for move in valid_moves if move in threat_path]
            valid_threat_path.append(threat_location)
            valid_threat_paths.append(valid_threat_path)
        return valid_threat_paths

    def is_checkmate(self, board, color):
        # if empty
        if not self._calculator.get_destinations(board, board.get_endgame_piece_location(color)):
            # and nothing can block. Does Calculator check that??
            pass
        pass
