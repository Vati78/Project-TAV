"""
Toutes les constantes du jeu
"""

import pygame as pg
pg.mixer.init()

# Board
SQUARE = 70
WIDTH = 8*SQUARE
HEIGHT = 8*SQUARE

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
check_sound = pg.mixer.Sound("../Sounds/check.mp3")
