from .board import ChessBoard


class Chess:

    def __init__(self, existing_board=None):
        self._board = ChessBoard(existing_board)

    # Methods to play chess
    @property
    def board(self):
        return self._get_board()

    def _get_board(self):
        return self._board.board

    def export(self):
        return self._board.export()

    def move(self, start_location, end_location):
        start = self.convert_to_internal_indexes(start_location)
        end = self.convert_to_internal_indexes(end_location)
        return self._board.move(start, end)

    def destinations(self, start_location):
        return list(self._board.valid_moves(start_location).keys())

    def promote(self, location, new_piece_name):
        self._board.promote(location, new_piece_name)

    def get_all_piece_names(self):
        return self._board.get_all_piece_names()

    # Methods to navigate history
    def previous(self):
        self._board.previous()

    def next(self):
        self._board.next()

    def first(self):
        self._board.first()

    def get_history(self):
        return self._board.get_history()

    @staticmethod
    def convert_to_internal_indexes(location):
        if isinstance(location, str):
            assert len(location) == 2
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            col = alphabet.index(location[0].lower())
            row = int(location[1]) - 1
            key = (row, col)
            return key
        return location
