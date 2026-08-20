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
RANK = 0xFF
FILE = 0x0101010101010101
NOT_A_FILE = FULL_BOARD ^ FILE
NOT_H_FILE = FULL_BOARD ^ (FILE << 7)


# Coordinates
COLS = ['a','b','c','d','e','f','g','h']
RANKS = ['1','2','3','4','5','6','7','8']

# Square value
square_value = []
for rank in range(8):
    for file in range(8):
        d = min(rank, 7-rank, file, 7-file)

        if d == 3: square_value.append(50)
        elif d == 2: square_value.append(25)
        elif d == 1: square_value.append(10)
        else: square_value.append(5)


# Themes and colors
NMB_THEMES = 3
BLACK = [(118,150,86), (150, 77, 34), (111,115,210)]
WHITE = [(238,238,210), (238, 220, 151), (210,210,255)]
LAST_MOVE_WHITE = [(207,238,55), (255, 212, 59), (48, 206, 196)]
LAST_MOVE_BLACK = [(186,202,68), (209, 158, 5), (38, 175, 185)]
GREY = (50, 50, 50)
ILLEGAL_MOVE_COLOR = (255,0,0)

ILLEGAL_MOVE_DURATION = 100

# Players
HUMAN = "wb"

# Sounds
move_sound = pg.mixer.Sound("../Sounds/move.mp3")
illegal_sound = pg.mixer.Sound("../Sounds/illegal.mp3")
check_sound = pg.mixer.Sound("../Sounds/check.mp3")
capture_sound = pg.mixer.Sound("../Sounds/capture.mp3")
castle_sound = pg.mixer.Sound("../Sounds/castle.mp3")
promote_sound = pg.mixer.Sound("../Sounds/promote.mp3")
start_sound = pg.mixer.Sound("../Sounds/start.mp3")
end_sound = pg.mixer.Sound("../Sounds/end.mp3")
low_time_sound = pg.mixer.Sound("../Sounds/tenseconds.mp3")