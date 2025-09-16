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

    def rebond(self, p_vy, loop, coeff, touche_exterieur=False): #p_vy: vy de la plateforme; touche_exterieur: haut ou bas de l'écran
        bord = -1 if touche_exterieur else 1
        signe_x = -1 if self.vx < 0 else 1
        #signe_y = -1 if self.vy < 0 else 1
        #sens = -1 if self.vy > 0 and p_vy > 0 else 1
        if coeff != 0:
            A = coeff/self.radius * math.pi/2
            self.vx = -math.cos(2*A)*self.vx+sin(2*A)*self.vy
            self.vy
        else:
            self.vx = - self.vx_i * bord * (1 + loop/2000) * signe_x
            self.vy =  self.vy * bord + p_vy*0.1 #*sens


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
        if balle.x <= players[0].x + players[0].lx and balle.x - balle.vx <= players[0].x + players[0].lx:
            return False
        elif (players[0].y <= balle.y <= players[0].y + players[0].ly
                and balle.x - balle.radius <= players[0].x + players[0].lx):
            balle.rebond(players[0].vy, n, 0)
        # if the ball is below the plateform
        elif players[0].y - balle.radius + 1 <= balle.y <= players[0].y and math.sqrt(
                    (balle.y - players[0].y) ** 2 + (balle.x - (players[0].x + players[0].lx)) ** 2) <= balle.radius:
                balle.rebond(players[0].vy, n, players[0].y-balle.y)
        # if the ball is above the Plateform
        elif players[0].y + players[0].ly <= balle.y <= players[0].y + players[0].ly + balle.radius:
            if math.sqrt((balle.y - (players[0].y + players[0].ly)) ** 2 + (
                    balle.x - (players[0].x + players[0].lx)) ** 2) <= balle.radius:
                balle.rebond(players[0].vy, n, players[0].y-balle.y)

    if balle.vx > 0:
        if balle.x >= players[1].x and balle.x - balle.vx >= players[1].x:
            return False
        elif (players[1].y <= balle.y <= players[1].y + players[1].ly
                and balle.x + balle.radius >= players[1].x):
            balle.rebond(players[1].vy, n, 0)
        # if the ball is below the Plateform
        elif players[1].y - balle.radius + 1 <= balle.y <= players[1].y and math.sqrt((balle.y - players[1].y) ** 2 + (balle.x - players[1].x) ** 2) <= balle.radius:
                balle.rebond(players[1].vy, n, players[0].y-balle.y)
        # if the ball is above the Plateform
        elif players[1].y + players[1].ly <= balle.y <= players[1].y + players[1].ly + balle.radius:
            if math.sqrt(
                    (balle.y - (players[1].y + players[1].ly)) ** 2 + (balle.x - players[1].x) ** 2) <= balle.radius:
                balle.rebond(players[1].vy, n, players[0].y-balle.y)

    if balle.y - balle.radius <= 20 or balle.y + balle.radius >= HEIGHT-20:
        balle.rebond(0, n, 0, True)

    if balle.x - balle.radius < 0 or balle.x + balle.radius > WIDTH:
        return False

    return True


def main():
    players = [Plateform(100, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 20, GREEN), Plateform(WIDTH-110, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 20, GREEN)]
    balle = Ball(WIDTH//2, HEIGHT//2 - 10, 10, 0, 35, RED)
    n = 0
    running = True

    #balle.vy = rd.randint(-10, 10)
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


