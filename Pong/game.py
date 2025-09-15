import pygame as pg
import math
import random as rd
import os
import time


pg.init()

os.chdir(os.path.abspath(__file__)[0:-8])

"""
Constants and initialization
"""

WIDTH = 1000
HEIGHT = 500

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Ping-Pong")

GREEN = (118,150,86)
dGREEN = (88,120,56)
WHITE = (238,238,210)
dWHITE = (208,208,180)
GREY = (50, 50, 50)
RED = (255, 20, 20)

win.blit(pg.image.load(f"Images/terrain.png"), (0, 0))

class Ball:
    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx_i = vx
        self.vy_i = vy
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def rebond(self, coeff, loop, touche_exterieur=False):
        bord = -1 if touche_exterieur else 1
        signe_x = -1 if self.vx < 0 else 1
        signe_y = -1 if self.vy < 0 else 1
        sens = -1 if self.vy > 0 and coeff > 0 else 1

        self.vx = - self.vx_i * bord * (1 + loop/1000) * signe_x
        self.vy =  self.vy * bord + coeff*0.1#*sens


    def draw(self):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vx
        self.y += self.vy


class Plateform:
    def __init__(self, x, y, lx, ly, ymax, ymin, color):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.vy = 0
        self.ymax = ymax
        self.ymin = ymin
        self.vmax = 10
        self.color = color

    def move(self, vy):
        vy *= self.vmax
        if self.ymin < self.y + vy < self.y + vy + self.ly < self.ymax:
            self.y += vy
            self.vy = vy

    def reset(self):
        self.vy = 0

    def draw(self, index):
        win.blit(pg.transform.scale(pg.image.load(f"Images/Platforme_{index+1}.png"), (self.lx, self.ly)),
                 (self.x, self.y))

def interactions(players, balle, n):
    if balle.vx < 0:
        #if balle.x <= players[0].x + players[0].lx and math.sqrt(
         #           (balle.y - players[0].y) ** 2 + (balle.x - players[0].x) ** 2) <= balle.radius:
          #  balle.rebond(0, n, True)
        if (players[0].y <= balle.y <= players[0].y + players[0].ly
                and balle.x - balle.radius <= players[0].x + players[0].lx):
            balle.rebond(players[0].vy, n)
        elif players[0].y - balle.radius + 1 <= balle.y <= players[0].y:
            if math.sqrt(
                    (balle.y - players[0].y) ** 2 + (balle.x - (players[0].x + players[0].lx)) ** 2) <= balle.radius:
                balle.rebond(players[0].vy, n)
        elif players[0].y + players[0].ly <= balle.y <= players[0].y + players[0].ly + balle.radius:
            if math.sqrt((balle.y - (players[0].y + players[0].ly)) ** 2 + (
                    balle.x - (players[0].x + players[0].lx)) ** 2) <= balle.radius:
                balle.rebond(players[0].vy, n)

    if balle.vx > 0 and balle.x <= players[1].x:
        if (players[1].y <= balle.y <= players[1].y + players[1].ly
                and balle.x + balle.radius >= players[1].x):
            balle.rebond(players[1].vy, n)
        elif players[1].y - balle.radius + 1 <= balle.y <= players[1].y:
            if math.sqrt((balle.y - players[1].y) ** 2 + (balle.x - players[1].x) ** 2) <= balle.radius:
                balle.rebond(players[1].vy, n)
        elif players[1].y + players[1].ly <= balle.y <= players[1].y + players[1].ly + balle.radius:
            if math.sqrt(
                    (balle.y - (players[1].y + players[1].ly)) ** 2 + (balle.x - players[1].x) ** 2) <= balle.radius:
                balle.rebond(players[1].vy, n)

    if balle.y - balle.radius <= 20 or balle.y + balle.radius >= HEIGHT-20:
        balle.rebond(0, n, True)

    if balle.x - balle.radius < 0 or balle.x + balle.radius > WIDTH:
        return False

    return True


def main():
    players = [Plateform(100, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 20, GREEN), Plateform(WIDTH-110, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 20, GREEN)]
    balle = Ball(WIDTH//2, HEIGHT//2 - 10, 5, 0, 40, RED)
    n = 0
    running = True

    balle.vy = rd.randint(-10, 10)
    clock = pg.time.Clock()

    while running:
        n += 1

        for i in players: i.reset()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()

        if keys[pg.K_DOWN]:
            players[0].move(1)

        if keys[pg.K_UP]:
            players[0].move(-1)

        if keys[pg.K_RIGHT]:
            pass

        balle.move()
        players[1].y = balle.y - players[1].ly//2

        if running:
            running = interactions(players, balle, n)

        # display
        win.blit(pg.image.load(f"Images/terrain.png"), (0, 0))
        balle.draw()
        for i in enumerate(players): i[1].draw(i[0])

        pg.display.update()
        clock.tick(120)

main()


