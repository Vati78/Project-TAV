"""
Classe joueur humain et bot
"""

import const
import board
import sound
import copy
import random as rd
import math


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

        self.s_castling_right = True
        self.l_castling_right = True
        self.castled = False
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
    def return_move(self, gestionary):
        print(self.minimax_with_alpha_beta_pruning(gestionary, 3, -math.inf, math.inf, 1))
        """
        gestionary.chess_game.get_all_legal_moves(int(self.color == "b"))
        lmoves = []
        for i, j in enumerate(gestionary.chess_game.list_legal_moves):
            for b in board.split_bits(j):
                lmoves.append([2 ** i, b])
        if lmoves == []: return
        move = rd.choice(lmoves)
        gestionary.chess_game.play_move(move[0], move[1], int(self.color == "b"), False)
        """
    def minimax_with_alpha_beta_pruning(self, gestionary, depth, alpha, beta, player):
        print("Profondeur :", depth)
        if depth == 0:
            evaluate = gestionary.chess_game.evaluation()
            return evaluate

        status = {
            "players": copy.deepcopy(gestionary.chess_game.players),
            "player_turn": gestionary.chess_game.player_turn,
            "check": gestionary.chess_game.check,
            "list_legal_moves": copy.deepcopy(gestionary.chess_game.list_legal_moves),
            "index_last_capture_or_pawn_move": gestionary.chess_game.index_last_capture_or_pawn_move,
            "total": gestionary.chess_game.total,
        }

        def undo_move():
            gestionary.chess_game.players = copy.deepcopy(status["players"])
            gestionary.chess_game.player_turn = status["player_turn"]
            gestionary.chess_game.check = status["check"]
            gestionary.chess_game.list_legal_moves = copy.deepcopy(status["list_legal_moves"])
            gestionary.chess_game.index_last_capture_or_pawn_move = status["index_last_capture_or_pawn_move"]
            gestionary.chess_game.total = status["total"]
            del gestionary.chess_game.list_position[-1]
            gestionary.chess_game.index_position -= 1
            gestionary.chess_game.player_turn ^= 1
            gestionary.chess_game.result = None

        if player == 0:
            max_eval = -math.inf

            for i, legal_moves in enumerate(gestionary.chess_game.list_legal_moves):
                if legal_moves:
                    for move in board.split_bits(legal_moves):
                        print(2*depth*"_", "Move :", i, "-->", move.bit_length()-1)
                        # promotion available
                        if (1 << i) & gestionary.chess_game.players[player].pieces[0] and i//8 == 1:
                            print("Promotion")
                            for promoted_piece in range(1,5):
                                gestionary.chess_game.play_move(1 << i, move, player, promoted_piece)
                                child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth - 1, alpha, beta, player ^ 1)
                                print(2*depth*"_", "Evaluation :", child_eval)
                                max_eval = max(child_eval, max_eval)
                                alpha = max(child_eval, alpha)
                                if alpha >= beta:
                                    break

                                undo_move()

                        else:
                            gestionary.chess_game.play_move(1 << i, move, player)
                            child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth-1, alpha, beta, player^1)
                            print(2*depth*"_", "Evaluation :", child_eval)
                            max_eval = max(child_eval, max_eval)
                            alpha = max(child_eval, alpha)
                            if alpha >= beta:
                                break

                            undo_move()

            return max_eval

        else:
            min_eval = math.inf

            for i, legal_moves in enumerate(gestionary.chess_game.list_legal_moves):
                if legal_moves:
                    for move in board.split_bits(legal_moves):
                        print(2 * depth * "_", "Move :", i, "-->", move.bit_length() - 1)
                        # promotion available
                        if (1 << i) & gestionary.chess_game.players[player].pieces[0] and i//8 == 6:
                            print("Promotion")
                            for promoted_piece in range(1, 5):
                                gestionary.chess_game.play_move(1 << i, move, player, promoted_piece)
                                child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth - 1, alpha, beta, player ^ 1)
                                print(2*depth*"_", "Result :", child_eval)
                                min_eval = min(child_eval, min_eval)
                                beta = min(child_eval, beta)
                                if alpha >= beta:
                                    break

                                undo_move()

                        else:
                            gestionary.chess_game.play_move(1 << i, move, player)
                            child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth - 1, alpha, beta, player ^ 1)
                            print(2*depth*"_", "Result :", child_eval)
                            min_eval = min(child_eval, min_eval)
                            beta = min(child_eval, beta)
                            if alpha >= beta:
                                break

                            undo_move()

            return min_eval
