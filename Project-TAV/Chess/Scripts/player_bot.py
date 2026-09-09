"""
Classe joueur humain et bot
"""

import const
import board
import sound
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

        # if a move was indeed made
        if not gestionary.chess_game.candidate_move[1]:
            sound.play_sound(gestionary)
            gestionary.chess_game.sound_to_play = 0


class Bot(Item):
    def find_and_play_move(self, gestionary):
        i, square_f, promotion = self.minimax_with_alpha_beta_pruning(gestionary, 2,
                                        -math.inf, math.inf, int(self.color == "b"), 2)
        gestionary.chess_game.play_move(1 << i, square_f, int(self.color == "b"), promotion)
        sound.play_sound(gestionary)
        gestionary.chess_game.sound_to_play = 0

    def minimax_with_alpha_beta_pruning(self, gestionary, depth, alpha, beta, player, depth_i):
        best_move = []
        status = gestionary.chess_game.status_to_key()

        #print("Profondeur :", depth)
        if depth == 0:
            evaluate = gestionary.chess_game.evaluation()
            return evaluate

        def undo_move():
            del gestionary.chess_game.list_position[-1]
            gestionary.chess_game.index_position -= 1
            gestionary.chess_game.player_turn ^= 1
            gestionary.chess_game.result = None
            gestionary.chess_game.key_to_status(gestionary.chess_game.list_position[-1])
            gestionary.chess_game.sound_to_play = 0

        if player == 0:
            max_eval = -math.inf

            for i, legal_moves in enumerate(gestionary.chess_game.list_legal_moves):
                if legal_moves:
                    for move in board.split_bits(legal_moves):
                        #print(2*depth*"_", "Move :", i, "-->", move.bit_length()-1)
                        # promotion available
                        if (1 << i) & gestionary.chess_game.players[player].pieces[0] and i//8 == 1:
                            #print("Promotion")
                            for promoted_piece in range(1,5):
                                gestionary.chess_game.play_move(1 << i, move, player, promoted_piece)
                                if gestionary.chess_game.result is not None: child_eval = gestionary.chess_game.evaluation()
                                else: child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth - 1, alpha, beta, player ^ 1, depth_i)
                                undo_move()
                                #print(2*depth*"_", "Evaluation :", child_eval)
                                if max_eval == child_eval or best_move == []: best_move.append((i, move, promoted_piece))
                                elif max_eval > child_eval: best_move = [(i, move, promoted_piece)]
                                max_eval = max(child_eval, max_eval)
                                alpha = max(child_eval, alpha)
                                if alpha >= beta:
                                    break

                        else:
                            gestionary.chess_game.play_move(1 << i, move, player)
                            if gestionary.chess_game.result is not None: child_eval = gestionary.chess_game.evaluation()
                            else: child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth - 1, alpha, beta, player ^ 1, depth_i)
                            undo_move()
                            if max_eval == child_eval or best_move == []: best_move.append((i, move, False))
                            elif max_eval < child_eval: best_move = [(i, move, False)]
                            max_eval = max(child_eval, max_eval)
                            alpha = max(child_eval, alpha)
                            if alpha >= beta:
                                break


            if depth == depth_i:
                return rd.choice(best_move)
            return max_eval

        else:
            min_eval = math.inf

            for i, legal_moves in enumerate(gestionary.chess_game.list_legal_moves):
                if legal_moves:
                    for move in board.split_bits(legal_moves):
                        #print((2 * depth * "_", "Move :", i, "-->", move.bit_length() - 1)
                        # promotion available
                        if (1 << i) & gestionary.chess_game.players[player].pieces[0] and i//8 == 6:
                            #print(("Promotion")
                            for promoted_piece in range(1, 5):
                                gestionary.chess_game.play_move(1 << i, move, player, promoted_piece)
                                if gestionary.chess_game.result is not None: child_eval = gestionary.chess_game.evaluation()
                                else: child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth - 1, alpha, beta, player ^ 1, depth_i)
                                undo_move()
                                #print((2*depth*"_", "Result :", child_eval)
                                if min_eval == child_eval or best_move == []: best_move.append((i, move, promoted_piece))
                                elif min_eval > child_eval: best_move = [(i, move, promoted_piece)]
                                min_eval = min(child_eval, min_eval)
                                beta = min(child_eval, beta)
                                if alpha >= beta:
                                    break



                        else:
                            gestionary.chess_game.play_move(1 << i, move, player)
                            if gestionary.chess_game.result is not None: child_eval = gestionary.chess_game.evaluation()
                            else: child_eval = self.minimax_with_alpha_beta_pruning(gestionary, depth - 1, alpha, beta, player ^ 1, depth_i)
                            undo_move()
                            #print((2*depth*"_", "Result :", child_eval)
                            if min_eval == child_eval or best_move == []: best_move.append((i, move, False))
                            elif min_eval > child_eval: best_move = [(i, move, False)]
                            min_eval = min(child_eval, min_eval)
                            beta = min(child_eval, beta)
                            if alpha >= beta:
                                break



            if depth == depth_i:
                return rd.choice(best_move)

            return min_eval
