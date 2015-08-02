_pawn = "pawn"
_knight = "knight"
_rook = "rook"
_bishop = "bishop"
_queen = "queen"
_king = "king"


class Piece:

    def __init__(self, piece_name, piece_color):
        self.kind = piece_name
        self.color = piece_color

    def __str__(self):
        return "{} {}".format(self.color, self.kind)

    def get_valid_moves(self):
        return None

    def get_attack_moves(self):
        return None


class Pawn(Piece):

    def __init__(self, piece_color):
        Piece.__init__(self, _pawn, piece_color)

    def get_valid_moves(self):
        return [(1, 0)]

    def get_attack_moves(self):
        return [(1, 1)]


class Knight(Piece):

    def __init__(self, piece_color):
        Piece.__init__(self, _knight, piece_color)


class Rook(Piece):

    def __init__(self, piece_color):
        Piece.__init__(self, _rook, piece_color)


class Bishop(Piece):

    def __init__(self, piece_color):
        Piece.__init__(self, _bishop, piece_color)


class Queen(Piece):

    def __init__(self, piece_color):
        Piece.__init__(self, _queen, piece_color)


class King(Piece):

    def __init__(self, piece_color):
        Piece.__init__(self, _king, piece_color)
