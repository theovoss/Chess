

class Piece:

    def __init__(self, piece_name, piece_color, moves):
        self.kind = piece_name
        self.color = piece_color
        self.moves = moves

    def __str__(self):
        return "{} {}".format(self.color, self.kind)

    def set_location(self, location):
        self.location = location
