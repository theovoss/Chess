from .board import ChessBoard


class Chess:

    def __init__(self, existing_board=None):
        self._board = ChessBoard(existing_board)

    @property
    def board(self):
        return self._get_board()

    def _get_board(self):
        return self._board.board

    def generate_fen(self):
        return self._board.generate_fen()

    def export(self):
        return self._board.export()

    def move(self, start_location, end_location):
        start = self._convert_location_to_board_indices(start_location)
        end = self._convert_location_to_board_indices(end_location)
        return self._board.move(start, end)

    def destinations(self, start_location):
        return self._board.end_locations_for_piece_at_location(start_location)

    @staticmethod
    def _convert_location_to_board_indices(location):
        if isinstance(location, str):
            assert len(location) == 2
            alphabet = "abcdefghijklmnopqrstuvwxyz"
            col = alphabet.index(location[0].lower())
            row = int(location[1]) - 1
            key = (row, col)
            return key
        return location
