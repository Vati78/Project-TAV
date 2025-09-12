import pygame as pg
import math

for event in pg.event.get():
    if event.type == pg.QUIT:
        running = False