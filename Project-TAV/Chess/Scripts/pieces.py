"""
Toutes les fonctions en rapport avec le mouvement des pièces.
"""
import board

class Piece:
    class Pawn:
        def __init__(self, color):
            self.color = color
            self.opposite_color = "w" if self.color == "b" else "b"

        def legal_moves(self, gestionary, rank, col):
            legal_moves = []
            coeff = -1 if self.color == "w" else 1

            if not board.color_and_occupied_square(gestionary, rank+1*coeff, col):
                legal_moves.append((rank+1*coeff, col))

                if rank == (0+1*coeff)%7 and not board.color_and_occupied_square(gestionary, rank+2*coeff, col):
                    if not gestionary.chess_game.in_check(self.color):
                        legal_moves.append((rank+2*coeff, col))

            if 0 < col and board.color_and_occupied_square(gestionary, rank+1*coeff, col-1) == self.opposite_color:
                legal_moves.append((rank+1*coeff, col-1))

            if col < 7 and board.color_and_occupied_square(gestionary, rank+1*coeff, col+1) == self.opposite_color:
                legal_moves.append((rank+1*coeff, col+1))


            # en passant
            return legal_moves

    class Rook:
        def __init__(self, color):
            self.color = color
            self.opposite_color = "w" if self.color == "b" else "b"

        def legal_moves(self, gestionary, rank, col):
            legal_moves = []
            dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            for direction in dir:
                col_dir = col
                rank_dir = rank
                while 0 <= col_dir <= 7 and 0 <= rank_dir <= 7:
                    rank_dir += direction[0]
                    col_dir += direction[1]

                    if abs(col_dir-3.5) > 3.5 or abs(rank_dir-3.5) > 3.5:
                        break

                    if not board.color_and_occupied_square(gestionary, rank_dir, col_dir):
                        legal_moves.append((rank_dir, col_dir))

                    else:
                        if board.color_and_occupied_square(gestionary, rank_dir, col_dir) == self.opposite_color:
                            legal_moves.append((rank_dir, col_dir))
                        break

            return legal_moves

    class Knight:
        def __init__(self, color):
            self.color = color
            self.opposite_color = "w" if self.color == "b" else "b"

        def legal_moves(self, gestionary, rank, col):
            legal_moves = []
            dir = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

            for direction in dir:
                rank_dir = rank+direction[0]
                col_dir = col+direction[1]

                if 0 <= rank_dir <= 7 and 0 <= col_dir <= 7:
                    if board.color_and_occupied_square(gestionary, rank_dir, col_dir) != self.color:
                        legal_moves.append((rank_dir, col_dir))

            return legal_moves

    class Bishop:
        def __init__(self, color):
            self.color = color
            self.opposite_color = "w" if self.color == "b" else "b"

        def legal_moves(self, gestionary, rank, col):
            legal_moves = []
            dir = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

            for direction in dir:
                col_dir = col
                rank_dir = rank
                while 0 <= col <= 7 and 0 <= rank <= 7:
                    rank_dir += direction[0]
                    col_dir += direction[1]

                    if abs(col_dir-3.5) > 3.5 or abs(rank_dir-3.5) > 3.5:
                        break

                    if not board.color_and_occupied_square(gestionary, rank_dir, col_dir):
                        legal_moves.append((rank_dir, col_dir))

                    else:
                        if board.color_and_occupied_square(gestionary, rank_dir, col_dir) == self.opposite_color:
                            legal_moves.append((rank_dir, col_dir))
                        break

            return legal_moves

    class King:
        def __init__(self, color):
            self.color = color
            self.opposite_color = "w" if self.color == "b" else "b"

        def legal_moves(self, gestionary, rank, col):
            legal_moves = []
            dir = [(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0), (0, 1), (0, -1)]

            for direction in dir:
                col_dir = col + direction[1]
                rank_dir = rank + direction[0]

                if 0 <= col_dir <= 7 and 0 <= rank_dir <= 7:
                    if board.color_and_occupied_square(gestionary, rank_dir, col_dir) != self.color:
                        legal_moves.append((rank_dir, col_dir))


            # short castle
            # long castle

            return legal_moves

    class Queen:
        def __init__(self, color):
            self.color = color

        def legal_moves(self, gestionary, rank, col):
            rook_moves = Piece.Rook(self.color).legal_moves(gestionary, rank, col)
            bishop_moves = Piece.Bishop(self.color).legal_moves(gestionary, rank, col)

            legal_moves = []

            for move in rook_moves:
                legal_moves.append(move)
            for move in bishop_moves:
                legal_moves.append(move)

            return legal_moves