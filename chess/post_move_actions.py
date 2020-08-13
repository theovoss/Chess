def increment_move_count(board, end):
    board[end].move_count += 1


def doesnt_survive(board, end):
    board[end] = None
