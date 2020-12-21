from chess.piece.directions import convert_shorthand_directions


class Piece:

    def __init__(self, piece_name, piece_color, moves):
        self.kind = piece_name
        self.color = piece_color
        self.move_count = 0
        self.moves = Piece._convert_moves(moves)
        self.promote_me_daddy = False

    def __str__(self):
        return "{} {}".format(self.color, self.kind)

    def __repr__(self):
        character = self.kind[0]
        if self.kind == "knight":
            character = 'n'
        if self.color == "white":
            character = character.upper()
        return character

    @property
    def opposite_color(self):
        opposite = "white"
        if opposite == self.color:
            opposite = "black"
        return opposite

    @staticmethod
    def _convert_moves(moves):
        converted_moves = []
        for move in moves:
            converted_directions = []
            for direction in move['directions']:
                if isinstance(direction, str):
                    converted_directions += convert_shorthand_directions(direction)
                else:
                    converted_directions.append(direction)
            converted_move = move
            converted_move["directions"] = converted_directions
            converted_moves.append(converted_move)
        return converted_moves
