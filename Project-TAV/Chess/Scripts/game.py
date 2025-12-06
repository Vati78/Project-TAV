"""
Toutes les fonctions qui gèrent le déroulement de la partie.
"""

import const
import pieces
import player_bot as pb
import board


class Game:
    def __init__(self, gestionary):
        self.gestionary = gestionary

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
                    elif board.color_and_occupied_square(self.gestionary, self.left_click_up[0], self.left_click_up[1]) == self.player_turn:
                        self.candidate_move = [self.left_click_up[0], self.left_click_up[1], None, None]
                        self.left_click_down, self.left_click_up = None, None

                    else:
                        self.candidate_move[2], self.candidate_move[3] = self.left_click_down[0], self.left_click_down[1]
                        self.left_click_down, self.left_click_up = None, None

            else:
                # if the end square is the same color as the starting square
                if board.color_and_occupied_square(self.gestionary, self.left_click_up[0], self.left_click_up[1]) != self.player_turn:
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

        print(self.position)
    
    def in_check(self, player):
        for rank in self.position:
            print(rank)


        opposite_color = "b" if player == "w" else "w"
        coeff = -1 if player == "w" else 1

        (kp_rank, kp_col) = eval(f"self.{player}_player.king_pos")
        print(kp_rank, kp_col)

        pawn_dir = [(1*coeff, -1), (1*coeff, 1)]
        knight_dir = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
        bishop_dir = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        rook_dir =  [(0, 1), (1, 0), (-1, 0), (0, -1)]

        # for the pawn
        for dir in pawn_dir:
            new_rank = kp_rank+dir[0]
            new_col = kp_col+dir[1]
            if 0 <= new_rank <= 7 and 0 <= new_col <= 7:
                if board.color_and_occupied_square(self.gestionary, new_rank, new_col) == opposite_color:
                    if isinstance(board.get_type(self.gestionary, new_rank, new_col), pieces.Piece.Pawn):
                        print("Pawn", new_rank, new_col)
                        return True

        # for the knights
        for dir in knight_dir:
            new_rank = kp_rank+dir[0]
            new_col = kp_col+dir[1]
            if 0 <= new_rank <= 7 and 0 <= new_col <= 7:
                if board.color_and_occupied_square(self.gestionary, new_rank, new_col) == opposite_color:
                    if isinstance(board.get_type(self.gestionary, new_rank, new_col), pieces.Piece.Knight):
                        print("Nights")
                        return True

        # for the bishops and queen
        for dir in bishop_dir:
            rank, col = kp_rank, kp_col
            while 0 <= rank <= 7 and 0 <= col <= 7:
                rank += dir[0]
                col += dir[1]
                if 0 <= rank <= 7 and 0 <= col <= 7:
                    if board.color_and_occupied_square(self.gestionary, rank, col) == opposite_color:
                        if isinstance(board.get_type(self.gestionary, rank, col), (pieces.Piece.Bishop, pieces.Piece.Queen)):
                            print("Bishop, Queen")
                            return True
                        else:
                            break
                    elif board.color_and_occupied_square(self.gestionary, rank, col) == player:
                        break

        # for the rooks and queen
        for dir in rook_dir:
            rank, col = kp_rank, kp_col
            while 0 <= rank <= 7 and 0 <= col <= 7:
                rank += dir[0]
                col += dir[1]
                if 0 <= rank <= 7 and 0 <= col <= 7:
                    if board.color_and_occupied_square(self.gestionary, rank, col) == opposite_color:
                        if isinstance(board.get_type(self.gestionary, rank, col), (pieces.Piece.Rook, pieces.Piece.Queen)):
                            print("Rook/Queen")
                            return True
                        else:
                            break
                    elif board.color_and_occupied_square(self.gestionary, rank, col) == player:
                        break

        # for the opponent's king
        if abs(kp_rank-eval(f"self.{opposite_color}_player.king_pos[0]"))<2 and abs(kp_col-eval(f"self.{opposite_color}_player.king_pos[1]"))<2:
            return True

        return False






