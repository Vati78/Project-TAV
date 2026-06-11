"""
Toutes les fonctions en rapport avec les pièces.
"""
import const

def is_valid_square(gestionary, square, color):
    # if the number gets too big or too low
    if square >> 64 or not square:
        is_valid = False
        stop = True

        return is_valid, stop

    # if the square is occupied by a friendly piece
    if gestionary.chess_game.players[color].pieces_total & square:
        is_valid = False
        stop = True

        return is_valid, stop

    is_valid = True

    # if it's occupied by an enemy piece
    if gestionary.chess_game.players[~color].pieces_total & square:
        stop = True
    else:
        stop = False

    return is_valid, stop

def get_type(index, color):
    if index == 0:
        return Piece().Pawn(color)
    elif index == 1:
        return Piece().Knight(color)
    elif index == 2:
        return Piece().Bishop(color)
    elif index == 3:
        return Piece().Rook(color)
    elif index == 4:
        return Piece().Queen(color)
    elif index == 5:
        return Piece().King(color)


class Piece:
    class Pawn:
        def __init__(self, color):
            self.color = color
            self.opposite_color = - ~self.color & 1

        def legal_moves(self, gestionary, square_i):
            legal_moves = 0

            # white pawns
            if not self.color:
                # if the pawn is not on the last rank
                if square_i >> 8:
                    # forward (if there is no piece in front of it)
                    square = square_i >> 8
                    if not square & gestionary.chess_game.total:
                        legal_moves |= square

                        # if it is on its starting square and there is no piece in front of it
                        square >>= 8
                        if square_i & (const.RANK << 48) and not square & gestionary.chess_game.total:
                            legal_moves |= square

                    # capture right (if it is not on the h file and there is a piece to capture)
                    square = square_i >> 7
                    if const.NOT_H_FILE & square_i and square & gestionary.chess_game.players[self.opposite_color].pieces_total:
                        legal_moves |= square

                    # capture left (if it is not on the a file and there is a piece to capture)
                    square = square_i >> 9
                    if const.NOT_A_FILE & square_i and square & gestionary.chess_game.players[self.opposite_color].pieces_total:
                        legal_moves |= square

                    # en passant

            # black pawns
            else:
                # if the pawn is not on the first rank
                if not square_i >> 56:
                    # forward (if there is no piece in front of it)
                    square = square_i << 8
                    if not square & gestionary.chess_game.total:
                        legal_moves |= square

                        # if it is on its starting square and there is no piece in front of it
                        square <<= 8
                        if square_i & (const.RANK << 8) and not square & gestionary.chess_game.total:
                            legal_moves |= square

                    # capture right (if it is not on the h file and there is a piece to capture)
                    square = square_i << 9
                    if const.NOT_H_FILE & square_i and square & gestionary.chess_game.players[self.opposite_color].pieces_total:
                        legal_moves |= square

                    # capture left (if it is not on the a file and there is a piece to capture)
                    square = square_i << 7
                    if const.NOT_A_FILE & square_i and square & gestionary.chess_game.players[self.opposite_color].pieces_total:
                        legal_moves |= square

                    # en passant


            return legal_moves

    class Rook:
        def __init__(self, color):
            self.color = color
            self.opposite_color = - ~self.color

        def legal_moves(self, gestionary, square_i):
            legal_moves = 0

            # moving 1 to the right
            square = square_i
            while True:
                # if the piece is on the h file
                if not square & const.NOT_H_FILE:
                    break

                square <<= 1

                is_valid_move, stop  = is_valid_square(gestionary, square, self.color)
                if is_valid_move : legal_moves |= square
                if stop: break

            # moving 1 to the left
            square = square_i
            while True:
                # if the piece is on the a file
                if not square & const.NOT_A_FILE:
                    break
                square >>= 1

                is_valid_move, stop = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                if stop: break

            # moving 1 up
            square = square_i
            while True:
                square <<= 8

                is_valid_move, stop = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                if stop: break

            # moving 1 down
            square = square_i
            while True:
                square >>= 8

                is_valid_move, stop = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                if stop: break

            return legal_moves

    class Knight:
        def __init__(self, color):
            self.color = color
            self.opposite_color = - ~self.color

            self.knight_moves = self.get_knight_moves()

        def get_knight_moves(self):
            moves = []
            directions = [(6, 1), (10, 1), (15, 2), (17, 2)]
            for i in range(64):
                moves_per_square = 0
                for direction, delta in directions:
                    if 0 <= i + direction <= 63 and i // 8 == (i + direction) // 8 - delta:
                        moves_per_square |= 1 << i + direction
                    if 0 <= i - direction <= 63 and i // 8 == (i - direction) // 8 + delta:
                        moves_per_square |= 1 << i - direction
                moves.append(moves_per_square)
            return moves

        def legal_moves(self, gestionary, square_i):
            # removes all friendly pieces from list
            return self.knight_moves[square_i.bit_length()-1] & (~gestionary.chess_game.players[self.color].pieces_total & const.FULL_BOARD)

    class Bishop:
        def __init__(self, color):
            self.color = color
            self.opposite_color = - ~self.color

        def legal_moves(self, gestionary, square_i):
            legal_moves = 0

            # moving 1 to the right up
            square = square_i
            while True:
                # if the piece is on the h file
                if not square & const.NOT_H_FILE:
                    break

                square <<= 9

                is_valid_move, stop = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                if stop: break

            # moving 1 to the right down
            square = square_i
            while True:
                if not square & const.NOT_H_FILE:
                    break

                square >>= 7

                is_valid_move, stop = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                if stop: break

            # moving 1 to the left up
            square = square_i
            while True:
                # if the piece is on the a file
                if not const.NOT_A_FILE & square:
                    break

                square <<= 7

                is_valid_move, stop = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                if stop: break

            # moving 1 to the left down
            square = square_i
            while True:
                if not const.NOT_A_FILE & square:
                    break

                square >>= 9

                is_valid_move, stop = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                if stop: break

            return legal_moves

    class King:
        def __init__(self, color):
            self.color = color
            self.opposite_color = - ~self.color

        def legal_moves(self, gestionary, square_i):
            legal_moves = 0

            # all directions
            if square_i & const.NOT_A_FILE:
                # left down
                square = square_i >> 9
                is_valid_move, _ = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                # left
                square = square_i >> 1
                is_valid_move, _ = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                # left up
                square = square_i << 7
                is_valid_move, _ = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
            if square_i & const.NOT_H_FILE:
                # right down
                square = square_i >> 7
                is_valid_move, _ = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                # right
                square = square_i << 1
                is_valid_move, _ = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
                # right up
                square = square_i << 9
                is_valid_move, _ = is_valid_square(gestionary, square, self.color)
                if is_valid_move: legal_moves |= square
            # up
            square = square_i << 8
            is_valid_move, _ = is_valid_square(gestionary, square, self.color)
            if is_valid_move: legal_moves |= square
            # down
            square = square_i >> 8
            is_valid_move, _ = is_valid_square(gestionary, square, self.color)
            if is_valid_move: legal_moves |= square


            # short castle
            if not (gestionary.chess_game.players[self.color].king_moved_yet
                    or gestionary.chess_game.players[self.color].h_rook_move
                    or (3 << (5 + 7*self.opposite_color*8)) | gestionary.chess_game.total):
                legal_moves |= 1 << (6 + 7*self.opposite_color*8)

            # long castle
            if not (gestionary.chess_game.players[self.color].king_moved_yet
                    or gestionary.chess_game.players[self.color].a_rook_move
                    or (7 << (1 + 7*self.opposite_color*8)) | gestionary.chess_game.total):
                legal_moves |= 1 << (2 + 7*self.opposite_color*8)

            return legal_moves

    class Queen:
        def __init__(self, color):
            self.color = color

        def legal_moves(self, gestionary, square_i):
            return Piece.Rook(self.color).legal_moves(gestionary, square_i) | Piece.Bishop(self.color).legal_moves(gestionary, square_i)