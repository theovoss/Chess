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
