"""
Classe joueur humain et bot
"""

import const
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
    def __init__(self, color, timer, venv):
        super().__init__(color, timer)
        self.calculated_move = None
        self.bot_calculating = False
        self.depth = 3

        self.venv = venv

        self.transposition_table = {}

    def find_move(self, gestionary):
        game = gestionary.chess_game

        self.bot_calculating = True

        status = game.status_to_key()
        self.venv.chess_game.key_to_status(status)

        self.venv.chess_game.player_turn = int(self.color == "b")
        self.venv.chess_game.index_position = game.index_position

        self.venv.chess_game.list_position = game.list_position[:game.index_position] + [status]

        th.Thread(target=self.minimax_with_alpha_beta_pruning,
                  args=(0, -math.inf, math.inf, int(self.color == "b"), self.depth, [], [])).start()

    def play_move(self, gestionary):
        move_i, move_f, promotion = self.calculated_move
        gestionary.chess_game.play_move(move_i, move_f, int(self.color == "b"), promotion)
        sound.play_sound(gestionary)
        gestionary.chess_game.sound_to_play = 0
        self.calculated_move = None
        self.bot_calculating = False

    def minimax_with_alpha_beta_pruning(self, depth, alpha, beta, player, depth_max, quiet_search, list_previous_moves):
        def undo_move():
            del self.venv.chess_game.list_position[-1]
            self.venv.chess_game.index_position -= 1
            self.venv.chess_game.player_turn ^= 1
            self.venv.chess_game.result = None
            self.venv.chess_game.key_to_status(self.venv.chess_game.list_position[-1])
            self.venv.chess_game.sound_to_play = 0


        best_move = []

        if depth >= depth_max and not quiet_search:
            return self.venv.chess_game.evaluation()


        if player == 0:
            max_eval = -math.inf

            for move_i, move_f, promotion in self.venv.chess_game.move_ordering():
                quiet_search = bool(move_f & self.venv.chess_game.total)

                self.venv.chess_game.play_move(move_i, move_f, player, promotion)

                """hash = self.venv.chess_game.zobrist_hash

                if hash in self.transposition_table:
                    child_eval = self.transposition_table[hash][1]

                else:
                    list_previous_moves.append(self.venv.chess_game.zobrist_hash)
                        ->
                    """


                if self.venv.chess_game.result is not None:
                    child_eval = self.venv.chess_game.evaluation()
                else:
                    child_eval = self.minimax_with_alpha_beta_pruning(depth + 1, alpha, beta, player ^ 1, depth_max, quiet_search, list_previous_moves)

                undo_move()

                if max_eval == child_eval or best_move == []: best_move.append(((move_i, move_f, promotion), child_eval))
                elif max_eval < child_eval: best_move = [((move_i, move_f, promotion), child_eval)]
                max_eval = max(child_eval, max_eval)
                alpha = max(child_eval, alpha)
                if alpha >= beta:
                    break

            if depth == 0:
                self.calculated_move, best_eval = rd.choice(best_move)

                """for move in list_previous_moves[:-1]:
                    self.transposition_table[move] = (self.calculated_move, best_eval)"""

                return
            return max_eval



        else:
            min_eval = math.inf

            for move_i, move_f, promotion in self.venv.chess_game.move_ordering():
                quiet_search = bool(move_f & self.venv.chess_game.total)

                self.venv.chess_game.play_move(move_i, move_f, player, promotion)

                """hash = self.venv.chess_game.zobrist_hash

                if hash in self.transposition_table:
                    child_eval =  self.transposition_table[hash][1]

                else:
                    list_previous_moves.append(self.venv.chess_game.zobrist_hash)
                        ->
                    """

                if self.venv.chess_game.result is not None:
                    child_eval = self.venv.chess_game.evaluation()
                else:
                    child_eval = self.minimax_with_alpha_beta_pruning(depth + 1, alpha, beta, player ^ 1, depth_max, quiet_search, list_previous_moves)

                undo_move()

                if min_eval == child_eval or best_move == []: best_move.append(((move_i, move_f, promotion), child_eval))
                elif min_eval > child_eval: best_move = [((move_i, move_f, promotion), child_eval)]
                min_eval = min(child_eval, min_eval)
                beta = min(child_eval, beta)
                if alpha >= beta:
                    break

            if depth == 0:
                self.calculated_move, best_eval = rd.choice(best_move)

                """for move in list_previous_moves[:-1]:
                    self.transposition_table[move] = (self.calculated_move, best_eval)"""

                return

            return min_eval
