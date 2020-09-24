def increment_move_count(board, end):
    if board[end]:
        board[end].move_count += 1
    else:
        print("trying to increment move count of location {}, but it's empty".format(end))


def doesnt_survive(board, end):
    board[end] = None


def promotable(board, end):
    if end[0] == 7 or end[0] == 0:
        board[end].promote_me_daddy = True
    else:
        board[end].promote_me_daddy = False
