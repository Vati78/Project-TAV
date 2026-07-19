"""
Toutes les constantes du jeu
"""

import pygame as pg
pg.mixer.init()

# Board
SQUARE = 70
WIDTH = 8*SQUARE
HEIGHT = 8*SQUARE

# Bitboards
FULL_BOARD = 0xFFFFFFFFFFFFFFFF
NOT_A_FILE = 0xfefefefefefefefe
NOT_H_FILE = 0x7f7f7f7f7f7f7f7f
RANK = 0xFF

# Coordinates
COLS = ['a','b','c','d','e','f','g','h']
RANKS = ['1','2','3','4','5','6','7','8']

# Pieces
PIECES = {0 : "Pawn",
          1 : "Knight",
          2 : "Bishop",
          3 : "Rook",
          4 : "Queen",
          5 : "King"}

# Themes and colors
NMB_THEMES = 3
BLACK = [(118,150,86), (150, 77, 34), (111,115,210)]
WHITE = [(238,238,210), (238, 220, 151), (210,210,255)]
LAST_MOVE_WHITE = [(207,238,55), (255, 212, 59), (48, 206, 196)]
LAST_MOVE_BLACK = [(186,202,68), (209, 158, 5), (38, 175, 185)]
GREY = (50, 50, 50)
ILLEGAL_MOVE_COLOR = (255,0,0)

ILLEGAL_MOVE_DURATION = 60

# Players
HUMAN = "wb" #None

#Sounds
move_sound = pg.mixer.Sound("../Sounds/move.mp3")
illegal_sound = pg.mixer.Sound("../Sounds/illegal.mp3")
check_sound = pg.mixer.Sound("../Sounds/check.mp3")
capture_sound = pg.mixer.Sound("../Sounds/capture.mp3")
castle_sound = pg.mixer.Sound("../Sounds/castle.mp3")
promote_sound = pg.mixer.Sound("../Sounds/promote.mp3")
start_sound = pg.mixer.Sound("../Sounds/start.mp3")
end_sound = pg.mixer.Sound("../Sounds/end.mp3")
low_time_sound = pg.mixer.Sound("../Sounds/tenseconds.mp3")