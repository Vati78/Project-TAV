"""
Toutes les fonctions qui gèrent le déroulement de la partie.
"""

import const
import pieces
import player_bot as pb
import board
import copy

import math


class Game:
    def __init__(self, gestionary):
        self.gestionary = gestionary

        self.players = [pb.Player("w") if "w" in const.HUMAN else pb.Bot("w"), pb.Player("b") if "b" in const.HUMAN else pb.Bot("b")]
        self.index_last_capture_or_pawn_move = 0
        ################################################
        self.total = self.players[0].pieces_total|self.players[1].pieces_total
        self.index_position = 0
        #                      players                      total              list_legal_moves        check          sound
        #self.list_position = [[copy.deepcopy(self.players), self.total,        0,                      False,         0]]
        self.list_position = []
        ################################################
        self.player_turn = self.index_position % 2
        ################################################
        self.clicked_move = False
        self.double_click = False
        self.left_click_down = 0
        self.left_click_up = 0
        ################################################
        self.candidate_move = [0, 0]
        self.check = False
        self.list_legal_moves = []
        self.legal_moves = 0
        self.illegal_move = False
        #################################################
        self.sound_to_play = 0
        ################################################
        self.result = None


    def status_to_key(self):
        # white
        # black
        # total, legal moves, check
        return (self.players[0].pieces[0],
                self.players[0].pieces[1],
                self.players[0].pieces[2],
                self.players[0].pieces[3],
                self.players[0].pieces[4],
                self.players[0].pieces[5],
                self.players[0].pieces_total,
                self.players[0].s_castling_right,
                self.players[0].l_castling_right,
                self.players[0].castled,
                self.players[0].last_piece_played,
                self.players[0].last_capture_or_pawn_move_index,
                self.players[1].pieces[0],
                self.players[1].pieces[1],
                self.players[1].pieces[2],
                self.players[1].pieces[3],
                self.players[1].pieces[4],
                self.players[1].pieces[5],
                self.players[1].pieces_total,
                self.players[1].s_castling_right,
                self.players[1].l_castling_right,
                self.players[1].castled,
                self.players[1].last_piece_played,
                self.players[1].last_capture_or_pawn_move_index,
                self.total,
                self.list_legal_moves.copy(),
                self.check,
                self.sound_to_play)


    def key_to_status(self, key):
        self.players[0].pieces[0] = key[0]
        self.players[0].pieces[1] = key[1]
        self.players[0].pieces[2] = key[2]
        self.players[0].pieces[3] = key[3]
        self.players[0].pieces[4] = key[4]
        self.players[0].pieces[5] = key[5]
        self.players[0].pieces_total = key[6]
        self.players[0].s_castling_right = key[7]
        self.players[0].l_castling_right = key[8]
        self.players[0].castled = key[9]
        self.players[0].last_piece_played = key[10]
        self.players[0].last_capture_or_pawn_move_index = key[11]
        self.players[1].pieces[0] = key[12]
        self.players[1].pieces[1] = key[13]
        self.players[1].pieces[2] = key[14]
        self.players[1].pieces[3] = key[15]
        self.players[1].pieces[4] = key[16]
        self.players[1].pieces[5] = key[17]
        self.players[1].pieces_total = key[18]
        self.players[1].s_castling_right = key[19]
        self.players[1].l_castling_right = key[20]
        self.players[1].castled = key[21]
        self.players[1].last_piece_played = key[22]
        self.players[1].last_capture_or_pawn_move_index = key[23]
        self.total = key[24]
        self.list_legal_moves = key[25].copy()
        self.check = key[26]
        self.sound_to_play = key[27]


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
                    if self.check:
                        self.illegal_move = True
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

        if nb_checks:
            self.sound_to_play = 4
            self.check = True

        for j in range(6):
            # if king
            if j == 5:
                square = self.players[color].pieces[5]
                i = square.bit_length() - 1
                legal_moves = pieces.Piece().King(color).legal_moves(self.gestionary, square)

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


        # checkmate and stalemate
        if all(move == 0 for move in self.list_legal_moves):
            self.sound_to_play = 5
            if nb_checks == 0:
                self.result = 0
            else:
                self.result = 2*self.player_turn - 1


    def play_move(self, square_i, square_f, color, promotion=False):
        player = self.players[color]
        opposite_player = self.players[color ^ 1]

        # short castle
        if player.pieces[5] == square_i and square_f == square_i << 2:
            player.pieces[3] = player.pieces[3] ^ (square_f << 1) | (square_f >> 1)
            player.s_castling_right = False
            player.castled = True
            self.sound_to_play = max(self.sound_to_play, 2)

        # long castle
        elif player.pieces[5] == square_i and square_f == square_i >> 2:
            player.pieces[3] = player.pieces[3] ^ (square_f >> 2) | (square_f << 1)
            player.l_castling_right = False
            player.castled = True
            self.sound_to_play = max(self.sound_to_play, 2)

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

            self.sound_to_play = max(self.sound_to_play, 1)
            self.index_last_capture_or_pawn_move = self.index_position

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
                    self.sound_to_play = max(self.sound_to_play, 3)
                    self.index_last_capture_or_pawn_move = self.index_position

                # pawns
                if i == 0:
                    self.index_last_capture_or_pawn_move = self.index_position

                # rooks
                if i == 3:
                    if not const.NOT_H_FILE & square_i:
                        player.s_castling_right = False

                    if not const.NOT_A_FILE & square_i:
                        player.l_castling_right = False

                # king
                if i == 5:
                    player.s_castling_right = False
                    player.l_castling_right = False

            # changing the opponent's piece if capture
            if square_f & opposite_player.pieces[i]:
                opposite_player.pieces[i] ^= square_f
                self.sound_to_play = max(self.sound_to_play, 1)
                self.index_last_capture_or_pawn_move = self.index_position


        self.update_position(square_i, square_f)


    def update_position(self, square_i, square_f):

        self.players[self.player_turn].last_piece_played = [square_i, square_f]
        for i in self.players: i.update_pos()
        self.total = 0
        for j in self.players:
            for i in j.pieces:
                self.total |= i

        # if not "current" position and another move has been played
        if self.index_position != len(self.list_position) - 1 and self.players[self.player_turn].last_piece_played != self.list_position[self.index_position+1][12*self.player_turn + 10]:
            del self.list_position[self.index_position+1:]

        self.left_click_down = 0
        self.left_click_up = 0
        self.candidate_move = [0,0]
        self.list_legal_moves = []
        self.legal_moves = 0
        self.check = False
        self.index_position += 1
        self.player_turn ^= 1

        # updates list_legal_moves and check
        self.get_all_legal_moves(self.player_turn)

        self.list_position.append(self.status_to_key())


        if self.result is None:
            # 3-fold repetition
            nb_same_position = 1
            for i, position in enumerate(self.list_position[self.index_position%2:-1:2]):
                if (position[:6] == self.list_position[-1][:6]
                        and position[12:18] == self.list_position[-1][12:18]
                        and position[25] == self.list_legal_moves):
                    nb_same_position += 1

            if nb_same_position >= 3:
                self.result = 0

            # 50-move rule
            if self.index_position - self.index_last_capture_or_pawn_move >= 100:
                self.result = 0


    def evaluation(self) -> int:
        # game end
        if self.result:
            return self.result * math.inf

        e = 0
        """
        isolated_pawns_p = 0
        doubled_pawns_p = 0
        material_p = 0
        center_control_p = 0
        center_control_legal_moves_p = 0
        enemy_territory_control_p = 0
        piece_development_p = 0
        """

        nb_pawns = [[], []]
        for i in range(2):
            for j in range(8):
                nb_pawns[i].append((self.players[i].pieces[0] & (const.FILE << j)).bit_count())

        isolated_pawns = [[False for _ in range(8)], [False for _ in range(8)]]
        for i in range(2):
            for j in range(8):
                if j == 0:
                    if not nb_pawns[i][1]: isolated_pawns[i][0] = True
                elif j == 7:
                    if not nb_pawns[i][6]: isolated_pawns[i][7] = True
                else:
                    if not (nb_pawns[i][j - 1] or nb_pawns[i][j + 1]): isolated_pawns[i][j] = True

        for index in range(2):
            player = self.players[index]
            coeff = -2 * index + 1

            # calculates legal moves for other player
            if index != self.player_turn:
                c_check = self.check
                c_list_legal_moves = self.list_legal_moves
                self.get_all_legal_moves(index)


            for i in range(8):
                if isolated_pawns[index][i]:
                    # isolated pawns
                    e -= coeff * 50

                # doubled (or tripled) pawns
                if nb_pawns[index][i] > 1:
                    e -= coeff * 5 * (nb_pawns[index][i] ** 3)


            for i in range(5):
                player_pieces = player.pieces[i]

                # material
                e += coeff * player_pieces.bit_count() * pieces.get_type(i, index).value


                for piece in board.split_bits(player_pieces):
                    square_index = piece.bit_length() - 1

                    # center control
                    e += coeff * const.square_value[square_index]

                    for move in board.split_bits(self.list_legal_moves[square_index]):
                        move_index = move.bit_length() - 1

                        # center control
                        e += coeff * const.square_value[move_index]

                        # enemy territory control
                        d = abs(7*index - move_index//8)
                        if d <= 3:
                            e += coeff * (40 - 10*d)


                    # except pawns
                    if i:
                        # piece development
                        e += coeff * 10 * ((player_pieces ^ self.list_position[0][12*index+i]).bit_count()//2)

                        # rook or queen
                        if i in (3, 4):
                            file = (piece.bit_length() - 1)%8
                            if not player.pieces[0] & (const.FILE << file):
                                nb_opposite_pawns = nb_pawns[index ^ 1][file]
                                # attacks isolated pawns
                                if isolated_pawns[index ^ 1][file]:
                                    e += coeff * 75 * nb_opposite_pawns
                                # (semi) open files
                                elif nb_opposite_pawns < 2:
                                    e += coeff * 60 * (2 >> nb_opposite_pawns)

            # castle
            if player.castled:
                e += coeff * 150
            elif not (player.s_castling_right or player.l_castling_right):
                e -= coeff * 200

            # re-changes variables to normal status
            if index != self.player_turn:
                self.check = c_check
                self.list_legal_moves = c_list_legal_moves

        """
        print("Material :", material_p)
        e += material_p
        print("Isolated pawns :", isolated_pawns_p)
        e += isolated_pawns_p
        print("Doubled pawns :", doubled_pawns_p)
        e += doubled_pawns_p
        print("Center control :", center_control_p)
        e += center_control_p
        print("Center control legal moves :", center_control_legal_moves_p)
        e += center_control_legal_moves_p
        print("Enemy control legal moves :", enemy_territory_control_p)
        e += enemy_territory_control_p
        print("Piece development :", piece_development_p)
        e += piece_development_p"""

        return e
