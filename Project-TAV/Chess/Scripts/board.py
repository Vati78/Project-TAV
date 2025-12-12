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
    for col in range(8): # for every column
        for rank in range(8): # for every rank
            if (col+rank) % 2 == 0: # if the sum of the indices is even
                pg.draw.rect(gestionary.win, const.WHITE[theme_index], (col*const.SQUARE, rank*const.SQUARE, const.SQUARE, const.SQUARE))
            else: # else
                pg.draw.rect(gestionary.win, const.BLACK[theme_index], (col * const.SQUARE, rank * const.SQUARE, const.SQUARE, const.SQUARE))

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
    coor = None
    move_piece = False
    if gestionary.chess_game.left_click_down and not gestionary.chess_game.left_click_up:
        coor = gestionary.chess_game.left_click_down

    for rank in enumerate(gestionary.chess_game.position): # goes through every rank
        for col in enumerate(rank[1]): # goes through every column
            if col[1] != " ": # if the square is not empty
                if (rank[0], col[0]) == coor and mk.mouse_to_coor(gestionary.mouse_pos) is not None:
                    move_piece = True
                else:
                    gestionary.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces/{col[1]}.png"),
                                                           (const.SQUARE, const.SQUARE)),
                                        ((col[0])*const.SQUARE, (rank[0])*const.SQUARE))

    if move_piece:
        gestionary.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces/{gestionary.chess_game.position[coor[0]][coor[1]]}.png"),
                                               (const.SQUARE, const.SQUARE)),
                            (gestionary.mouse_pos[0] - const.SQUARE / 2, gestionary.mouse_pos[1] - const.SQUARE / 2))

# checks if a specific square is occupied by a piece, if so : returns the color
def color_and_occupied_square(gestionary, rank, col):
    if gestionary.chess_game.position[rank][col] == " ":
        return False
    else:
        return gestionary.chess_game.position[rank][col][0]

# returns the type of piece /!\ Make sure there is a piece !!!
def get_type(gestionary, rank, col):
    piece = gestionary.chess_game.position[rank][col]

    if piece[1] == "P":
        return pieces.Piece.Pawn(piece[0])
    elif piece[1] == "N":
        return pieces.Piece.Knight(piece[0])
    elif piece[1] == "R":
        return pieces.Piece.Rook(piece[0])
    elif piece[1] == "B":
        return pieces.Piece.Bishop(piece[0])
    elif piece[1] == "K":
        return pieces.Piece.King(piece[0])
    elif piece[1] == "Q":
        return pieces.Piece.Queen(piece[0])
    else:
        return False

# blits all legal moves
def blit_legal_moves(gestionary):
    for move in gestionary.chess_game.legal_moves_list:
        (col, rank, _) = move
        if color_and_occupied_square(gestionary, col, rank):
            pg.draw.circle(gestionary.win, (168, 168, 168), (rank * const.SQUARE + const.SQUARE // 2, col * const.SQUARE + const.SQUARE // 2),
                           const.SQUARE // 2 - 2, 3)
        else:
            pg.draw.circle(gestionary.win, (168, 168, 168), (rank * const.SQUARE + const.SQUARE // 2, col * const.SQUARE + const.SQUARE // 2), 10)

def write_player_turn(gestionary):
    t="White" if gestionary.chess_game.player_turn == "w" else "Black"
    t += " is playing"
    police = pg.font.SysFont("Arial", int(const.SQUARE/3))
    texte = police.render(t, True, (255,255,255))
    gestionary.win.blit(texte, (const.WIDTH + 30, 10))

