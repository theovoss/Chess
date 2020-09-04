import operator as _operator


def add_unit_direction(start, unit_direction):
    return tuple(map(_operator.add, start, unit_direction))
