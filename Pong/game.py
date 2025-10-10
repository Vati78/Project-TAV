import pygame as pg, math, os, time, random as rd

pg.init()
os.chdir(os.path.dirname(__file__))

"""
Constants and initialization
"""

phone = False

debug = 0

#dimensions de la fenetre PYGAME
WIDTH = 1000
HEIGHT = 600
POINTS = 50

#création de la fenetre PYGAME
win = pg.display.set_mode((WIDTH, HEIGHT+POINTS))
pg.display.set_caption("Ping-Pong")

#creation de certaines couleurs
GREEN = (118,150,86)
dGREEN = (88,120,56)
WHITE = (238,238,210)
dWHITE = (208,208,180)
GREY = (50, 50, 50)
RED = (255, 20, 20)

#affichage des images de
win.blit(pg.image.load(f"Images/haut.png"), (0, 0))
win.blit(pg.image.load(f"Images/terrain.png"), (0, 100))

last_r = None #0: dernier rebond à gauche; 1: dernier rebond à droite

variantes = False

#création de la classe BALLE
class Ball():
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
    def rebond(self, p, loop, position):
        global debug
        #p_vy: vy de la plateforme; position: relative to the plateform; touche_exterieur: haut ou bas de l'écran
        position = position.lower()
        #bord = -1 if position in ("above","below","wall") else 1
        if position in ("above", "walldown"): diry = -1
        elif position in ("below", "wallup"): diry = 1
        elif self.vy > 0: diry = 1
        else: diry = -1
        signe_x = -1 if (self.vx < 0) else 1
        if position in ("right","left"): signe_x = -1 if position == "left" else 1
        vy = 0 if "wall" in position else 0.2 * p.vy
       # print("#",p.vy, vy)
        self.vx =  self.vx_i * (1 + loop/2000) * signe_x
        self.vy =  abs(self.vy) * diry + vy #*sens
        m = False
        if position == "above":
            if self.y + self.radius > p.y:
                self.y = p.y - self.radius
                m = True
        elif position == "below":
            if self.y - self.radius < p.y + p.ly:
                self.y = p.y + p.ly + self.radius
                m = True
        # si la balle touche le haut ou la bas du terrain
        if self.y - self.radius <= 120 and m:
            self.y = 120 + self.radius
            if self.x > p.x + p.lx // 2: self.x = p.x + p.lx + self.radius
            else: self.x = p.x - self.radius
        if self.y + self.radius >= HEIGHT - 20 and m:
            self.y = HEIGHT - 20 - self.radius
            if self.x > p.x + p.lx // 2: self.x = p.x + p.lx + self.radius
            else: self.x = p.x - self.radius
        #print("rebond", position, self.vx, self.vy)

    #affichage de la balle
    def draw(self):
        win.blit(self.image, (self.x-self.radius, self.y-self.radius))

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
class Plateform():
    #création des variables relatives à la classe PLATEFORME
    def __init__(self, x, y, lx, ly, ymax, ymin, color, index, ia = None, diff = 10):
        self.x = x
        self.y = y
        self.lx = lx
        self.ly = ly
        self.vy = 0
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

    #déplacement de la PLATEFORME
    def move(self, vy, ball=None):
        if self.ia and ball != None:
            if ball.vx > 0 and self.y_v == None:
                x = ball.x + ball.radius
                y = ball.y
                vy = ball.vy
                while x < self.x:
                    x += ball.vx
                    y += vy
                    if y + vy - ball.radius <= 120: vy = -vy
                    elif y + vy + ball.radius >= HEIGHT - 20: vy = -vy
                self.y_v = y - self.ly/2
                self.count += 1
                #print(vy)
                #print(y, ' -')
                if self.diff != "":
                    if self.count >= self.diff + int(self.diff * (rd.random()- 0.5)/2):
                        self.count = 0
                        self.y_v = rd.randint(self.ymin, self.ymax-self.ly)
                        #print("rd")
            elif ball.vx<0: self.y_v = None
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
    def draw(self):
        win.blit(self.img, (self.x, self.y))

#détection des différentes interactions entre les objets

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Contraint une valeur dans un intervalle."""
    return max(min_val, min(value, max_val))

def contact(p, balle, n) -> str:
    """
    Détermine le type de contact ('ABOVE', 'LEFT', 'RIGHT', 'BELOW', ou '')
    entre une balle (cercle) et une plateforme rectangulaire.
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


def interactions(players, balle, n):#, simulation=False, coor=None):
    global last_r

    p =- 1
    if balle.x < players[0].x + players[0].lx + balle.radius + balle.vx + 10: p = 0
    elif balle.x > players[1].x - balle.radius - balle.vx - 10: p = 1
    if p != -1:
        c = contact(players[p], balle, n)
        if c: balle.rebond(players[p], n, c)
        else:
            s = False
            py = int(players[p].y)
            bx , by = int(balle.x), int(balle.y)
          #  print(f">>>Simulation {n}>>>")
            steps = int(max(abs(players[p].vy), abs(balle.vy), abs(balle.vx)))
            for simx in range(steps):
                players[p].y = int(py + (simx * players[p].vy / steps))
                balle.y = int(by + (simx * balle.vy / steps))
                balle.x = int(bx + (simx * balle.vx / steps))
                c = contact(players[p], balle, (n,1, steps))
             #   print((players[p].y, balle.y, balle.x), end ="; ")
                if c:
                   # print("")
                    balle.freeze()
                    players[p].freeze()
                    s = True
                    break
            if not s:
                players[p].y = py
                balle.x = bx
                balle.y = by
          #  print("<<<End<<<")


    #si la balle touche le haut ou la bas du terrain
    if balle.y - balle.radius <= 120:
        balle.rebond(players[p], n, "wallup")
    if balle.y + balle.radius >= HEIGHT-20:
        balle.rebond(players[p], n, "walldown")

    #si la balle touche la gauche ou la droite du terrain
    if balle.x - balle.radius < 0 or balle.x + balle.radius > WIDTH:
        #arreter le jeu
        return False

    #continuer le jeu
    return True



####~~~~~~~~~~~~####+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+--+-+-+####
#fonction principale
def main():
    global last_r, debug
    #création des objets
    players = [Plateform(100,     (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 0),
               Plateform(WIDTH-110, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 1, True, 15)]
    balle = Ball(WIDTH//2, HEIGHT//2 - 10, 5, rd.randint(-50, 50)/10, 35)

    #nombre d'itérations et variable de boucle principale
    n = 0
    running = True

    #initialisation de l'horloge
    clock = pg.time.Clock()

    #chargement des images de fond
    fond = pg.image.load(f"Images/terrain.png")
    haut = pg.image.load(f"Images/haut.png")
    police = pg.font.SysFont("Arial", 45)

    pause = False
    pause_e = True

    #boucle principale
    while running:

        #détection d'un éventuel évenement menant à une fermeture de pygame
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        #mise à 0 de la vitesse verticale de chaque joueur
#        for i in players: i.vy = 0

        if phone:
             mouse_pos = pg.mouse.get_pos()
             if mouse_pos[1] > players[0].y + players[0].ly//2 + players[0].vmax:
                 players[0].move(1)
             elif mouse_pos[1] < players[0].y +  players[0].ly//2 - players[0].vmax:
                 players[0].move(-1)

        else:
            #collecte de tous les éléments
            keys = pg.key.get_pressed()

            #mouvements du jour 0
            if not pause:
                if keys[pg.K_DOWN]:
                    players[0].move(1)
                if keys[pg.K_UP]:
                    players[0].move(-1)
                if keys[pg.K_LEFT]: debug = 1
                else: debug = 0
            if keys[pg.K_RIGHT]:
                if pause_e:
                    pause = not pause
                    pause_e = False
            else: pause_e = True
        if pause:
            continue

        # + 1 itération à la boucle principale
        n += 1

        #mouvement de la balle
        balle.move()
        pg.draw.rect(win, "black", (balle.x, balle.y, 5, 5))

        #mouvement du bot
        #players[1].y = balle.y - players[1].ly//2
        players[1].move(0, balle)

        #terminer le jeu si aucune interaction quand la balle sort du terrain
        if running:
            #pas d'interaction+
            if not interactions(players, balle, n): # n  loop (car loop != 0)
                last_r = None
                # attitrage des points
                if balle.vx < 0:
                    players[1].nmb_points += 1
                else:
                    players[0].nmb_points += 1
                del balle
                #recréation d'une nouvelle partie
                for i in (0, 1):
                    players[i].y = (HEIGHT-100)//2
                    players[i].reset()
                balle = Ball(WIDTH // 2, HEIGHT // 2 - 10, 5, rd.randint(-20,20)/10, 35)
                n = 0
                time.sleep(1)

        #affichage de tous les éléments
        win.fill((0,0,0))
        win.blit(fond, (0, 100))
        win.blit(haut, (0, 0))
        balle.draw()
        for i in enumerate(players): i[1].draw()

        #Affichage du score
        score = f"{players[0].nmb_points} : {players[1].nmb_points}"
        texte = police.render(score, True, (255,255,255))
        win.blit(texte, (WIDTH/2 - 9 * (len(str(players[0].nmb_points))+1) - 27, HEIGHT))

        #mise à jour de la fenetre pygame
        pg.display.update()
        clock.tick(120)

main()