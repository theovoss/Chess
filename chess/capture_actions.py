# pylint: disable=W0613
# allow unused variables so all capture action functions can have same parameter definition


def replace(board, start, end):
    board[end] = board[start]
    board[start] = None


def becomes_piece(board, start, end):
    if not _is_capturing(board, end):
        replace(board, start, end)
        return

    board[end].color = board[start].color
    board[end].move_count = board[start].move_count
    board[start] = None


def explode(board, start, end):
    if not _is_capturing(board, end):
        replace(board, start, end)
        return

    for place in board.get_surrounding_locations(end):
        if place[0] < 0 or place[1] < 0:
            continue
        board[place] = None
    board[end] = None


def increment_move_count(board, start, end):
    if _has_piece(board, end):
        board[end].move_count += 1


def _has_piece(board, location):
    return board[location] is not None


def _is_capturing(board, location):
    return board[location] is not None
