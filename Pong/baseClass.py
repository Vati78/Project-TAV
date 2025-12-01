#import de diférents modules
import pygame as pg, math, os, time, random as rd, copy

#classe relative à chauqe lutin du jeu
class item():

    #initialisation des variables communes à chaque objet
    #leur coordonnées et leur image d'affichage
    def __init__(self, x, y, lx=50,ly=50,imagename = None):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly

        if imagename is not None:
            self.image = pg.image.load(imagename)

        # si l'image n'est pas précisée, on affiche l'image correspondante au nom de la classe
        else:
            imagename = type(self).__name__

        #    try:
            self.img = pg.transform.scale(pg.image.load(f"Images/{imagename}.png"), (self.lx, self.ly))
        #    except:
                
    def draw(self, game):
        game.win.blit(self.img, (self.x, self.y))

    #cette fonction crée une nouvelle instance d'une classe particulière dont les variables seront
    #les mêmes que celle originale, sauf que les variables relatives à l'affichage de l'originale ne sont pas
    #recopiées
    def __deepcopy__(self, memo):

        #on récupère la classe relative à l'objet que l'on veut copier
        cls = self.__class__
        #on crée une nouvelle instance de classe "cls" sans passer par la fonction "init" (c'est le principe de new)
        result = cls.__new__(cls)
        #pour éviter une copie d'un élément à l'infini, on alloue une place dans un dictionnaire à chaque lutin
        #du jeu, et chaque nouvelle instance remplacera l'ancienne
        memo[id(self)] = result

        #ensuite on parcourt chaque attribut de l'objet dans son dictionnaire "self"
        for k, v in self.__dict__.items():
            if isinstance(v, pg.Surface):  # Exclure les Surface (attributs relatifs à l'affichage de l'objet)
                setattr(result, k, v)  # on garde les éléments de l'objet initial
            else:
                setattr(result, k, copy.deepcopy(v, memo))

        #on retourne la nouvelle instance préparée
        return result

#création de la classe BALLE
class Ball(item):
    #initialisation des variables relatives à la BALLE
    def __init__(self, x, y, vx, vy, radius):
        self.x = x
        self.y = y
        self.vx_i = abs(vx)
        self.vy_i = vy
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.image = pg.image.load(f"Images/Balle.png")
        self.stop = False #si il doit ne pas move dans cette iteration (cf freeze())

    #détection d'un rebond
    def rebond(self, p, loop, position, game):
        """
        rebond de la balle
        :param p: objet Plateforme
        :param loop: nombre d'échages (rebonds sur un joueur) pour la vitesse
        :param position: LEFT, RIGHT, ABOVE ou BELOW (lutin par rapport a la balle)
        :param game: objet Game
        :return:
        """

        position = position.lower()

        #si la balle est en interaction avec un objet au-dessus d'elle, elle va repartir vers le bas → diry = -1
        if position in ("above", "walldown"):
            diry = -1

        #si elle l'est avec un objet en dessous, elle remonte
        elif position in ("below", "wallup"):
            diry = 1

        elif self.vy > 0: diry = 1

        else: diry = -1

        signe_x = -1 if (self.vx < 0) else 1

        if position in ("right","left"):
            signe_x = -1 if position == "left" else 1

        #si la balle touche un mur, on accélère pas sa vitesse, si c'est une plateforme, on le fait à raison de +20% de celle de
        #la plateforme
        vy = 0 if "wall" in position else 0.2 * p.vy

        #on accélère la vitesse horizontale de la balle à chaque rebond
        self.vx =  self.vx_i * (1 + loop/2000) * signe_x

        #on fait de même
        self.vy =  abs(self.vy) * diry + vy

        #if the ball is between the plateform and the borders
        m = False #bool: if the ball is forced by the platform to go out of the border

        if position == "above":
            if self.y + self.radius > p.y:
                self.y = p.y - self.radius
                m = True

        elif position == "below":
            if self.y - self.radius < p.y + p.ly:
                self.y = p.y + p.ly + self.radius
                m = True

        # si la balle touche le haut ou le bas du terrain
        if self.y - self.radius <= 120 and m:
            self.y = 120 + self.radius
            if self.x > p.x + p.lx // 2: self.x = p.x + p.lx + self.radius
            else: self.x = p.x - self.radius

        if self.y + self.radius >= game.HEIGHT - 20 and m:
            self.y = game.HEIGHT - 20 - self.radius
            if self.x > p.x + p.lx // 2: self.x = p.x + p.lx + self.radius
            else: self.x = p.x - self.radius
        #print("rebond", position, self.vx, self.vy)

    #affichage de la balle
    def draw(self, game):
        game.win.blit(self.image, (self.x-self.radius, self.y-self.radius))

    #déplacement pour la fonction interaction
    def freeze(self):
        self.stop = True

    #déplacement de la balle
    def move(self):
        if not self.stop:
            self.x += self.vx
            self.y += self.vy
        else: self.stop = False

#création de la classe PLATEFORME
class Plateform(item):
    #création des variables relatives à la classe PLATEFORME
    def __init__(self, x, y, lx, ly, ymax, ymin, color, index, ia = None, diff = 10):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.vy = 0
        self.vx = 0
        self.ymax = ymax
        self.ymin = ymin
        self.vmax = 10
        self.color = color
        self.index = index
        self.img = pg.transform.scale(pg.image.load(f"Images/Platforme_{self.index+1}.png"), (self.lx, self.ly))
        self.nmb_points = 0
        self.stop = False #si il doit ne pas bouger à l'iteration, cf freeze()

        self.ia = ia if ia != None else (index == 1)

        if self.ia:
            self.y_v = None
            self.vmax /= 2
            self.diff = diff
            self.count = 0
            self.last_x_calculated = 0
            self.calculation_interval = 200

    #déplacement de la PLATEFORME
    def move(self, vy, game = None):
        if self.ia and game is not None:
            if game.balle.vx > 0 and (self.y_v is None or game.balle.x - self.last_x_calculated > self.calculation_interval):
                a = True
                if self.diff != "":
                    #if failing
                    if self.count >= self.diff + int(self.diff * (rd.random()- 0.5)/2):
                        a = False
                        print("r", end = "; ")
                        self.count = 0
                        self.y_v = rd.randint(self.ymin, self.ymax-self.ly)
                if a: #if not voluntary failing
                    jeu = copy.deepcopy(game)

                    while jeu.balle.x  + jeu.balle.radius < self.x:
                        jeu.balle.move()
                        for i in jeu.items: i.move(jeu)
                        if not jeu.interactions(): break

                    self.y_v = jeu.balle.y - self.ly/2
                    self.count += 1
                    del jeu
                    print(self.y_v)
                    self.last_x_calculated = game.balle.x
            elif game.balle.vx<0:
                self.y_v = None
                self.last_x_calculated = 0
            if self.y_v is None: y_v = ((self.ymin + self. ymax) / 2 - self.ly / 2)
            else: y_v = self.y_v
            vy=0
            if abs(y_v - self.y) >= self.vmax: vy = 1 if y_v - self.y > 0 else -1
        if not self.stop:
            vy *= self.vmax
            if self.ymin < self.y + vy < self.y + vy + self.ly < self.ymax:
                self.y += vy
                self.vy = vy
        else: self.stop = False

    def freeze(self):
        self.stop = True
        if self.y < self.ymin: self.y = self.ymin
        if self.y + self.ly > self.ymax: self.y = self.ymax - self.ly

    #nouvel envoi de balle
    def reset(self):
        self.vy = 0
        if self.ia: self.y_v = None

    #affichage de la PLATEFORME
    def draw(self, game):
        game.win.blit(self.img, (self.x, self.y))
