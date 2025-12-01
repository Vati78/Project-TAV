import pygame as pg, math, os, time, random as rd, copy
from baseClass import *

class Portals():
    def __init__(self, x1, y1, x2, y2):
        self.p1 = Portal(x1, y1, self,1)
        self.p2 = Portal(x2, y2, self,2)
        self.contact = False
        self.ok = True
    def move(self):
        self.ok = not self.contact
        self.contact = False
    def teleport(self, p, game):
        """
        teleports the ball if not already teleported before

        :param self: Portals object
        :param p: Index of the Portal who called the function
        :param game: Game object
        :return: None
        """
        if self.contact and self.ok: self.ok = False
        self.contact = True
        if self.ok:
            if p==2:
                game.balle.x += self.p1.x - self.p2.x
                game.balle.y += self.p1.y - self.p2.y
                #print(1, self.p2.x, self.p2.y)
                #return self.p2.x, self.p2.y
            else:
                game.balle.x += self.p2.x - self.p1.x
                game.balle.y += self.p2.y - self.p1.y
                #print(p, self.p1.x, self.p1.y)
                #return self.p1.x, self.p2.y


class Portal(item):
    def __init__(self, x, y, p,i):
        item.__init__(self,x,y,30,60)
        self.p = p
        self.index = i
    def move(self,game):
        """
        Move
        
        :param self: Portal object
        :param game: Game object
        """
        if self.index == 1: self.p.move()
    def interagit(self, c, game):
        """
        Interaction of Portal with the Ball
        
        :param self: Portal object
        :param c: Direction of the contact
        :param game: Game object
        """
        return self.p.teleport(self.index, game) 
