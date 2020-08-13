# pylint: disable=W0212
"""Chess History unit test module."""

import unittest

from chess.board.history import History
from chess.piece.piece import Piece


class TestHistory(unittest.TestCase):

    def setUp(self):
        self.history = History()

    def test_add(self):
        self.history.add({})
        self.assertEqual(len(self.history), 1)

    def test_get_full_history(self):
        for i in range(5):
            self.history.add({str(i): i})
        actual = self.history.all()
        self.assertEqual(len(actual), 5)
        self.assertEqual(actual[0], {"0": 0})
        self.assertEqual(actual[4], {"4": 4})

    def test_previous(self):
        for i in range(5):
            self.history.add({str(i): i})
        previous = self.history.previous()
        self.assertEqual({'4': 4}, previous)

        previous = self.history.previous()
        self.assertEqual({'3': 3}, previous)

        # can go back to beginning of history
        self.history.previous()
        self.history.previous()
        previous = self.history.previous()
        self.assertEqual({'0': 0}, previous)

        # doesn't go beyond initial history state
        previous = self.history.previous()
        self.assertEqual(None, previous)
        self.assertEqual(self.history._index, -1)

    def test_add_after_previous(self):
        for i in range(5):
            self.history.add({str(i): i})
        self.history.previous()
        previous = self.history.previous()
        self.assertEqual({'3': 3}, previous)
        self.assertEqual(5, len(self.history))
        self.assertEqual(2, self.history._index)
        self.history.add({"sitting": "throne"})
        self.assertEqual(4, len(self.history))

    def test_first(self):
        for i in range(5):
            self.history.add({str(i): i})
        self.history.first()
        self.assertEqual(-1, self.history._index)
        self.assertEqual(5, len(self.history))

    def test_next(self):
        for i in range(5):
            self.history.add({str(i): i})
        self.history.first()
        item = self.history.next()
        self.assertEqual({'0': 0}, item)
        item = self.history.next()
        self.assertEqual({'1': 1}, item)

        # beyond end of list
        self.history.next()
        self.history.next()
        self.history.next()
        item = self.history.next()
        self.assertEqual(None, item)
        self.assertEqual(4, self.history._index)

    def test_json(self):
        for i in range(3):
            self.history.add({str(i): i})
        data = self.history.json
        self.assertEqual(data, [{'0': 0}, {'1': 1}, {'2': 2}])

    def test_construct_history_object(self):
        start = [0, 0]
        end = [4, 5]
        piece = Piece("name", "red", [{"directions": ["move"]}])
        captures = {(5, 5): piece}
        record = History.construct_history_object(start, end, piece, captures)
        self.assertEqual(piece.moves, [{'directions': ['move']}])
        self.assertEqual(record, {
            'start': start,
            'end': end,
            'piece': {'name': 'name', 'color': 'red', 'moves': [{'directions': ['move']}]},
            'captures': {(5, 5): {'name': 'name', 'color': 'red', 'moves': [{'directions': ['move']}]}}})
