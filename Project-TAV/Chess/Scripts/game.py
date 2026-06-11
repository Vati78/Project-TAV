"""
Toutes les fonctions qui gèrent le déroulement de la partie.
"""

import const
import pieces
import player_bot as pb
import board
import copy


class Game:
    def __init__(self, gestionary):
        self.gestionary = gestionary

        self.players = [pb.Player("w") if "w" in const.HUMAN else pb.Bot("w"), pb.Player("b") if "b" in const.HUMAN else pb.Bot("b")]
        ################################################
        self.total = self.players[0].pieces_total|self.players[1].pieces_total
        self.index_position = 0
        self.list_position = [(self.players[0].pieces, self.players[1].pieces)]
        ################################################
        self.player_turn = self.index_position % 2
        ################################################
        self.clicked_move = False
        self.double_click = False
        self.left_click_down = 0
        self.left_click_up = 0
        self.candidate_move = [0, 0]
        self.legal_moves = 1
        self.illegal_moves_list = []


    def input_to_candidate_move(self):
        """
        transforms input into the move wanted by the user
        :return: None
        """
        """
        Click down :
        if clicked not on right piece color
        --> if move_i
            --> if clicked_move
                --> if in legal_moves
                    --> move
                --> else
                    --> move = None
        --> else
            --> move = None
        if clicked on right piece color
        --> if move_i
            --> if clicked_move
                --> if square == move_i
                    --> double_click = True
                --> else
                    --> move_i
        --> else
            --> move_i
        """
        if self.left_click_down:
            if not self.left_click_down & self.players[self.player_turn].pieces_total:
                if self.candidate_move[0]:
                    if self.clicked_move:
                        #print(self.legal_moves)
                        #print(self.left_click_down & self.legal_moves)
                        if self.left_click_down & self.legal_moves:
                            self.candidate_move[1] = self.left_click_down
                        else:
                            self.candidate_move = [0, 0]
                            self.clicked_move = False
                            self.double_click = False
                else:
                    self.candidate_move = [0, 0]
                    self.clicked_move = False
                    self.double_click = False
            else:
                if self.candidate_move[0]:
                    if self.clicked_move:
                        if self.left_click_down == self.candidate_move[0]:
                            self.double_click = True
                        else:
                            self.candidate_move[0] = self.left_click_down
                            self.double_click = False
                            # update legal_moves
                else:
                    self.candidate_move[0] = self.left_click_down
                    # update legal_moves

        """ 
        Click up :
        if move_i
        --> if square is different
            --> if in legal_moves
                --> move
            --> else
                --> clicked_move = True
        --> if square is same
            --> if double_click
                --> move = None
            --> else
                --> clicked_move = True
        """
        if self.candidate_move[0] and self.left_click_up:
            if not self.candidate_move[0] == self.left_click_up:
                if self.left_click_up & self.legal_moves:
                    self.candidate_move[1] = self.left_click_up
                else:
                    self.clicked_move = True
            else:
                if self.double_click:
                    self.candidate_move = [0,0]
                    self.clicked_move = False
                    self.double_click = False
                else:
                    self.clicked_move = True

        if self.left_click_up:
            self.left_click_up = 0
        print(self.candidate_move, self.clicked_move, self.double_click)


    def play_move(self, square_i, square_f, color):
        player = self.players[color]
        opposite_player = self.players[- ~color & 1]

        # short castle
        if player.pieces[5] == square_i and square_f == square_i << 2:
            player.pieces[3] = player.pieces[3] ^ (square_f << 1) | (square_f >> 1)

        # long castle
        elif player.pieces[5] == square_i and square_f == square_i >> 2:
            player.pieces[3] = player.pieces[3] ^ (square_f >> 2) | (square_f << 1)

        # en passant
        elif True:
            pass

        # promotion
        elif True:
            pass
    
        for i in range(6):
            # changing the moving piece
            if square_i & player.pieces[i]:
                print(bin(player.pieces[i]))
                player.pieces[i] = player.pieces[i] ^ square_i | square_f
                print(bin(player.pieces[i]))
            # changing the opponent's piece if capture
            if square_f & opposite_player.pieces[i]:
                opposite_player.pieces[i] ^= square_f
        self.index_position += 1
        self.update_position()


    def in_check(self, color):
        opposite_color = - ~color & 1
        print(color, opposite_color, -~color & 1)
        opposite_player = self.players[opposite_color]

        k_pos = self.players[color].pieces[5]

        # pawns
        if not color: # white
            # if the white king is at least on the 6th rank or less
            if k_pos >> 16:
                if const.NOT_H_FILE & k_pos and (k_pos >> 7) & opposite_player.pieces[0]:
                    return True, 0
                if const.NOT_A_FILE & k_pos and (k_pos >> 9) & opposite_player.pieces[0]:
                    return True, 0
        else: # black
            # if the black king is on the 3rd rank or more
            if not k_pos >> 48:
                if const.NOT_H_FILE & k_pos and (k_pos << 9) & opposite_player.pieces[0]:
                    return True, 0, None
                if const.NOT_A_FILE & k_pos and (k_pos << 7) & opposite_player.pieces[0]:
                    return True, 0, None

        # knights
        if opposite_player.pieces[1] & pieces.Piece().Knight(color).knight_moves[k_pos.bit_length()-1]:
            return True, 1, None

        # bishops (and queen)
        if pieces.Piece().Bishop(color).legal_moves(self.gestionary, k_pos) & (opposite_player.pieces[2] | opposite_player.pieces[4]):
            return True

        # rooks (and queen)
        if pieces.Piece().Rook(color).legal_moves(self.gestionary, k_pos) & (opposite_player.pieces[3] | opposite_player.pieces[4]):
            return True

        # opponent's king
        pass

        return False


    def get_all_legal_moves(self, color):
        legal_moves = []
        illegal_moves = []
        is_in_check = False, None

        self.legal_moves = 0

        if self.in_check(color):
            self.legal_moves = 0

        for i in range(64):
            square = 1 << i
            if square & self.players[color].pieces_total:
                for j in range(6):
                    if square & self.players[color].pieces[j]:
                        legal_moves_piece = pieces.get_type(j, color).legal_moves(self.gestionary, square)
                        if square & self.left_click_down:
                            self.legal_moves = legal_moves_piece
        print("l:", self.left_click_down, self.legal_moves)
        #self.legal_moves = const.FULL_BOARD

        """                
            else:
                legal_moves.append(0)
                illegal_moves.append(0)
        for rank_f, col_f, specific in board.get_type(self.gestionary, rank, col).legal_moves(self.gestionary, rank, col):
            k_move = False
            specific_condition = True if specific is None else False

            if isinstance(board.get_type(self.gestionary, rank, col), pieces.Piece.King):
                k_move = True
                if specific == "s_castle":
                    if not self.gestionary.chess_game.in_check(self.player_turn):
                        self.gestionary.chess_game.play_move(rank, col, rank, col+1, specific)
                        exec(f"self.{self.player_turn}_player.king_pos = (rank, col+1)")
                        if not self.gestionary.chess_game.in_check(self.player_turn):
                            specific_condition = True

                if specific == "l_castle":
                    if not self.gestionary.chess_game.in_check(self.player_turn):
                        self.gestionary.chess_game.play_move(rank, col, rank, col-1, specific)
                        exec(f"self.{self.player_turn}_player.king_pos = (rank, col-1)")
                        if not self.gestionary.chess_game.in_check(self.player_turn):
                            specific_condition = True


                exec(f"self.{self.player_turn}_player.king_pos = (rank_f, col_f)")




            self.gestionary.chess_game.play_move(rank, col, rank_f, col_f, specific)

            if not self.gestionary.chess_game.in_check(self.player_turn) and specific_condition:
                legal_moves.append((rank_f, col_f, specific))
            else:
                illegal_moves.append((rank_f, col_f, specific))


            if k_move: exec(f"self.{self.player_turn}_player.king_pos = (rank, col)")
            self.position = [row[:] for row in actual_position]

        self.legal_moves_list = legal_moves
        self.illegal_moves_list = illegal_moves

        """
    def update_position(self):
        self.left_click_down = 0
        self.left_click_up = 0
        self.legal_moves = 0
        self.illegal_moves_list = []
        self.total = 0
        for j in self.players:
            for i in j.pieces:
                self.total |= i
        self.player_turn = self.index_position % 2
        for i in self.players: i.update_pos()
