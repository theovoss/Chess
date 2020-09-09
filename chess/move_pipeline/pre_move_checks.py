def has_not_moved(board, locations, history, color):
    for location in locations:
        if board[location] and board[location].move_count != 0:
            return False
    return True


def has_moved_once(board, locations, history, color):
    for location in locations:
        if board[location] is None or board[location].move_count != 1:
            return False
    return True


def is_empty(board, locations, history, color):
    for location in locations:
        if board[location] is not None:
            return False
    return True


def is_not_empty(board, locations, history, color):
    return not is_empty(board, locations, history, color)


def moved_last(board, locations, history, color):
    if history.all() and history.all()[-1]['end'] in locations:
        return True
    return False
