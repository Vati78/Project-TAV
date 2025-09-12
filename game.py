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

win.fill(GREY)

class Ball:
    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def rebond(self, plateforme):
        self.vx = -self.vx
        self.vy = -self.vy + plateforme.vy

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
        self.vmax = 4
        self.color = color

    def move(self, vy):
        vy *= self.vmax
        if self.ymin < self.y + vy< self.ymax:
            self.y += vy
            self.vy = vy

    def reset(self):
        self.vy = 0

    def draw(self):
        pg.draw.rect(win, self.color, (self.x, self.y, self.lx, self.ly))


def main():

    players = [Plateform(10, HEIGHT//2, 10, 100, WIDTH-40, 0, GREEN), Plateform(WIDTH-20, HEIGHT//2, 10, 100, WIDTH-40, 0, GREEN)]
    balle = Ball(WIDTH//2, HEIGHT//2, 10, 0, 40, GREEN)
    running = True

    while running:
        keys = pg.key.get_pressed()
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

        if players[0].y <= balle.y <= players[0].y + players[0].ly:
            if balle.x - balle.radius <= players[0].x + players[0].lx and balle.vx < 0:
                balle.rebond(players[0])
        elif players[0].y - balle.radius <= balle.y <= players[0].y:
            if math.sqrt((balle.y - players[0].y)^2 + (balle.x - (players[0].x + players[0].lx))^2) <= balle.radius:
                balle.rebond(players[0])
        elif players[0].y + players[0].ly<= balle.y <= players[0].y + players[0].ly + balle.radius :
            if ((balle.y - (players[0].y - players[0].ly))**2 + (balle.x - players[0].x + players[0].lx)**2)**0.5:
                balle.rebond(players[0])

        if (balle.x + balle.radius >= players[1].x
                and players[1].y <= balle.y <= players[1].y + players[1].ly)\
                and balle.vx > 0:
            balle.rebond(players[1])

        #display
        win.fill(GREY)
        balle.draw()
        for i in players: i.draw()

        pg.display.update()
        pg.time.Clock().tick(60)


main()


