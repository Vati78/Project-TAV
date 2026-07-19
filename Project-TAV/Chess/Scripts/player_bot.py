"""
Classe joueur humain et bot
"""

import const
import board
import pieces
import sound
import copy

class Item:
    def __init__(self, color):
        self.color = color
        self.opposite_color = "w" if self.color == "b" else "b"

        self.pieces = [0 for _ in range(6)]

        if color == "w":
            self.pieces[0] = 71776119061217280  # pawns
            self.pieces[1] = 4755801206503243776  # knights
            self.pieces[2] = 2594073385365405696  # bishops
            self.pieces[3] = 9295429630892703744  # rooks
            self.pieces[4] = 576460752303423488  # queens
            self.pieces[5] = 1152921504606846976  # king
        else:
            self.pieces[0] = 65280
            self.pieces[1] = 66
            self.pieces[2] = 36
            self.pieces[3] = 129
            self.pieces[4] = 8
            self.pieces[5] = 16

        self.pieces_total = 0
        for i in self.pieces:
            self.pieces_total |= i

        self.king_move = None
        self.a_rook_move = False
        self.h_rook_move = False
        self.last_piece_played = (0, 0)
        self.last_capture_or_pawn_move_index = 0

    def update_pos(self):
        self.pieces_total = 0
        for i in self.pieces:
            self.pieces_total |= i

class Player(Item):
    def move(self, gestionary):
        square_i, square_f = gestionary.chess_game.candidate_move

        promotion = False

        # promotion
        if square_i & self.pieces[0] and (square_f & const.RANK or not (square_f << 8) & const.FULL_BOARD):
            promotion = True

        gestionary.chess_game.play_move(square_i, square_f, int(self.color=="b"), promotion)

        if not gestionary.chess_game.candidate_move[1]:
            sound.play_sound(gestionary)
            if gestionary.chess_game.list_position[gestionary.chess_game.index_position][4] == 0:
                gestionary.chess_game.list_position[gestionary.chess_game.index_position][4] = copy.deepcopy(gestionary.chess_game.sound_to_play)
            gestionary.chess_game.sound_to_play.clear()


class Bot(Item):
    def return_move(self):
        pass