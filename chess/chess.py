from .board import ChessBoard


class Chess:

    def __init__(self):
        self._board = ChessBoard()

    @property
    def board(self):
        return self._get_board()

    def _get_board(self):
        return self._board._board

    def move(self, start_location, end_location):
        self._board.move(start_location, end_location)
        return True
