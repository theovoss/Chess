
def endgame_piece_is_threatened(board, calculator, color):
    # TODO: have to pass in ignore location too...
    location = board.get_endgame_piece_location(color)
    if not location:
        return False

    return calculator.is_threatened(board, [location], board[location].opposite_color)
