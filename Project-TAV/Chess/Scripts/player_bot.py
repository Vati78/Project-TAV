"""
Classe joueur humain et bot
"""

import const
import board
import sound
import random as rd
import math
import threading as th

class Item:
    def __init__(self, color, timer):
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

        self.timer = timer[0] * 60 if timer is not None else None
        self.increment = timer[1] if timer is not None else None

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

        move = gestionary.chess_game.play_move(square_i, square_f, int(self.color=="b"), promotion)

        # if a move was indeed made
        if move:
            sound.play_sound(gestionary)
            gestionary.chess_game.sound_to_play = 0

            gestionary.chess_game.left_click_down = 0
            gestionary.chess_game.left_click_up = 0
            gestionary.chess_game.candidate_move = [0, 0]



class Bot(Item):
    def __init__(self, color, timer, virtual_environment):
        super().__init__(color, timer)
        self.calculated_move = None
        self.bot_calculating = False
        self.depth = 4

        self.virtual_environment = virtual_environment

    def find_move(self, gestionary):
        self.bot_calculating = True

        status = gestionary.chess_game.status_to_key()
        self.virtual_environment.chess_game.key_to_status(status)

        self.virtual_environment.chess_game.player_turn = int(self.color == "b")
        self.virtual_environment.chess_game.index_position = 0

        self.virtual_environment.chess_game.list_position = [status]

        th.Thread(target=self.minimax_with_alpha_beta_pruning,
                  args=(self.depth, -math.inf, math.inf, int(self.color == "b"), self.depth)).start()

    def play_move(self, gestionary):
        i, square_f, promotion = self.calculated_move
        gestionary.chess_game.play_move(1 << i, square_f, int(self.color == "b"), promotion)
        sound.play_sound(gestionary)
        gestionary.chess_game.sound_to_play = 0
        self.calculated_move = None
        self.bot_calculating = False

    def minimax_with_alpha_beta_pruning(self, depth, alpha, beta, player, depth_i):
        best_move = []

        #print("Profondeur :", depth)
        if depth == 0:
            evaluate = self.virtual_environment.chess_game.evaluation()
            return evaluate

        def undo_move():
            del self.virtual_environment.chess_game.list_position[-1]
            self.virtual_environment.chess_game.index_position -= 1
            self.virtual_environment.chess_game.player_turn ^= 1
            self.virtual_environment.chess_game.result = None
            self.virtual_environment.chess_game.key_to_status(self.virtual_environment.chess_game.list_position[-1])
            self.virtual_environment.chess_game.sound_to_play = 0

        if player == 0:
            max_eval = -math.inf

            for i, legal_moves in enumerate(self.virtual_environment.chess_game.list_legal_moves):
                if legal_moves:
                    for move in board.split_bits(legal_moves):
                        #print(2*depth*"_", "Move :", i, "-->", move.bit_length()-1)
                        # promotion available
                        if (1 << i) & self.virtual_environment.chess_game.players[player].pieces[0] and i//8 == 1:
                            #print("Promotion")
                            for promoted_piece in range(1,5):
                                self.virtual_environment.chess_game.play_move(1 << i, move, player, promoted_piece)
                                if self.virtual_environment.chess_game.result is not None: child_eval = self.virtual_environment.chess_game.evaluation()
                                else: child_eval = self.minimax_with_alpha_beta_pruning(depth - 1, alpha, beta, player ^ 1, depth_i)
                                undo_move()
                                #print(2*depth*"_", "Evaluation :", child_eval)
                                if max_eval == child_eval or best_move == []: best_move.append((i, move, promoted_piece))
                                elif max_eval < child_eval: best_move = [(i, move, promoted_piece)]
                                max_eval = max(child_eval, max_eval)
                                alpha = max(child_eval, alpha)
                                if alpha >= beta:
                                    break

                        else:
                            self.virtual_environment.chess_game.play_move(1 << i, move, player)
                            if self.virtual_environment.chess_game.result is not None: child_eval = self.virtual_environment.chess_game.evaluation()
                            else: child_eval = self.minimax_with_alpha_beta_pruning(depth - 1, alpha, beta, player ^ 1, depth_i)
                            undo_move()
                            if max_eval == child_eval or best_move == []: best_move.append((i, move, False))
                            elif max_eval < child_eval: best_move = [(i, move, False)]
                            max_eval = max(child_eval, max_eval)
                            alpha = max(child_eval, alpha)
                            if alpha >= beta:
                                break


            if depth == depth_i:
                self.calculated_move = rd.choice(best_move)
                return
            return max_eval

        else:
            min_eval = math.inf

            for i, legal_moves in enumerate(self.virtual_environment.chess_game.list_legal_moves):
                if legal_moves:
                    for move in board.split_bits(legal_moves):
                        #print((2 * depth * "_", "Move :", i, "-->", move.bit_length() - 1)
                        # promotion available
                        if (1 << i) & self.virtual_environment.chess_game.players[player].pieces[0] and i//8 == 6:
                            #print(("Promotion")
                            for promoted_piece in range(1, 5):
                                self.virtual_environment.chess_game.play_move(1 << i, move, player, promoted_piece)
                                if self.virtual_environment.chess_game.result is not None: child_eval = self.virtual_environment.chess_game.evaluation()
                                else: child_eval = self.minimax_with_alpha_beta_pruning(depth - 1, alpha, beta, player ^ 1, depth_i)
                                undo_move()
                                #print((2*depth*"_", "Result :", child_eval)
                                if min_eval == child_eval or best_move == []: best_move.append((i, move, promoted_piece))
                                elif min_eval > child_eval: best_move = [(i, move, promoted_piece)]
                                min_eval = min(child_eval, min_eval)
                                beta = min(child_eval, beta)
                                if alpha >= beta:
                                    break



                        else:
                            self.virtual_environment.chess_game.play_move(1 << i, move, player)
                            if self.virtual_environment.chess_game.result is not None: child_eval = self.virtual_environment.chess_game.evaluation()
                            else: child_eval = self.minimax_with_alpha_beta_pruning(depth - 1, alpha, beta, player ^ 1, depth_i)
                            undo_move()
                            #print((2*depth*"_", "Result :", child_eval)
                            if min_eval == child_eval or best_move == []: best_move.append((i, move, False))
                            elif min_eval > child_eval: best_move = [(i, move, False)]
                            min_eval = min(child_eval, min_eval)
                            beta = min(child_eval, beta)
                            if alpha >= beta:
                                break



            if depth == depth_i:
                self.calculated_move = rd.choice(best_move)
                return

            return min_eval
