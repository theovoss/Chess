
def endgame_piece_is_threatened(board, calculator, color):
    # TODO: have to pass in ignore location too...
    location = board.get_endgame_piece_location()
    return calculator.is_threatened(board, [location], color)
