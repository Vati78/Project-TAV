"""
Classe joueur humain et bot
"""

import pygame as pg
import const
import board
import pieces


class Player:
    def __init__(self,color):
        self.color = color
        self.opposite_color = "w" if self.color == "b" else "b"
        self.king_pos = (7, 4) if self.color == "w" else (0, 4)
        self.king_move = False
        self.a_rook_move = False
        self.h_rook_move = False
        self.s_castling_right = True
        self.l_castling_right = True
        self.castle = False

    def move(self, gestionary):
        rank_i = gestionary.chess_game.candidate_move[0]
        col_i = gestionary.chess_game.candidate_move[1]
        rank_f = gestionary.chess_game.candidate_move[2]
        col_f = gestionary.chess_game.candidate_move[3]

        gestionary.chess_game.candidate_move = [None, None, None, None]

        for rank, col, specific in gestionary.chess_game.legal_moves_list:
            if rank_f == rank and col_f == col:
                capture = board.color_and_occupied_square(gestionary, rank_f, col_f)
                if isinstance(board.get_type(gestionary, rank_i, col_i), pieces.Piece.King):
                    self.king_pos = (rank_f, col_f)

                gestionary.chess_game.play_move(rank_i, col_i, rank_f, col_f, specific)

                if gestionary.chess_game.in_check(self.opposite_color): const.check_sound.play()
                elif capture: const.capture_sound.play()
                else: const.move_sound.play()
        else:
            for rank, col, specific in gestionary.chess_game.illegal_moves_list:
                if rank_f == rank and col_f == col:
                    const.illegal_sound.play()

        gestionary.chess_game.legal_moves_list = []
        gestionary.chess_game.illegal_moves_list = []

class Bot:
    def __init__(self, color):
        self.color = color
        self.king_pos = (7, 4) if self.color == "w" else (0, 4)
        self.king_move = False
        self.a_rook_move = False
        self.h_rook_move = False
        self.s_castling_right = True
        self.l_castling_right = True
        self.castle = False

    def return_move(self):
        pass