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


def attack_condition(end_location, board):
    if board[end_location] is not None:
        return True
    return False


def default_condition(start_location, end_location, board):
    return True


def has_not_moved_condition(start_location, end_location, board):
    return True


def move_away_from_starting_side_condition(start_location, end_location, board):
    return True


def en_passant_condition(start_location, end_location, board):
    return True


class Pawn(Piece):

    def __init__(self, piece_color):
        Piece.__init__(self, _pawn, piece_color)

    def validate_moves(self):
        move_forward = dict(move=(1, 0), conditions=[move_away_from_starting_side_condition])
        move_forward_two = dict(move=(2, 0), conditions=[default_condition, has_not_moved_condition, move_away_from_starting_side_condition])
        attack = dict(move=(1, 1), conditions=[attack_condition, en_passant_condition, move_away_from_starting_side_condition])
        return [move_forward, move_forward_two, attack]


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
