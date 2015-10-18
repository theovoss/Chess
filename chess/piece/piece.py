

class Piece:

    def __init__(self, piece_name, piece_color, moves):
        self.kind = piece_name
        self.color = piece_color
        self.moves = moves
        self.move_count = 0

    def __str__(self):
        return "{} {}".format(self.color, self.kind)

    def __repr__(self):
        character = self.kind[0]
        if self.kind == "knight":
            character = 'n'
        if self.color == "white":
            character = character.upper()
        return character
