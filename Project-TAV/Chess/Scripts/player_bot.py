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

    def move(self, chess_game):
        print(chess_game.candidate_move)
        rank_i = chess_game.candidate_move[0]
        col_i = chess_game.candidate_move[1]
        rank_f = chess_game.candidate_move[2]
        col_f = chess_game.candidate_move[3]

        specific = None
        #print(rank_i)
        #chess_game.candidate_move = [None, None, None, None]
        #print(rank_i)

        if (rank_f, col_f) in board.get_type(rank_i, col_i).legal_moves(rank_i, col_i):
            actual_position = [row[:] for row in chess_game.position]

            if isinstance(board.get_type(rank_i, col_i), pieces.Piece.King):
                self.king_pos = (rank_f, col_f)

            chess_game.play_move(rank_i, col_i, rank_f, col_f, specific)
            if not chess_game.in_check(self.color):
                print("no check ...")
            else:
                game.position = actual_position
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