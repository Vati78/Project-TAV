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
        self.contact = True
        if self.ok:
            if p==1:
                return self.p2.x, self.p2.y
            else:
                return self.p1.x, self.p2.y


class Portal(item):
    def __init__(self, x, y, p,i):
        item.__init__(self,x,y)
        self.p = p
        self.index = i
    def move(self,game):
        if self.index == 1: self.p.move()
    def interagit(self, c, game):
        return self.p.teleport(self.index, game) 
