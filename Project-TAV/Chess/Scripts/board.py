"""
Toutes les fonctions en rapport avec le plateau de jeu
"""

import pygame as pg
import main
import const
import game
import pieces

theme_index = 1

# draws the board
def draw_board():
    for col in range(8): # for every column
        for rank in range(8): # for every rank
            if (col+rank) % 2 == 0: # if the sum of the indices is even
                pg.draw.rect(main.win, const.WHITE[theme_index], (col*const.SQUARE, rank*const.SQUARE, const.SQUARE, const.SQUARE))
            else: # else
                pg.draw.rect(main.win, const.BLACK[theme_index], (col * const.SQUARE, rank * const.SQUARE, const.SQUARE, const.SQUARE))

# draws the pieces
def draw_pieces():
    for rank in enumerate(main.chess_game.position): # goes through every rank
        for col in enumerate(rank[1]): # goes through every column
            if col[1] != " ": # if the square is not empty
                main.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces/{col[1]}.png"), (const.SQUARE, const.SQUARE)), ((col[0])*const.SQUARE, (rank[0])*const.SQUARE))

# checks if a specific square is occupied by a piece, if so : returns the color
def color_and_occupied_square(rank, col):
    if main.chess_game.position[rank][col] == " ":
        return False
    else:
        return main.chess_game.position[rank][col][0]

# returns the type of piece /!\ Make sure there is a piece !!!
def get_type(rank, col):
    piece = main.chess_game.position[rank][col]

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

# blits all legal moves
def blit_legal_moves(rank, col):
    for move in get_type(rank, col).legal_moves(rank, col):
        if color_and_occupied_square(col, rank):
            pg.draw.circle(main.win, (168, 168, 168), (col * const.SQUARE + const.SQUARE // 2, rank * const.SQUARE + const.SQUARE // 2),
                           const.SQUARE // 2 - 2, 3)
        else:
            pg.draw.circle(main.win, (168, 168, 168), (col * const.SQUARE + const.SQUARE // 2, rank * const.SQUARE + const.SQUARE // 2), 10)

def write_player_turn():
    t="White" if main.chess_game.player_turn == "w" else "Black"
    t += " is playing"
    police = pg.font.SysFont("Arial", int(const.SQUARE/3))
    texte = police.render(t, True, (255,255,255))
    main.win.blit(texte, (const.WIDTH + 30, 10))

