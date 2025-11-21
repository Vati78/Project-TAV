"""
Toutes les interactions de la souris et du clavier
"""

import pygame as pg
import main
import game
import const

# translates mouse position to chess coordinates
def mouse_to_coor(m_pos):
    m_x, m_y = m_pos # transcripts the pos tuple into x and y coordinates
    if 0 <= m_x <= const.WIDTH and 0 <= m_y <= const.HEIGHT: # if the pixel coordinate is on the chess board
        return (m_y//const.SQUARE, m_x//const.SQUARE) # returns gives the column and row number (starting at 0)
    else: # else
        return None # returns no coordinates
