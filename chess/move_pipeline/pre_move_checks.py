def has_not_moved(board, locations, history):
    for location in locations:
        if board[location] and board[location].move_count != 0:
            return False
    return True


def has_moved_once(board, locations, history):
    for location in locations:
        if board[location] is None or board[location].move_count != 1:
            return False
    return True


def is_empty(board, locations, history):
    for location in locations:
        if board[location] is not None:
            return False
    return True


def is_not_empty(board, locations, history):
    return not is_empty(board, locations, history)


def is_not_threatened(board, locations, history):
    return True


def moved_last(board, locations, history):
    if history.all() and history.all()[-1]['end'] in locations:
        return True
    return False
