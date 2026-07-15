"""
Toutes les fonctions en rapport avec le plateau de jeu
"""

import pygame as pg
import const, pieces, mouse_keys as mk

pg.init()
theme_index = 1
board_origin = (0, 0)
font = pg.font.SysFont(None, 24)

# draws the board
def draw_board(gestionary):
    for col in range(8):
        for rank in range(8):
            # add if legal move
            if (col+rank)%2 == 0:
                pg.draw.rect(gestionary.win, const.WHITE[theme_index], (col*const.SQUARE, rank*const.SQUARE, const.SQUARE, const.SQUARE))
            else:
                pg.draw.rect(gestionary.win, const.BLACK[theme_index], (col*const.SQUARE, rank*const.SQUARE, const.SQUARE, const.SQUARE))

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
                gestionary.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/white{const.PIECES[k]}.png"),
                    (const.SQUARE, const.SQUARE)),
                    ((i%8)*const.SQUARE, (i//8)*const.SQUARE))
                break
            elif gestionary.chess_game.players[1].pieces[k] & square:
                gestionary.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/black{const.PIECES[k]}.png"),
                        (const.SQUARE, const.SQUARE)),
                        ((i%8)*const.SQUARE, (i//8)*const.SQUARE))
                break

#draws the selected piece
def draw_selected_piece(gestionary):
    if (gestionary.chess_game.candidate_move[0]
            and not gestionary.chess_game.candidate_move[1]
            and gestionary.chess_game.left_click_down
            and not gestionary.chess_game.left_click_up):

        # empties the square
        i = gestionary.chess_game.candidate_move[0].bit_length() - 1

        if ((i % 8) + (i // 8)) % 2 == 0:
            pg.draw.rect(gestionary.win, const.WHITE[theme_index],
                         ((i % 8) * const.SQUARE, (i // 8) * const.SQUARE, const.SQUARE, const.SQUARE))
        else:
            pg.draw.rect(gestionary.win, const.BLACK[theme_index],
                         ((i % 8) * const.SQUARE, (i // 8) * const.SQUARE, const.SQUARE, const.SQUARE))

        # blits coor if needed
        if i//8 == 7: # if the piece is on the last rank
            color = const.WHITE if (i%8) % 2 == 0 else const.BLACK
            text = font.render(const.COLS[i%8], True, color[theme_index])
            x = (i%8 + 1) * const.SQUARE - text.get_width() - 5
            y = 8 * const.SQUARE - text.get_width() - 10

            gestionary.win.blit(text, (x, y))

        if i%8 == 0:
            color = const.WHITE if (i//8)%2 == 1 else const.BLACK
            text = font.render(const.RANKS[7 - i//8], True, color[theme_index])
            y = (i//8) * const.SQUARE + 5
            x = 5

            gestionary.win.blit(text, (x, y))




        # blits the piece on mouse coor with movement animation
        dir = 0 if sum(gestionary.previous_mouse_pos)//5 == gestionary.mouse_pos[0] else abs(sum(gestionary.previous_mouse_pos)//5 - gestionary.mouse_pos[0])//(sum(gestionary.previous_mouse_pos)//5 - gestionary.mouse_pos[0])

        angle = sum(gestionary.previous_mouse_pos)//5 - gestionary.mouse_pos[0] if -30 < sum(gestionary.previous_mouse_pos)//5 - gestionary.mouse_pos[0] < 30 else 30*dir


        for k in range(6):
            if gestionary.chess_game.players[0].pieces[k] & gestionary.chess_game.candidate_move[0]:
                gestionary.win.blit(
                    pg.transform.rotate(
                        pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/white{const.PIECES[k]}.png"),
                        (const.SQUARE*1.1, const.SQUARE*1.1)),
                    angle*0.6),
                (gestionary.mouse_pos[0] - const.SQUARE // 2, gestionary.mouse_pos[1] - const.SQUARE // 2))

                break
            elif gestionary.chess_game.players[1].pieces[k] & gestionary.chess_game.candidate_move[0]:
                gestionary.win.blit(
                    pg.transform.rotate(
                        pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/black{const.PIECES[k]}.png"),
                        (const.SQUARE * 1.1, const.SQUARE * 1.1)),
                    angle*0.6),
                (gestionary.mouse_pos[0] - const.SQUARE // 2, gestionary.mouse_pos[1] - const.SQUARE // 2))

                break

# checks if a specific square is occupied by a piece, if so : returns the color
def color_and_occupied_square(gestionary, square):
    if gestionary.chess_game.total & square:
        return True
    return False

# blits all legal moves
def blit_legal_moves(gestionary):
        for square in split_bits(gestionary.chess_game.legal_moves):
            i = square.bit_length() - 1
            if color_and_occupied_square(gestionary, square):
                pg.draw.circle(gestionary.win, (168, 168, 168), ((i%8) * const.SQUARE + const.SQUARE // 2, (i//8) * const.SQUARE + const.SQUARE // 2),
                               const.SQUARE // 2 - 2, 3)
            else:
                pg.draw.circle(gestionary.win, (168, 168, 168), ((i%8) * const.SQUARE + const.SQUARE // 2, (i//8) * const.SQUARE + const.SQUARE // 2), 10)

# displays whose turn it is
def write_player_turn(gestionary):
    t="White" if not gestionary.chess_game.player_turn else "Black"
    t += " is playing"
    police = pg.font.SysFont("Arial", int(const.SQUARE/3))
    texte = police.render(t, True, (255,255,255))
    gestionary.win.blit(texte, (const.WIDTH + 30, 10))

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

