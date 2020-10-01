import copy
from dataclasses import dataclass
from typing import Any


@dataclass
class ConditionArgs():
    calculator: Any
    board: dict
    directions: list
    start: tuple
    ends: list
    player_direction: tuple

    @staticmethod
    def generate(board, move, start, paths, player_direction):
        return ConditionArgs(board._calculator, board, move.get('directions'), start, copy.deepcopy(paths), player_direction)
