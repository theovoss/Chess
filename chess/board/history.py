import copy


class History():

    def __init__(self, json=None):
        self._index = -1
        self._history = []
        self._initial_board = {}
        if json:
            if 'history' in json:
                self._history = json['history']
            if 'initial_board' in json:
                self._initial_board = json['initial_board']
            if 'index' in json:
                self._index = json['index']

    def __len__(self):
        return len(self._history)

    @property
    def initial_board(self):
        return self._initial_board

    @property
    def json(self):
        return {'history': self._history, 'initial_board': self._initial_board, 'index': self._index}

    def add(self, obj):
        if self._index != len(self) - 1:
            # history has been undone, so unspool history
            self._history = self._history[:self._index + 1]
        self._history.append(obj)
        self._index += 1

    def all(self):
        return copy.deepcopy(self._history)

    def previous(self):
        record = self._history[self._index]

        if self._index < 0:
            return None

        self._index -= 1
        return record

    def first(self):
        self._index = -1

    def next(self):
        if self._index >= len(self) - 1:
            return None
        self._index += 1
        record = self._history[self._index]
        return record

    @staticmethod
    def construct_history_object(start, end, piece, captures=None):
        obj = {
            'start': start,
            'end': end,
            'piece': {
                'name': piece.kind,
                'color': piece.color,
                'moves': piece.moves
            }
        }
        if captures:
            obj['captures'] = {}
            for location, captured in captures.items():
                obj['captures'][location] = {
                    'name': captured.kind,
                    'color': captured.color,
                    'moves': captured.moves
                }
        return obj
