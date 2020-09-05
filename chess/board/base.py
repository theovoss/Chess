class Board:

    def __init__(self, num_rows, num_columns):
        self._board = dict()
        for row in range(num_rows):
            for column in range(num_columns):
                self._board[(row, column)] = None

        self.rows = num_rows
        self.columns = num_columns

    @property
    def board(self):
        return self._board

    @staticmethod
    def get_surrounding_locations(location):
        return [
            (location[0] + 1, location[1]),
            (location[0] - 1, location[1]),
            (location[0] + 1, location[1] + 1),
            (location[0] - 1, location[1] + 1),
            (location[0] + 1, location[1] - 1),
            (location[0] - 1, location[1] - 1),
            (location[0], location[1] + 1),
            (location[0], location[1] - 1),
        ]

    def __getitem__(self, key):
        return self.board.get(key)

    def __setitem__(self, key, value):
        self.board[key] = value

    def __iter__(self):
        for key in self.board:
            yield key

    def __len__(self):
        return len(self.board)

    def clear_board(self):
        for location in self:
            self[location] = None
