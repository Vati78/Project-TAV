"""
Toutes les fonctions qui gèrent le déroulement de la partie.
"""

import pygame as pg
import main
import const
import player_bot as pb
import board


class Game:
    def __init__(self):
        self.position = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    [" ", " ", " ", " ", " ", " ", " ", " "],
                    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


        self.player_turn = "w"
        self.opposite_color = "b"

        self.w_player = pb.Player("w") if "w" in const.HUMAN else pb.Bot("w")
        self.b_player = pb.Player("b") if "b" in const.HUMAN else pb.Bot("b")

        self.human = True if self.player_turn in const.HUMAN else False

        self.left_click_down = None
        self.left_click_up = None
        self.candidate_move = [None, None, None, None]



    def input_to_candidate_move(self):
        # if the button was released
        if self.left_click_up is not None:

            # if clicked
            if self.left_click_down == self.left_click_up:
                # if nothing was clicked
                if (self.candidate_move[0], self.candidate_move[1]) == (None, None):
                    self.candidate_move[0], self.candidate_move[1] = self.left_click_down[0], self.left_click_down[1]
                    self.left_click_down, self.left_click_up = None, None

                # if something was already clicked
                elif (self.candidate_move[2], self.candidate_move[3]) == (None, None):

                    # if the end square is the same as the starting square
                    if (self.left_click_down[0], self.left_click_down[1]) == (self.candidate_move[0], self.candidate_move[1]):
                        self.candidate_move = [None, None, None, None]
                        self.left_click_down, self.left_click_up = None, None

                    # if the end square is the same color as the starting square
                    elif board.color_and_occupied_square(self.left_click_up[0], self.left_click_up[1]) == self.player_turn:
                        self.candidate_move = [self.left_click_up[0], self.left_click_up[1], None, None]
                        self.left_click_down, self.left_click_up = None, None

                    else:
                        self.candidate_move[2], self.candidate_move[3] = self.left_click_down[0], self.left_click_down[1]
                        self.left_click_down, self.left_click_up = None, None
    
            else:
                # if the end square is the same color as the starting square
                if board.color_and_occupied_square(self.left_click_up[0], self.left_click_up[1]) != self.player_turn:
                    self.candidate_move = [self.left_click_down[0], self.left_click_down[1], self.left_click_up[0], self.left_click_up[1]]

                self.left_click_down, self.left_click_up = None, None


    def make_move(self):
        move = eval(f"self.{self.player_turn}_player.return_move(self.candidate_move)")
    
        if move:
            self.player_turn = "w" if self.player_turn == "b" else "b"
    
    def play_move(self, rank_i, col_i, rank_f, col_f, specific=None):
        if specific == "s_castle":
            self.position[rank_i][5] = self.player_turn+"R"
            self.position[rank_i][7] = " "
        elif specific == "l_castle":
            self.position[rank_i][3] = self.player_turn+"R"
            self.position[rank_i][0] = " "
        elif specific == "en_passant":
            pass
        elif specific == "promote":
            pass
    
        self.position[rank_f][col_f] = self.position[rank_i][col_i]
        self.position[rank_i][col_i] = " "
    
    def in_check(self, player):
        opposite_color = "b" if player == "w" else "w"
    
        for ranks, a in enumerate(self.position):
            for cols, piece in enumerate(a):
                if piece[0] == opposite_color:
                    if (eval(f"{player}_player.king_pos")) in board.get_type(ranks, cols).legal_moves(ranks, cols):
                        print(ranks, cols)
                        return True
        return False
    
    def blit_legal_moves_if_possible(self):
        if (self.candidate_move[2], self.candidate_move[3]) == (None, None) and self.candidate_move[0] is not None and self.candidate_move[1] is not None:
            board.blit_legal_moves(self.candidate_move[0], self.candidate_move[1])





