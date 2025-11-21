"""
Classe joueur humain et bot
"""

import pygame as pg
import main
import random
import const
import board
import pieces
import game

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

    def return_move(self, candidate_move):
        if all(item is not None for item in candidate_move) and board.color_and_occupied_square(candidate_move[0], candidate_move[1]) == game.player_turn:
            rank_i, col_i, rank_f, col_f = candidate_move[0], candidate_move[1], candidate_move[2], candidate_move[3]
            specific = None

            game.left_click_down = None
            game.left_click_up = None
            game.candidate_move = [None, None, None, None]

            if (rank_f, col_f) in board.get_type(rank_i, col_i).legal_moves(rank_i, col_i):
                actual_position = [row[:] for row in game.position]

                if isinstance(board.get_type(rank_i, col_i), pieces.Piece.King):
                    self.king_pos = (rank_f, col_f)

                game.play_move(rank_i, col_i, rank_f, col_f, specific)
                if not game.in_check(self.color):
                    print("no check ...")
                else:
                    game.position = actual_position
                    return False

                return True
        return False

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