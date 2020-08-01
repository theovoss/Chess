shorthands = {
    'vertical': [[1, 0], [-1, 0]],
    'horizontal': [[0, 1], [0, -1]],
    'diagonal': [[-1, -1], [1, 1], [-1, 1], [1, -1]],
    'L': [[2, 1], [2, -1], [1, 2], [1, -2], [-1, 2], [-1, -2], [-2, 1], [-2, -1]],
    'extended L': [[3, 1], [3, -1], [1, 3], [1, -3], [-1, 3], [-1, -3], [-3, 1], [-3, -1]]
}


def convert_shorthand_directions(shorthand):
    if isinstance(shorthand, str) and shorthand in shorthands:
        return shorthands[shorthand]
    return shorthand


def get_direction_shorthands():
    return shorthands.keys()
