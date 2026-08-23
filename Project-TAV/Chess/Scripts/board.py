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


# loads the sprites
def load_sprites_unscaled(gestionary):
    const.WHITE_PIECES_UNSCALED = (pg.image.load(f"../Sprites/Pieces_bitboards/whitePawn.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/whiteKnight.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/whiteBishop.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/whiteRook.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/whiteQueen.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/whiteKing.png").convert_alpha(gestionary.win))

    const.BLACK_PIECES_UNSCALED = (pg.image.load(f"../Sprites/Pieces_bitboards/blackPawn.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/blackKnight.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/blackBishop.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/blackRook.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/blackQueen.png").convert_alpha(gestionary.win),
                            pg.image.load(f"../Sprites/Pieces_bitboards/blackKing.png").convert_alpha(gestionary.win))

def load_sprites_scaled(gestionary):
    const.WHITE_PIECES_SCALED  = (pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/whitePawn.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/whiteKnight.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/whiteBishop.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/whiteRook.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/whiteQueen.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/whiteKing.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)))

    const.BLACK_PIECES_SCALED = (pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/blackPawn.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/blackKnight.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/blackBishop.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/blackRook.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/blackQueen.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)),
                           pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/blackKing.png").convert_alpha(gestionary.win),
                                              (const.SQUARE, const.SQUARE)))


# draws the board
def draw_board(gestionary):
    # white down, black up
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
            if gestionary.illegal_move_time[0] and square == gestionary.chess_game.players[gestionary.illegal_move_time[1]].pieces[5]:
                color = (const.ILLEGAL_MOVE_COLOR[0] + round((color[0] - const.ILLEGAL_MOVE_COLOR[0]) / const.ILLEGAL_MOVE_DURATION * (const.ILLEGAL_MOVE_DURATION - gestionary.illegal_move_time[0])),
                         const.ILLEGAL_MOVE_COLOR[1] + round((color[1] - const.ILLEGAL_MOVE_COLOR[1]) / const.ILLEGAL_MOVE_DURATION * (const.ILLEGAL_MOVE_DURATION - gestionary.illegal_move_time[0])),
                         const.ILLEGAL_MOVE_COLOR[2] + round((color[2] - const.ILLEGAL_MOVE_COLOR[2]) / const.ILLEGAL_MOVE_DURATION * (const.ILLEGAL_MOVE_DURATION - gestionary.illegal_move_time[0])))


            if gestionary.invert_position:
                pg.draw.rect(gestionary.win, color,
                ((7 - col) * const.SQUARE, (7 - rank) * const.SQUARE, const.SQUARE, const.SQUARE))
            else:
                pg.draw.rect(gestionary.win, color,
                (col * const.SQUARE, rank * const.SQUARE, const.SQUARE, const.SQUARE))


            # highlight selected square
            if square & mk.mouse_to_coor(gestionary.mouse_pos, gestionary.invert_position):
                    if square & gestionary.chess_game.total or gestionary.chess_game.candidate_move[0]:
                        if gestionary.invert_position:
                            pg.draw.rect(gestionary.win, (255, 255, 255),
                                         ((7-col) * const.SQUARE, (7-rank) * const.SQUARE, const.SQUARE, const.SQUARE),
                                         2)
                        else:
                            pg.draw.rect(gestionary.win, (255, 255, 255),
                            (col * const.SQUARE, rank * const.SQUARE, const.SQUARE, const.SQUARE),
                            2)


# draws the coordinates
def draw_coor(gestionary):
    for i, col in enumerate(const.COLS):
        color = const.WHITE if i%2 == 0 else const.BLACK
        text = font.render(col, True, color[theme_index])
        x = (i+1)*const.SQUARE - text.get_width() - 5
        y = 8*const.SQUARE - text.get_width() - 10

        gestionary.win.blit(text, (x, y))

    for i, rank in enumerate(const.RANKS[::-1]):
        x = 5
        if gestionary.invert_position:
            y = (7-i) * const.SQUARE + 5
            color = const.WHITE if i%2 == 0 else const.BLACK
        else:
            y = i*const.SQUARE + 5
            color = const.WHITE if i%2 == 1 else const.BLACK

        text = font.render(rank, True, color[theme_index])

        gestionary.win.blit(text, (x, y))


# draws the pieces
def draw_pieces(gestionary):
    selected_piece = None
    for square in split_bits(gestionary.chess_game.total):
        i = square.bit_length() - 1
        for k in range(6):
            if gestionary.chess_game.players[0].pieces[k] & square:
                if (gestionary.chess_game.players[0].pieces[k] & gestionary.chess_game.candidate_move[0]
                        and square == gestionary.chess_game.candidate_move[0]
                        and not gestionary.chess_game.candidate_move[1]
                        and gestionary.chess_game.left_click_down
                        and not gestionary.chess_game.left_click_up):

                    selected_piece = (0, k)
                    break

                else:
                    if gestionary.invert_position:
                        gestionary.win.blit(const.WHITE_PIECES_SCALED [k], ((7 - i%8)*const.SQUARE, (7 - i//8)*const.SQUARE))
                    else:
                        gestionary.win.blit(const.WHITE_PIECES_SCALED [k], ((i%8)*const.SQUARE, (i//8)*const.SQUARE))
                    break


            elif gestionary.chess_game.players[1].pieces[k] & square:
                if (gestionary.chess_game.players[1].pieces[k] & gestionary.chess_game.candidate_move[0]
                        and square == gestionary.chess_game.candidate_move[0]
                        and not gestionary.chess_game.candidate_move[1]
                        and gestionary.chess_game.left_click_down
                        and not gestionary.chess_game.left_click_up):

                    selected_piece = (1, k)
                    break

                else:
                    if gestionary.invert_position:
                        gestionary.win.blit(const.BLACK_PIECES_SCALED[k], ((7 - i%8)*const.SQUARE, (7 - i//8)*const.SQUARE))
                    else:
                        gestionary.win.blit(const.BLACK_PIECES_SCALED[k], ((i%8)*const.SQUARE, (i//8)*const.SQUARE))
                    break

    # blit selected piece
    if selected_piece is not None:
        if selected_piece[0] == 0:
            dx = sum(gestionary.previous_mouse_pos) // 5 - gestionary.mouse_pos[0]
            dir = 0 if sum(gestionary.previous_mouse_pos) // 5 == gestionary.mouse_pos[0] else abs(dx) // dx
            angle = dx if -30 < dx < 30 else 30 * dir

            gestionary.win.blit(
                pg.transform.rotate(
                    pg.transform.scale(
                        const.WHITE_PIECES_UNSCALED[selected_piece[1]],
                        (const.SQUARE * 1.1, const.SQUARE * 1.1)),
                    angle * 0.6),
                (gestionary.mouse_pos[0] - const.SQUARE // 2, gestionary.mouse_pos[1] - const.SQUARE // 2))

        else:
            dx = sum(gestionary.previous_mouse_pos) // 5 - gestionary.mouse_pos[0]
            dir = 0 if sum(gestionary.previous_mouse_pos) // 5 == gestionary.mouse_pos[0] else abs(dx) // dx
            angle = dx if -30 < dx < 30 else 30 * dir

            gestionary.win.blit(
                pg.transform.rotate(
                    pg.transform.scale(
                        const.BLACK_PIECES_UNSCALED[selected_piece[1]],
                        (const.SQUARE * 1.1, const.SQUARE * 1.1)),
                    angle * 0.6),
                (gestionary.mouse_pos[0] - const.SQUARE // 2, gestionary.mouse_pos[1] - const.SQUARE // 2))


# checks if a specific square is occupied by a piece
def occupied_square(gestionary, square):
    if gestionary.chess_game.total & square:
        return True
    return False


# blits all legal moves
def blit_legal_moves(gestionary, color, square_i):
    m_pos = mk.mouse_to_coor(gestionary.mouse_pos, gestionary.invert_position)
    for square in split_bits(gestionary.chess_game.legal_moves):
        i = square.bit_length() - 1

        facteur_grossissement = 1
        if square == m_pos:
            facteur_grossissement = 1.5

        #  capture                                  en passant
        if (occupied_square(gestionary, square) or (gestionary.chess_game.players[color].pieces[0] & square_i
                                                    and square_i >> 16 and (square_i << 16) & const.FULL_BOARD
                                                    and not ((square_i << 8) & square or (square_i >> 8) & square))):
            if gestionary.invert_position:
                pg.draw.circle(gestionary.win, (168, 168, 168), ((7-i%8) * const.SQUARE + const.SQUARE // 2, (7-i//8) * const.SQUARE + const.SQUARE // 2),
                               const.SQUARE // 2 - 2, 3)
            else:
                pg.draw.circle(gestionary.win, (168, 168, 168), ((i%8) * const.SQUARE + const.SQUARE // 2, (i // 8) * const.SQUARE + const.SQUARE // 2),
                               const.SQUARE // 2 - 2, 3)
        else:
            if gestionary.invert_position:
                pg.draw.circle(gestionary.win, (168, 168, 168), ((7-i%8) * const.SQUARE + const.SQUARE // 2, (7-i//8) * const.SQUARE + const.SQUARE // 2), 10*facteur_grossissement)
            else:
                pg.draw.circle(gestionary.win, (168, 168, 168), ((i%8) * const.SQUARE + const.SQUARE // 2, (i // 8) * const.SQUARE + const.SQUARE // 2),
                               10 * facteur_grossissement)


# displays whose turn it is
def write_player_turn(gestionary):
    t="White" if not gestionary.chess_game.player_turn else "Black"
    t += " is playing"
    police = pg.font.SysFont("Arial", int(const.SQUARE/3))
    texte = police.render(t, True, (255,255,255))
    gestionary.win.blit(texte, (const.WIDTH + 30, const.HEIGHT // 2 - 13))
    

# shows each player's legal time
def draw_timer(gestionary, color):
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

