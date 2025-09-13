import pygame as pg
import math
import time

pg.init()

"""
Constants and initialization
"""

WIDTH = 960
HEIGHT = 540

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Ping-Pong")

GREEN = (118,150,86)
dGREEN = (88,120,56)
WHITE = (238,238,210)
dWHITE = (208,208,180)
GREY = (50, 50, 50)
RED = (255, 20, 20)

win.fill(GREY)

class Ball:
    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def rebond(self, coeff, touche_exterieur):
        bord = -1 if touche_exterieur else 1
        self.vx = - (self.vx + coeff) * bord
        self.vy = - (self.vy + coeff)

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

    def draw(self):
        pg.draw.rect(win, self.color, (self.x, self.y, self.lx, self.ly))


def main():

    players = [Plateform(10, HEIGHT//2, 10, 100, HEIGHT, 0, GREEN), Plateform(WIDTH-20, HEIGHT//2+10, 10, 100, HEIGHT, 0, GREEN)]
    balle = Ball(WIDTH//2, HEIGHT//2 - 10, 10, 0, 40, RED)
    running = True

    while running:
        for i in players: i.reset()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                players[0].move(1)

            if event.key == pg.K_UP:
                players[0].move(-1)

        balle.move()

        if balle.vx < 0:
            if (players[0].y <= balle.y <= players[0].y + players[0].ly
                    and balle.x - balle.radius <= players[0].x + players[0].lx):
                balle.rebond(players[0].vy, False)
            elif players[0].y - balle.radius + 1 <= balle.y <= players[0].y:
                if math.sqrt((balle.y - players[0].y)**2 + (balle.x - (players[0].x + players[0].lx))**2) <= balle.radius:
                    balle.rebond(players[0].vy, False)
            elif players[0].y + players[0].ly <= balle.y <= players[0].y + players[0].ly + balle.radius:
                if math.sqrt((balle.y - (players[0].y + players[0].ly))**2 + (balle.x - (players[0].x + players[0].lx))**2) <= balle.radius:
                    balle.rebond(players[0].vy, False)

        if balle.vx > 0:
            if (players[1].y <= balle.y <= players[1].y + players[1].ly
                    and balle.x + balle.radius >= players[1].x):
                balle.rebond(players[1].vy, False)
            elif players[1].y - balle.radius + 1 <= balle.y <= players[1].y:
                if math.sqrt((balle.y - players[1].y)**2 + (balle.x - players[1].x)**2) <= balle.radius:
                    balle.rebond(players[1].vy, False)
            elif players[1].y + players[1].ly <= balle.y <= players[1].y + players[1].ly + balle.radius:
                if math.sqrt((balle.y - (players[1].y + players[1].ly))**2 + (balle.x - players[1].x)**2) <= balle.radius:
                    balle.rebond(players[1].vy, False)

        if balle.y - balle.radius <= 0:
            balle.rebond(0, True)
        elif balle.y + balle.radius >= HEIGHT:
            balle.rebond(0, True)



        #display
        win.fill(GREY)
        balle.draw()
        for i in players: i.draw()

        pg.display.update()
        pg.time.Clock().tick(60)


main()


