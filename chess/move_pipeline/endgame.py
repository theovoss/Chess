
def endgame_piece_is_threatened(board, calculator, color):
    # TODO: have to pass in ignore location too...
    location = board.get_endgame_piece_location(color)
    if not location:
        return False
    other_color = "black"
    if color == "black":
        other_color = "white"
    return calculator.is_threatened(board, [location], other_color)
