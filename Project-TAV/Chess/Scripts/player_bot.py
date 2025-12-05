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
        self.king_pos = (7, 4) if self.color == "w" else (0, 4)
        self.king_move = False
        self.a_rook_move = False
        self.h_rook_move = False
        self.s_castling_right = True
        self.l_castling_right = True
        self.castle = False

    def move(self, gestionary):
        print(gestionary.chess_game.candidate_move)
        rank_i = gestionary.chess_game.candidate_move[0]
        col_i = gestionary.chess_game.candidate_move[1]
        rank_f = gestionary.chess_game.candidate_move[2]
        col_f = gestionary.chess_game.candidate_move[3]

        gestionary.chess_game.candidate_move = [None, None, None, None]

        if (rank_f, col_f) in board.get_type(gestionary, rank_i, col_i).legal_moves(gestionary, rank_i, col_i):
            actual_position = [row[:] for row in gestionary.chess_game.position]
            specific = None
            king_move = False
            capture = board.color_and_occupied_square(gestionary, rank_f, col_f)

            if isinstance(board.get_type(gestionary, rank_i, col_i), pieces.Piece.King):
                king_move = True
                self.king_pos = (rank_f, col_f)

            gestionary.chess_game.play_move(rank_i, col_i, rank_f, col_f, specific)

            if not gestionary.chess_game.in_check(self.color):
                if capture: const.capture_sound.play()
                else: const.move_sound.play()
            else:
                const.illegal_sound.play()
                gestionary.chess_game.position = actual_position
                if king_move: self.king_pos = (rank_i, col_i)
                return False

            return True

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