import pygame as pg, os, time, random as rd, baseClass, inspect

pg.init()
pg.mixer.init()
os.chdir(os.path.dirname(__file__))


"""
Constants and initialization
"""



def clamp(value, min_val, max_val):
    """Contraint une valeur dans un intervalle."""
    return max(min_val, min(value, max_val))

def contact(p, balle, n):
    """
    Détermine le type de contact ('ABOVE', 'LEFT', 'RIGHT', 'BELOW', ou '') entre une balle (cercle) et une plateforme rectangulaire.

    :param p: The 2 Platform objects
    :param balle: The Ball object
    :param n: Iteration
    :return: Direction of the contact
    :rtype: Literal['', 'above', 'below', 'left', 'right']
    """
    # Point du rectangle le plus proche du centre du cercle
    closest_x = clamp(balle.x, p.x, p.x + p.lx)
    closest_y = clamp(balle.y, p.y, p.y + p.ly)

    # Différences
    dx = balle.x - closest_x
    dy = balle.y - closest_y
    dist_sq = dx * dx + dy * dy

    # Pas de collision
    if dist_sq > balle.radius ** 2:
        return ""

    # Détermination du côté de contact
    if abs(dy) > abs(dx):
        return "above" if dy < 0 else "below"
    else:
        return "left" if dx < 0 else "right"


#objet jeu principale
class Game(baseClass.Item):

    import variants #, baseClass
    def __init__(self, config = None):
        self.phone = False

        self.n = 0
        # dimensions de la fenêtre PYGAME
        self.WIDTH = 1000
        self.HEIGHT = 600
        self.POINTS = 50

        # création de la fenêtre PYGAME
        self.win = pg.display.set_mode((self.WIDTH, self.HEIGHT + self.POINTS))
        pg.display.set_caption("Pong game")

        # creation de certaines couleurs
        self.GREEN = (118, 150, 86)
        self.dGREEN = (88, 120, 56)
        self.WHITE = (238, 238, 210)
        self.dWHITE = (208, 208, 180)
        self.GREY = (50, 50, 50)
        self.RED = (255, 20, 20)

        # affichage des images de
        self.win.blit(pg.image.load(f"Images/haut.png"), (0, 0))
        self.win.blit(pg.image.load(f"Images/terrain.png"), (0, 100))

        self.simulate = False

        self.itemList = []
        for name, objet in inspect.getmembers(self.variants):
            if inspect.isclass(objet) and objet.variant:
                self.itemList.append(name)
        self.items = []
        if config is None: config = {
            "ball_speed": 5,
            "ball_size": 30,
            "human_players": 1,
            "bot_difficulty": 5,
            "bonus_frequency": 5,
            "active_items": self.itemList}
        self.ball_speed = config["ball_speed"]
        self.ball_size = config["ball_size"]
        self.nbplayers = config["human_players"]
        self.diff = config["bot_difficulty"]
        self.freq = config["bonus_frequency"]
        self.itemList = config["active_items"]

        if "Portal" in self.itemList:
            self.itemList.remove("Portal")
            self.portal = True
        else: self.portal = False

        for i in self.itemList:
            a = eval(f"self.variants.{i}")(0,0)
            del a
 #       baseClass.Ball(self.WIDTH//2, self.HEIGHT + 5 - 2*self.ball_size, self.ball_speed, rd.randint(-50, 50)/10, self.ball_size).draw(self)
  ##      baseClass.Ball(self.WIDTH // 2+50, self.HEIGHT + 7 - 2*self.ball_size, self.ball_speed, rd.randint(-50, 50) / 10, self.ball_size).draw(self)
    #    baseClass.Ball(self.WIDTH // 2+100, self.HEIGHT + 9 - 2*self.ball_size, self.ball_speed, rd.randint(-50, 50) / 10, self.ball_size).draw(self)
     #   pg.display.update()
      #  time.sleep(10000)

    def run(self):
        """
        runs the main main function

        :param self: Game object
        """
        self.main()


    def main(self):
        """
        main function of the game
        
        :param self: Game object
        """
        
        #création des objets
        self.players = [baseClass.Platform(100,     (self.HEIGHT-100)//2, 10, 100, self.HEIGHT-20, 120, self.GREEN, 0, self.nbplayers == 0, self.diff),#[baseClass.Platform(100,     (self.HEIGHT-100)//2, 10, 100, self.HEIGHT-20, 120, self.GREEN, 0),
                   baseClass.Platform(self.WIDTH-110, (self.HEIGHT-100)//2, 10, 100, self.HEIGHT-20, 120, self.GREEN, 1, self.nbplayers in (0,1), self.diff)]#15)]
        self.balle = baseClass.Ball(self.WIDTH//2, self.HEIGHT//2 - 10, self.ball_speed, rd.randint(-50, 50)/10, self.ball_size)
        '''
        a = self.variants.Portals(200,200,600,400)

        self.items = [self.variants.Bomb(300, 400), self.variants.Coin(600, 400)]
        '''

        #nombre d'itérations et variable de boucle principale
        self.n = 0
        running = True

        #initialisation de l'horloge
        clock = pg.time.Clock()

        #chargement des images de fond
        fond = pg.image.load("Images/terrain.png")
        haut = pg.image.load("Images/haut.png")
        police = pg.font.SysFont("Arial", 45)

        pause = False
        pause_e = True

        #boucle principale
        while running:

            #détection d'un éventuel évenement menant à une fermeture de pygame
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            if self.phone:
                 mouse_pos = pg.mouse.get_pos()
                 if mouse_pos[1] > self.players[0].y + self.players[0].ly//2 + self.players[0].vmax:
                     self.players[0].move(1)
                 elif mouse_pos[1] < self.players[0].y +  self.players[0].ly//2 - self.players[0].vmax:
                     self.players[0].move(-1)

            else:
                #collecte de tous les éléments
                keys = pg.key.get_pressed()

                #mouvements du jour 0
                if not pause and self.nbplayers != 0:
                    if keys[pg.K_DOWN]:
                        self.players[self.nbplayers-1].move(1)
                    if keys[pg.K_UP]:
                        self.players[self.nbplayers-1].move(-1)
                    if self.nbplayers == 2:
                        if keys[pg.K_s]:
                            self.players[0].move(1)
                        if keys[pg.K_z]:
                            self.players[0].move(-1)
                if keys[pg.K_RIGHT] or keys[pg.K_p]:
                    if pause_e:
                        pause = not pause
                        pause_e = False
                else: pause_e = True
            if pause:
                continue

            # + 1 itération à la boucle principale
            self.n += 1

            self.spawn()

            #mouvement de la balle
            self.balle.move()
            #pg.draw.rect(win, "black", (self.balle.x, self.balle.y, 5, 5))

            #mouvement du bot
            if self.nbplayers != 2:
                self.players[1].move(0, self)
                if self.nbplayers == 0: self.players[0].move(0, self)

            #gestion des items
            for i in self.items: i.move(self)

            #terminer le jeu si aucune interaction quand la balle sort du terrain
            if running:
                #si balle sort du terrain
                if not self.interactions(): # n  loop (car loop != 0)
                    last_r = None
                    # attitrage des points
                    if self.balle.vx < 0:
                        self.players[1].nmb_points += 1
                    else:
                        self.players[0].nmb_points += 1
                    del self.balle
                    #recréation d'un nouvel échange
                    for i in (0, 1):
                        self.players[i].y = (self.HEIGHT-100)//2
                        self.players[i].reset() 
                    self.balle = baseClass.Ball(self.WIDTH // 2, self.HEIGHT // 2 - 10, self.ball_speed, rd.randint(-50, 50)/10, self.ball_size)
                    self.n = 0
                    time.sleep(1)

            #affichage de tous les éléments
            self.win.fill((0,0,0))
            self.win.blit(fond, (0, 100))
            self.win.blit(haut, (0, 0))
            for i in self.items: i.draw(self)
            self.balle.draw(self)
            for i in enumerate(self.players): i[1].draw(self)

            #Affichage du score
            score = f"{self.players[0].nmb_points} : {self.players[1].nmb_points}"
            texte = police.render(score, True, (255,255,255))
            self.win.blit(texte, (self.WIDTH/2 - 9 * (len(str(self.players[0].nmb_points))+1) - 27, self.HEIGHT))

            #mise à jour de la fenetre pygame
            pg.display.update()
            clock.tick(120)

    def interactions(self):  # , simulation=False, coor=None):
        """
        Interactions
        
        :param self: Game object
        :return: If the game goes on (True) or stops (False) because the ball is out of the borders
        :rtype: bool
        """
        global last_r
        p = - 1  #index de la plateforme
        # print("a", players, self.balle)
        if self.balle.x < self.players[0].x + self.players[0].lx + self.balle.radius + self.balle.vx + 10:
            p = 0
        elif self.balle.x > self.players[1].x - self.balle.radius - self.balle.vx - 10:
            p = 1
        if p != -1:
            c = contact(self.players[p], self.balle, self.n)
            if c:
                self.balle.rebond(self.players[p], self.n, c, self)
            else:
                py = int(self.players[p].y)
                bx, by = int(self.balle.x), int(self.balle.y)
                #  print(f">>>Simulation {self.n}>>>")
                steps = int(max(abs(self.players[p].vy), abs(self.balle.vy), abs(self.balle.vx)))

                #faire la simulation pixel par pixel de la balle arrivant sur la plateforme
                for simx in range(steps):
                    self.players[p].y = int(py + (simx * self.players[p].vy / steps))
                    self.balle.y = int(by + (simx * self.balle.vy / steps))
                    self.balle.x = int(bx + (simx * self.balle.vx / steps))
                    c = contact(self.players[p], self.balle, (self.n, 1, steps))
                    #   print((self.players[p].y, self.balle.y, self.balle.x), end ="; ")
                    if c:
                        # print("")
                        self.balle.freeze()
                        self.players[p].freeze()
                        break
                else:
                    self.players[p].y = py
                    self.balle.x = bx
                    self.balle.y = by
            #  print("<<<End<<<")

        # si la balle touche le haut ou le bas du terrain
        if self.balle.y - self.balle.radius <= 130:
            self.balle.rebond(self.players[p], self.n, "wallup", self)
        if self.balle.y + self.balle.radius >= self.HEIGHT - 30:
            self.balle.rebond(self.players[p], self.n, "walldown", self)

        # si la balle touche la gauche ou la droite du terrain
        if self.balle.x - self.balle.radius < 0 or self.balle.x + self.balle.radius > self.WIDTH:
            # arreter le jeu
            return False
        # si la self.balle touche des items:
        for i in self.items:
            c = contact(i, self.balle, self.n)
            if c:
                a = i.interagit(c, self)

        # continuer le jeu
        return True


    def spawn(self):
        if self.freq!=0 and rd.randint(0, (1000 // self.freq)) == 0 and len(self.itemList) != 0:
            a=rd.choice(self.itemList)
            if a == "Dice" and (any(type(i).__name__=="Dice" for i in self.items) or rd.random()<0.9): pass #évite d'avoir plusieurs dés en même temps
            else: self.newItem(a)
        elif self.freq !=0 and self.portal and rd.randint(0, 10*(100 - self.freq)) == 0:
            a = True
            for i in self.items[:]:
                if isinstance(i, self.variants.Portal):
                    self.items.remove(i)
                    a = False
            if a: self.newItem("Portals")

    def newItem(self, type):
        if type == "Portals":
            a = self.variants.Portals(rd.randint(150, 820), rd.randint(130, 510), rd.randint(150, 820), rd.randint(130, 510))
            self.items += [a.p1, a.p2]
        else:
            self.items.append(eval(f"self.variants.{type}")(rd.randint(200,800), rd.randint(200,400)))

if __name__ == "__main__":
    game = Game()
    game.run()