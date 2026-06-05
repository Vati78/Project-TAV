"""
Humain and Bot player classes
"""

import const
import board
import pieces


class Player:
    def __init__(self,color):
        self.color = color
        self.opposite_color = "w" if self.color == "b" else "b"
        self.king_pos = (7, 4) if self.color == "w" else (0, 4)
        self.king_move = None
        self.king_moved_yet = False
        self.a_rook_move = False
        self.h_rook_move = False
        self.s_castling_right = True
        self.l_castling_right = True
        self.castle = False

    def move(self, gestionary):
        rank_i = gestionary.chess_game.candidate_move[0]
        col_i = gestionary.chess_game.candidate_move[1]
        rank_f = gestionary.chess_game.candidate_move[2]
        col_f = gestionary.chess_game.candidate_move[3]

        gestionary.chess_game.candidate_move = [None, None, None, None]

        # for every move in the list of legal moves
        for rank, col, specific in gestionary.chess_game.legal_moves_list:
            # if the candidate move is in it
            if rank_f == rank and col_f == col:
                # if capture
                capture = board.color_and_occupied_square(gestionary, rank_f, col_f)

                # if the king is moved
                if isinstance(board.get_type(gestionary, rank_i, col_i), pieces.Piece.King):
                    self.king_pos = (rank_f, col_f)
                    if self.king_move is None: self.king_move = gestionary.chess_game.index_position+1
                    self.s_castling_right = False
                    self.l_castling_right = False
                else:
                    if self.king_move is not None:
                        if self.king_move-1 <= gestionary.chess_game.index_position:
                            self.king_move = None
                            self.king_moved_yet = False


                # plays the move
                gestionary.chess_game.play_move(rank_i, col_i, rank_f, col_f, specific)

                # plays the sound
                if gestionary.chess_game.in_check(self.opposite_color): const.check_sound.play()
                elif capture: const.capture_sound.play()
                else: const.move_sound.play()

                # update position, index_position and list_position
                gestionary.chess_game.index_position += 1
                del gestionary.chess_game.list_position[gestionary.chess_game.index_position:]
                gestionary.chess_game.list_position.append([row[:] for row in gestionary.chess_game.position])
                gestionary.chess_game.update_position()

        else:
            for rank, col, specific in gestionary.chess_game.illegal_moves_list:
                # elif it is in the illegal moves list
                if rank_f == rank and col_f == col:
                    # plays the sound
                    const.illegal_sound.play()

        gestionary.chess_game.legal_moves_list = []
        gestionary.chess_game.illegal_moves_list = []

class Bot:
    def __init__(self, color):
        self.color = color
        self.king_pos = (7, 4) if self.color == "w" else (0, 4)
        self.king_move = None
        self.king_moved_yet = False
        self.a_rook_move = False
        self.h_rook_move = False
        self.s_castling_right = True
        self.l_castling_right = True
        self.castle = False

    def return_move(self, gestionary):
        pass