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
        history = copy.deepcopy(self._history)
        if self._index >= 0 and self._index < len(self._history):
            history[self._index]['current'] = True
        return history

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
    def construct_history_object(start, end, piece, captures=None, side_effects=None):
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
            obj['captures'] = captures
        if side_effects:
            obj['side_effects'] = side_effects
        return obj

    @staticmethod
    def construct_capture_obj(captureds):
        captures = []
        for location, piece in captureds.items():
            captures.append({'location': location, 'name': piece.kind, 'color': piece.color, 'moves': piece.moves})
        return captures

    @staticmethod
    def construct_side_effect(method, **kwargs):
        start = kwargs['start']
        end = kwargs['end']
        if method == 'move':
            return [{
                'method': 'move',
                'start': start,
                'end': end
            }]
        return []
