"""
Toutes les fonctions en rapport avec le plateau de jeu
"""

import pygame as pg
import const
import mouse_keys as mk

pg.init()
theme_index = 1
board_origin = (0, 0)
font = pg.font.SysFont(None, 24)

# draws the board
def draw_board(gestionary):
    for col in range(8):
        for rank in range(8):
            square = 1 << (8 * rank + col)

            if (col+rank)%2 == 0:
                if square in gestionary.chess_game.players[gestionary.chess_game.player_turn ^ 1].last_piece_played or square == gestionary.chess_game.candidate_move[0]:
                    color = const.LAST_MOVE_WHITE[theme_index]
                else:
                    color = const.WHITE[theme_index]

            else:
                if  square in gestionary.chess_game.players[gestionary.chess_game.player_turn ^ 1].last_piece_played or square == gestionary.chess_game.candidate_move[0]:
                    color = const.LAST_MOVE_BLACK[theme_index]
                else:
                    color = const.BLACK[theme_index]

            # changes color for illegal move animation
            if gestionary.illegal_move_time and square == gestionary.chess_game.players[gestionary.chess_game.player_turn].pieces[5]:
                color = (const.ILLEGAL_MOVE_COLOR[0] + round((color[0] - const.ILLEGAL_MOVE_COLOR[0]) / const.ILLEGAL_MOVE_DURATION * (const.ILLEGAL_MOVE_DURATION - gestionary.illegal_move_time)),
                         const.ILLEGAL_MOVE_COLOR[1] + round((color[1] - const.ILLEGAL_MOVE_COLOR[1]) / const.ILLEGAL_MOVE_DURATION * (const.ILLEGAL_MOVE_DURATION - gestionary.illegal_move_time)),
                         const.ILLEGAL_MOVE_COLOR[2] + round((color[2] - const.ILLEGAL_MOVE_COLOR[2]) / const.ILLEGAL_MOVE_DURATION * (const.ILLEGAL_MOVE_DURATION - gestionary.illegal_move_time)))


            pg.draw.rect(gestionary.win, color, (col * const.SQUARE, rank * const.SQUARE, const.SQUARE, const.SQUARE))


            # highlight selected square
            if square & mk.mouse_to_coor(gestionary.mouse_pos):
                if square & gestionary.chess_game.total or gestionary.chess_game.candidate_move[0]:
                    pg.draw.rect(gestionary.win, (255, 255, 255), (col * const.SQUARE, rank * const.SQUARE, const.SQUARE, const.SQUARE), 2)


# draws the coordinates
def draw_coor(gestionary):
    for i, col in enumerate(const.COLS):
        color = const.WHITE if i%2 == 0 else const.BLACK
        text = font.render(col, True, color[theme_index])
        x = (i+1)*const.SQUARE - text.get_width() - 5
        y = 8*const.SQUARE - text.get_width() - 10

        gestionary.win.blit(text, (x, y))

    for i, rank in enumerate(const.RANKS[::-1]):
        color = const.WHITE if i%2 == 1 else const.BLACK
        text = font.render(rank, True, color[theme_index])
        y = i*const.SQUARE + 5
        x = 5

        gestionary.win.blit(text, (x, y))


# draws the pieces
def draw_pieces(gestionary):
    for square in split_bits(gestionary.chess_game.total):
        i = square.bit_length() - 1
        for k in range(6):
            if gestionary.chess_game.players[0].pieces[k] & square:
                if (gestionary.chess_game.players[0].pieces[k] & gestionary.chess_game.candidate_move[0]
                        and square == gestionary.chess_game.candidate_move[0]
                        and not gestionary.chess_game.candidate_move[1]
                        and gestionary.chess_game.left_click_down
                        and not gestionary.chess_game.left_click_up):
                    dx = sum(gestionary.previous_mouse_pos)//5 - gestionary.mouse_pos[0]
                    dir = 0 if sum(gestionary.previous_mouse_pos)//5 == gestionary.mouse_pos[0] else abs(dx)//dx
                    angle = dx if -30 < dx < 30 else 30 * dir

                    gestionary.win.blit(
                        pg.transform.rotate(
                            pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/white{const.PIECES[k]}.png"),
                                               (const.SQUARE * 1.1, const.SQUARE * 1.1)),
                            angle * 0.6),
                        (gestionary.mouse_pos[0] - const.SQUARE // 2, gestionary.mouse_pos[1] - const.SQUARE // 2))

                    break

                else:
                    gestionary.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/white{const.PIECES[k]}.png"),
                        (const.SQUARE, const.SQUARE)),
                        ((i%8)*const.SQUARE, (i//8)*const.SQUARE))

                    break


            elif gestionary.chess_game.players[1].pieces[k] & square:
                if (gestionary.chess_game.players[1].pieces[k] & gestionary.chess_game.candidate_move[0]
                        and square == gestionary.chess_game.candidate_move[0]
                        and not gestionary.chess_game.candidate_move[1]
                        and gestionary.chess_game.left_click_down
                        and not gestionary.chess_game.left_click_up):
                    dx = sum(gestionary.previous_mouse_pos) // 5 - gestionary.mouse_pos[0]
                    dir = 0 if sum(gestionary.previous_mouse_pos) // 5 == gestionary.mouse_pos[0] else abs(dx) // dx
                    angle = dx if -30 < dx < 30 else 30 * dir

                    gestionary.win.blit(
                        pg.transform.rotate(
                            pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/black{const.PIECES[k]}.png"),
                                               (const.SQUARE * 1.1, const.SQUARE * 1.1)),
                            angle * 0.6),
                        (gestionary.mouse_pos[0] - const.SQUARE // 2, gestionary.mouse_pos[1] - const.SQUARE // 2))

                    break

                else:
                    gestionary.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/black{const.PIECES[k]}.png"),
                        (const.SQUARE, const.SQUARE)),
                        ((i%8)*const.SQUARE, (i//8)*const.SQUARE))

                    break


# checks if a specific square is occupied by a piece
def occupied_square(gestionary, square):
    if gestionary.chess_game.total & square:
        return True
    return False


# blits all legal moves
def blit_legal_moves(gestionary, color, square_i):
    m_pos = mk.mouse_to_coor(gestionary.mouse_pos)
    for square in split_bits(gestionary.chess_game.legal_moves):
        i = square.bit_length() - 1

        facteur_grossissement = 1
        if square == m_pos:
            facteur_grossissement = 1.5

        #  capture                                  en passant
        if (occupied_square(gestionary, square) or (gestionary.chess_game.players[color].pieces[0] & square_i
                                                    and square_i >> 16 and (square_i << 16) & const.FULL_BOARD
                                                    and not ((square_i << 8) & square or (square_i >> 8) & square))):
            pg.draw.circle(gestionary.win, (168, 168, 168), ((i%8) * const.SQUARE + const.SQUARE // 2, (i//8) * const.SQUARE + const.SQUARE // 2),
                           const.SQUARE // 2 - 2, 3)
        else:
            pg.draw.circle(gestionary.win, (168, 168, 168), ((i%8) * const.SQUARE + const.SQUARE // 2, (i//8) * const.SQUARE + const.SQUARE // 2), 10*facteur_grossissement)


# displays whose turn it is
def write_player_turn(gestionary):
    t="White" if not gestionary.chess_game.player_turn else "Black"
    t += " is playing"
    police = pg.font.SysFont("Arial", int(const.SQUARE/3))
    texte = police.render(t, True, (255,255,255))
    gestionary.win.blit(texte, (const.WIDTH + 30, const.HEIGHT // 2 - 13))
    

# shows each player's legal time
def draw_timer(gestionary,color):
    pass


# splits bits into seperated bits
def split_bits(n):
    parts = []
    while n:
        # isolates the lowest bit
        bit = n & -n
        parts.append(bit)
        # removes the lowest bit
        n &= n - 1
    return parts

