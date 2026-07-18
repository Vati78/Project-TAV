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
        #                      players                      total              legal_moves        sound
        self.list_position = [[copy.deepcopy(self.players), self.total,        0,                 []]]
        ################################################
        self.player_turn = self.index_position % 2
        ################################################
        self.clicked_move = False
        self.double_click = False
        self.left_click_down = 0
        self.left_click_up = 0
        self.candidate_move = [0, 0]
        self.list_legal_moves = []
        self.legal_moves = 0
        #################################################
        self.sound_to_play = []

    def input_to_candidate_move(self):
        """
        transforms input into the move wanted by the user
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
                        if self.left_click_down & self.legal_moves:
                            self.candidate_move[1] = self.left_click_down
                            self.clicked_move = False
                            self.double_click = False
                            self.legal_moves = 0
                        else:
                            self.candidate_move = [0, 0]
                            self.clicked_move = False
                            self.double_click = False
                            self.legal_moves = 0
                else:
                    self.candidate_move = [0, 0]
                    self.clicked_move = False
                    self.double_click = False
                    self.legal_moves = 0
            else:
                if self.candidate_move[0]:
                    if self.clicked_move:
                        if self.left_click_down == self.candidate_move[0]:
                            self.double_click = True
                        else:
                            self.candidate_move[0] = self.left_click_down
                            self.clicked_move = False
                            self.double_click = False
                            self.legal_moves = self.list_legal_moves[self.candidate_move[0].bit_length() - 1]
                else:
                    self.candidate_move[0] = self.left_click_down
                    self.legal_moves = self.list_legal_moves[self.candidate_move[0].bit_length()-1]

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
                    self.clicked_move = False
                    self.double_click = False
                    self.legal_moves = 0
                else:
                    self.clicked_move = True
            else:
                if self.double_click:
                    self.candidate_move = [0,0]
                    self.clicked_move = False
                    self.double_click = False
                    self.legal_moves = 0
                else:
                    self.clicked_move = True

        if self.left_click_up:
            self.left_click_up = 0

        #print(self.candidate_move, self.clicked_move, self.double_click)


    def check_and_pins(self, color, square):
        opposite_color = color ^ 1
        opposite_player = self.players[opposite_color]

        index_square = square.bit_length() - 1

        threats_pins_and_free_squares = []


        # up
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(index_square//8):
            studied_square = square >> (8 * (i+1))

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a rook
                    if studied_square & (opposite_player.pieces[3] | opposite_player.pieces[4]):
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat, potential_pin, free_squares))


        # up-right
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(min(index_square//8, 7 - (index_square%8))):
            studied_square = square >> (7 * (i + 1))

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a bishop
                    if studied_square & (opposite_player.pieces[2] | opposite_player.pieces[4]):
                        threat = studied_square
                    # if it's a pawn
                    elif i == 0 and color == 0 and studied_square & opposite_player.pieces[0]:
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat,potential_pin,free_squares))


        # right
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(7 - (index_square%8)):
            studied_square = square << (i + 1)

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a rook
                    if studied_square & (opposite_player.pieces[3] | opposite_player.pieces[4]):
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat,potential_pin,free_squares))


        # down-right
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(min(7 - (index_square//8), 7 - (index_square%8))):
            studied_square = square << (9 * (i + 1))

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a bishop
                    if studied_square & (opposite_player.pieces[2] | opposite_player.pieces[4]):
                        threat = studied_square
                    # if it's a pawn
                    elif i == 0 and color == 1 and studied_square & opposite_player.pieces[0]:
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat,potential_pin,free_squares))


        # down
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(7 - (index_square//8)):
            studied_square = square << (8 * (i + 1))

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a rook
                    if studied_square & (opposite_player.pieces[3] | opposite_player.pieces[4]):
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat,potential_pin,free_squares))


        # down-left
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(min(7 - (index_square//8), index_square%8)):
            studied_square = square << (7 * (i + 1))

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a bishop
                    if studied_square & (opposite_player.pieces[2] | opposite_player.pieces[4]):
                        threat = studied_square
                    # if it's a pawn
                    elif i == 0 and color == 1 and studied_square & opposite_player.pieces[0]:
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat,potential_pin,free_squares))


        # left
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(index_square%8):
            studied_square = square >> (i + 1)

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a rook
                    if studied_square & (opposite_player.pieces[3] | opposite_player.pieces[4]):
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat,potential_pin,free_squares))


        # up-left
        threat = False
        potential_pin = 0
        free_squares = 0
        for i in range(min(index_square//8, index_square%8)):
            studied_square = square >> (9 * (i + 1))

            if studied_square & self.total:
                # if the encountered piece is friendly (ignore king)
                if studied_square & (self.players[color].pieces_total ^ self.players[color].pieces[5]):
                    if potential_pin: break
                    potential_pin = studied_square

                elif studied_square & opposite_player.pieces_total:
                    # if the opponent's piece is a queen or a bishop
                    if studied_square & (opposite_player.pieces[2] | opposite_player.pieces[4]):
                        threat = studied_square
                    # if it's a pawn
                    elif i == 0 and color == 0 and studied_square & opposite_player.pieces[0]:
                        threat = studied_square

                    break
            free_squares |= studied_square
        threats_pins_and_free_squares.append((threat,potential_pin,free_squares))


        # knights
        threat = False
        moves = pieces.Piece().Knight(color).legal_moves(self.gestionary, square)
        # if the last piece played is a knight
        if opposite_player.last_piece_played[1] & opposite_player.pieces[1]:
            # if it checks the king
            if moves & opposite_player.last_piece_played[1]:
                threat = opposite_player.last_piece_played[1]
        elif moves & opposite_player.pieces[1]:
            threat = True
        threats_pins_and_free_squares.append((threat, 0, 0))

        return threats_pins_and_free_squares


    def get_all_legal_moves(self, color):
        self.list_legal_moves = [0 for _ in range(64)]

        a = self.check_and_pins(color, self.players[color].pieces[5])
        nb_checks = 0
        threat, pin, free_squares = 0, 0, 0
        for a_threat, a_pin, a_free_squares in a:
            if a_threat:
                pin |= a_pin
                free_squares = a_free_squares | a_threat
                if not a_pin:
                    nb_checks += 1

            # if double_check
            if nb_checks > 1: break

        for j in range(6):
            # if king
            if j == 5:
                square = self.players[color].pieces[5]
                i = square.bit_length() - 1
                legal_moves = pieces.get_type(j, color).legal_moves(self.gestionary, square)

                for move in board.split_bits(legal_moves):
                    a = self.check_and_pins(color, move)
                    for a_threat, a_pin, a_free_squares in a:
                        if a_threat and not a_pin:
                            legal_moves ^= move
                            break

                # short castle
                if (square << 2) & legal_moves and (nb_checks or not (square << 1) & legal_moves):
                    legal_moves ^= square << 2

                # long castle
                if (square >> 2) & legal_moves and (nb_checks or not (square >> 1) & legal_moves):
                    legal_moves ^= square >> 2

                self.list_legal_moves[i] = legal_moves


            else:
                if nb_checks < 2:
                    for square in board.split_bits(self.players[color].pieces[j]):
                        i = square.bit_length() - 1
                        legal_moves = pieces.get_type(j, color).legal_moves(self.gestionary, square)


                        if nb_checks == 1 or pin & square:
                            self.list_legal_moves[i] = legal_moves & free_squares
                        else:
                            self.list_legal_moves[i] = legal_moves

                else:
                    for square in board.split_bits(self.players[color].pieces[j]):
                        i = square.bit_length() - 1
                        self.list_legal_moves[i] = 0


        if all(move == 0 for move in self.list_legal_moves):
            if nb_checks == 0: print("stalemate")
            else: print("checkmate")

            self.sound_to_play.append("end")

        elif nb_checks: self.sound_to_play.append("check")


    def play_move(self, square_i, square_f, color, promotion=False):
        player = self.players[color]
        opposite_player = self.players[color ^ 1]

        # short castle
        if player.pieces[5] == square_i and square_f == square_i << 2:
            player.pieces[3] = player.pieces[3] ^ (square_f << 1) | (square_f >> 1)
            player.h_rook_move = True
            self.sound_to_play.append("castle")

        # long castle
        elif player.pieces[5] == square_i and square_f == square_i >> 2:
            player.pieces[3] = player.pieces[3] ^ (square_f >> 2) | (square_f << 1)
            player.a_rook_move = True
            self.sound_to_play.append("castle")

        # en passant
        elif (player.pieces[0] & square_i
            and not (square_f & self.total)
            and not ((square_i << 8) & square_f or (square_i >> 8) & square_f)
            and square_i >> 16 and (square_i << 16) & const.FULL_BOARD):
            if not color:
                for i in range(6):
                    if opposite_player.pieces[i] & (square_f << 8): opposite_player.pieces[i] ^= square_f << 8
            else:
                for i in range(6):
                    if opposite_player.pieces[i] & (square_f >> 8): opposite_player.pieces[i] ^= square_f >> 8

            self.sound_to_play.append("capture")

        for i in range(6):
            # changing the moving piece
            if square_i & player.pieces[i]:
                player.pieces[i] ^= square_i

                if promotion is True and i == 0:
                    promotion = self.gestionary.promoting(int(player.color == "b"), (square_f.bit_length() - 1) % 8)
                    if not promotion:
                        player.pieces[i] |= square_i
                        self.candidate_move[1] = 0
                        self.clicked_move = True
                        self.legal_moves = self.list_legal_moves[square_i.bit_length() - 1]
                        return

                if not promotion: player.pieces[i] |= square_f
                else:
                    player.pieces[promotion] |= square_f
                    self.sound_to_play.append("promotion")

                # rooks
                if i == 3:
                    if not (player.h_rook_move or const.NOT_H_FILE & square_i):
                        player.h_rook_move = True

                    if not (player.a_rook_move or const.NOT_A_FILE & square_i):
                        player.a_rook_move = True

                # king
                if i == 5:
                    if not player.king_move:
                        player.king_move = True

            # changing the opponent's piece if capture
            if square_f & opposite_player.pieces[i]:
                opposite_player.pieces[i] ^= square_f
                self.sound_to_play.append("capture")

        self.update_position()


    def update_position(self):
        # if not already calculated
        if self.index_position == len(self.list_position) - 1:
            self.list_position[-1][2] = copy.deepcopy(self.list_legal_moves)

        self.players[self.player_turn].last_piece_played = self.candidate_move
        for i in self.players: i.update_pos()
        self.total = 0
        for j in self.players:
            for i in j.pieces:
                self.total |= i

        # if not "current" position and another move has been played
        if self.index_position != len(self.list_position) - 1 and self.players[self.player_turn].last_piece_played != self.list_position[self.index_position+1][0][self.player_turn].last_piece_played:
            del self.list_position[self.index_position+1:]

        # if "current" position or another move has been played
        if not (self.index_position != len(self.list_position) - 1 and self.players[self.player_turn].last_piece_played == self.list_position[self.index_position+1][0][self.player_turn].last_piece_played):
            self.list_position.append([copy.deepcopy(self.players), self.total, 0, 0])


        self.left_click_down = 0
        self.left_click_up = 0
        self.candidate_move = [0,0]
        self.list_legal_moves = []
        self.legal_moves = 0
        self.index_position += 1
        self.player_turn = self.index_position % 2
