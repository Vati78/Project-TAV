"""
Toutes les constantes du jeu
"""

import pygame as pg
pg.mixer.init()

# Board
SQUARE = 70
WIDTH = 8*SQUARE
HEIGHT = 8*SQUARE

# Coordinates
COLS = ['a','b','c','d','e','f','g','h']
RANKS = ['1','2','3','4','5','6','7','8']

# Themes and colors
NMB_THEMES = 2
BLACK = [(118,150,86), (150, 77, 34)]
WHITE = [(238,238,210), (238, 220, 151)]
dGREEN = (88,120,56)
dWHITE = (208,208,180)
GREY = (50, 50, 50)

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