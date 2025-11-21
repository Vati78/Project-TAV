"""
Toutes les fonctions qui gèrent le déroulement de la partie.
"""

import pygame as pg
import main
import const
import player_bot as pb
import board

position = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


player_turn = "w"

w_player = pb.Player("w") if "w" in const.HUMAN else pb.Bot("w")
b_player = pb.Player("b") if "b" in const.HUMAN else pb.Bot("b")

left_click_down = None
left_click_up = None
candidate_move = [None, None, None, None]


def input_to_candidate_move():
    global left_click_up, left_click_down, candidate_move

    if left_click_up is not None:
        if left_click_down == left_click_up: # if clicked
            if (candidate_move[0], candidate_move[1]) == (None, None):
                # blit legal moves
                candidate_move[0], candidate_move[1] = left_click_down[0], left_click_down[1]

            elif ((candidate_move[2], candidate_move[3]) == (None, None)
                  and (left_click_down[0], left_click_down[1]) != (candidate_move[0], candidate_move[1])):
                candidate_move[2], candidate_move[3] = left_click_down[0], left_click_down[1]

        else:
            candidate_move = [left_click_down[0], left_click_down[1], left_click_up[0], left_click_up[1]]

    elif left_click_down and left_click_up is None:
        # blit legal moves
        pass

def make_move():
    global left_click_up, left_click_down, candidate_move, player_turn

    move = eval(f"{player_turn}_player.return_move(candidate_move)")

    if move:
        player_turn = "w" if player_turn == "b" else "b"

def play_move(rank_i, col_i, rank_f, col_f, specific=None):
    if specific == "s_castle":
        position[rank_i][5] = player_turn+"R"
        position[rank_i][7] = " "
    elif specific == "l_castle":
        position[rank_i][3] = player_turn+"R"
        position[rank_i][0] = " "
    elif specific == "en_passant":
        pass
    elif specific == "promote":
        pass

    position[rank_f][col_f] = position[rank_i][col_i]
    position[rank_i][col_i] = " "

def in_check(player):
    opposite_color = "b" if player == "w" else "w"

    for ranks, a in enumerate(position):
        for cols, piece in enumerate(a):
            if piece[0] == opposite_color:
                if (eval(f"{player}_player.king_pos")) in board.get_type(ranks, cols).legal_moves(ranks, cols):
                    print(ranks, cols)
                    return True
    return False







