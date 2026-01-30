from baseClass import *

class Portals:
    variant = False
    def __init__(self, x1, y1, x2, y2):
        self.p1 = Portal(x1, y1, self,1)
        self.p2 = Portal(x2, y2, self,2)
        self.contact = False #if there was a contact with one Portal before
        self.ok = True #if the Portals can teleport again


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
            if game.simulate is False: type(self.p1).son.play()
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


class Portal(Item):
    variant = True
    def __init__(self, x, y, p, i):
        Item.__init__(self,x,y,30,60)
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

class Bomb(Item):
    variant = True
    def __init__(self, x, y, lx=50, ly=50):
        Item.__init__(self, x, y, lx, ly)
    def interagit(self, c, game):
        if game.balle.last_rebond is not None:
            game.balle.last_rebond.nmb_points -= 1
            if game.balle.last_rebond.nmb_points < 0: game.balle.last_rebond.nmb_points = 0
            self.explose(game)
    def explose(self, game):
        if game.simulate is False:
            type(self).son.play()
        game.items.remove(self)
        del self

class Coin(Item):
    variant = True
    def __init__(self, x, y, lx=50, ly=50):
        Item.__init__(self, x, y, lx, ly)

    def interagit(self, c, game):
        if game.balle.last_rebond is not None:
            game.balle.last_rebond.nmb_points += 1
            self.explose(game)

    def explose(self, game):
        if game.simulate is False:
            type(self).son.play()
        game.items.remove(self)
        del self

class Dice(Item):
    variant = True
    def __init__(self, x, y, lx=50, ly=50):
        Item.__init__(self, x, y, lx, ly)
        self.actif = False
    def move(self, game):
        if self.actif and not game.balle.random[0]:
            self.explose(game)
    def interagit(self, c, game):
        if not self.actif:
            game.balle.random = [True, time.time() + 10]
            self.actif = True
            self.x, self.y = 20, 20
            if game.simulate is False:
                type(self).son.play()

    def explose(self, game):
        game.items.remove(self)
        del self