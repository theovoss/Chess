import copy


class History():

    def __init__(self):
        self._index = -1
        self._history = []

    def __len__(self):
        return len(self._history)

    @property
    def json(self):
        return self._history

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
    def construct_history_object(start, end):
        # TODO: add captures
        return {
            'start': start,
            'end': end
        }
