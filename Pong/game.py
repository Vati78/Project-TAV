import pygame as pg, math, os, time, random as rd

pg.init()
os.chdir(os.path.dirname(__file__))

"""
Constants and initialization
"""
phone = False

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
    def rebond(self, p_vy, loop, position):
        #p_vy: vy de la plateforme; position: relative to the plateform; touche_exterieur: haut ou bas de l'écran
        bord = -1 if position in ("above","below","wall") else 1
        signe_x = -1 if (self.vx < 0) else 1
        if position in ("right","left"): signe_x = 1 if position == "left" else -1
        self.vx = - self.vx_i * bord * (1 + loop/2000) * signe_x
        self.vy =  self.vy * bord + p_vy*0.1 #*sens
        if position in ("above","below"):
            self.vy += p_vy

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
            if self.y_v == None: y_v = ((self.ymin + self. ymax)/2 - self.ly/2)
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
    #nouvel envoi de balle
    def reset(self):
        self.vy = 0
        if self.ia: self.y_v = None

    #affichage de la PLATEFORME
    def draw(self):
        win.blit(self.img, (self.x, self.y))

#détection des différentes interactions entre les objets

def contact(player,balle,n):
    if  player.x + player.lx//2 < balle.x < player.x + player.lx + balle.radius:
        ###RIGHT###
        if (player.x + player.lx >= balle.x - balle.radius
            and player.y <= balle.y <= player.y + player.ly):
            print("directement à droite", n)
            return "right"

        elif (player.y + player.ly//2>= balle.y >= player.y - balle.radius*math.sqrt(2)//2
            and balle.x >= player.x + player.lx + balle.radius*math.sqrt(2)//2
            and math.sqrt((balle.x - player.x - player.lx)**2 + (balle.y - player.y)**2) <= balle.radius):
            print("à droite (du haut)", n)
            return "right"

        elif (player.y  + player.ly//2 <= balle.y <= player.y + player.ly + balle.radius*math.sqrt(2)//2
              and balle.x >= player.x + player.lx + balle.radius*math.sqrt(2)//2
              and math.sqrt((balle.x - player.x - player.lx)**2 + (balle.y - player.y - player.ly)**2) <= balle.radius):
            print("à droite (du bas)", n)
            return "right"

    ###RIGHT###
    ###LEFT###
    elif (player.x >= balle.x + balle.radius
        and player.y <= balle.y <= player.y + player.ly):
        print("directement à gauche", n)
        return "left"

    elif (player.y + player.ly//2 >= balle.y >= player.y - balle.radius*math.sqrt(2)//2
        and balle.x + balle.radius*math.sqrt(2)//2 <= player.x
        and math.sqrt((balle.x - player.x)**2 + (balle.y - player.y)**2) <= balle.radius):
        print("à gauche (du haut)", n)
        return "left"

    elif (player.y  + player.ly//2 <= balle.y <= player.y + player.ly + balle.radius*math.sqrt(2)//2
          and balle.x + balle.radius*math.sqrt(2)//2 >= player.x
          and math.sqrt((balle.x - player.x)**2 + (balle.y - player.y - player.ly)**2) <= balle.radius):
        print("à gauche (du bas)", n)
        return "left"

    ###LEFT###
    ###ABOVE###
    elif (player.x <= balle.x <= player.x + player.lx
        and player.y >= balle.y + balle.radius):
        print("directement au dessus", n)
        return "above"

    elif (balle.x <= player.x + player.lx + balle.radius*math.sqrt(2)//2
        and balle.y <= player.y - balle.radius * math.sqrt(2)//2
        and balle.vy > 0
        and math.sqrt((balle.x - player.x - player.lx)**2 + (balle.y - player.y)**2) <= balle.radius):
        print("au dessus (à droite)", n)
        return "above"

    elif (balle.x >= player.x - balle.radius*math.sqrt(2)//2
        and balle.y <= player.y - balle.radius*math.sqrt(2)//2
        and balle.vy > 0
        and math.sqrt((balle.x - player.x - player.lx)**2 + (balle.y - player.y)**2) <= balle.radius):
        print("au dessus (à gauche)", n)
        return "above"

    ###ABOVE###
    ###BELOW###
    elif (player.x <= balle.x <= player.x + player.lx
          and player.y + player.ly >= balle.y - balle.radius):
        print("directement au dessous", n)
        return "below"

    elif (balle.x <= player.x + player.lx + balle.radius*math.sqrt(2)//2
        and balle.y >= player.y - balle.radius*math.sqrt(2)//2
        and balle.vy < 0
        and math.sqrt((balle.x - player.x - player.lx)**2 + (balle.y - player.y - player.ly)**2) <= balle.radius):
        print("au dessous mais trigo", n)
        return "below"

    elif (balle.x >= player.x - balle.radius*math.sqrt(2)//2
         and balle.y >= player.y - balle.radius*math.sqrt(2)//2
         and balle.vy < 0
         and math.sqrt((balle.x - player.x - player.lx)**2 + (balle.y - player.y - player.ly)**2) <= balle.radius):
        print("au dessous mais trigo", n)
        return "below"


def interactions(players, balle, n):#, simulation=False, coor=None):
    global last_r

    p =- 1
    if balle.x < players[0].x + players[0].lx + balle.radius + balle.vx + 10: p = 0
    elif balle.x > players[1].x - balle.radius - balle.vx - 10: p = 1
    if p != -1:
        c = contact(players[p], balle, n)
        if c: balle.rebond(players[p].vy, n, c)
        else:
            s = False
            py = int(players[p].y)
            bx , by = int(balle.x), int(balle.y)
            if max(abs(players[p].vy), abs(balle.vy), abs(balle.vx)) == abs(balle.vx):
                for simx in range(int(abs(balle.vx))):
                    players[p].y = int(py + (simx * players[p].vy / abs(balle.vx)))
                    balle.y = int(by + (simx * balle.vy / abs(balle.vx)))
                    balle.x = int(bx + (simx * balle.vx / abs(balle.vx)))
                    c = contact(players[p], balle, n)
                    if c:
                        balle.freeze()
                        players[p].freeze()
                        s = True
            elif max(abs(players[p].vy), abs(balle.vy), abs(balle.vx)) == abs(balle.vy):
                for simy in range(int(abs(balle.vy))):
                    players[p].y = int(py + (simx * players[p].vy / abs(balle.vy)))
                    balle.y = int(by + (simx * balle.vy / abs(balle.vy)))
                    balle.x = int(bx + (simx * balle.vx / abs(balle.vy)))
                    c = contact(players[p], balle, n)
                    if c:
                        balle.freeze()
                        players[p].freeze()
                        s = True
            elif max(abs(players[p].vy), abs(balle.vy), abs(balle.vx)) == abs(players[p].vy):
                for simx in range(int(abs(players[p].vy))):
                    players[p].y = int(py + (simx * players[p].vy / abs(players[p].vy)))
                    balle.y = int(by + (simx * balle.vy / abs(players[p].vy)))
                    balle.x = int(bx + (simx * balle.vx / abs(players[p].vy)))
                    c = contact(players[p], balle, n)
                    if c:
                        balle.freeze()
                        players[p].freeze()
                        s = True
            if not s:
                players[p].y = py
                balle.x = bx
                balle.y = by


# """  ###BELOW###
#         ###CALCULATIONS###
#         if (not simulation
#             and last_r != 0
#             and (x + balle.vx <= players[0].x + players[0].lx + balle.radius
#             and  players[0].y - balle.radius - abs(players[0].vy) <= balle.y + balle.vy <= players[0].y + players[0].ly + balle.radius + abs(players[0].vy))):
#             print("début boucle", x, players[0].x + players[0].lx + balle.radius, int(x + balle.vx) - 1)
#             y_b = players[0].y
#             print(f"### {n} ###")
#             ni = abs(players[0].x + players[0].lx + balle.radius -(int(x + balle.vx) - 1)) #number of iterations
#             for sim_x in range(players[0].x + players[0].lx + balle.radius, int(x + balle.vx) - 1, -1):
#                 #players[0].y = int(y_b - players[0].vy / (sim_x - ni))
#                 result = interactions(players, balle, n, simulation=True, coor=(sim_x, sim_x*balle.vy//balle.vx + y-x*balle.vy//balle.vx))
#                 if result:
#                     print(balle.vy)
#                     balle.vy = sim_x*balle.vy//balle.vx + y-x*balle.vy//balle.vx - y
#                     balle.vx = sim_x - x
#                     print(" -- -- ",sim_x, balle.vx, balle.vy)
#                     break
#             else: print(" -- --  Pas trouvé !")
#             players[0].y = y_b
#
#         if simulation: return False
# """
    #si la balle touche le haut ou la bas du terrain
    if balle.y - balle.radius <= 120 or balle.y + balle.radius >= HEIGHT-20:
        balle.rebond(0, n, "wall")

    #si la balle touche la gauche ou la droite du terrain
    if balle.x - balle.radius < 0 or balle.x + balle.radius > WIDTH:
        #arreter le jeu
        return False

    #continuer le jeu
    return True



####~~~~~~~~~~~~####+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+--+-+-+--+-+-+####
#fonction principale
def main():
    global last_r
    #création des objets
    players = [Plateform(100,     (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 0),
               Plateform(WIDTH-110, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 1, True, 15)]
    balle = Ball(WIDTH//2, HEIGHT//2 - 10, 5, rd.randint(-50, 50)/10, 35)

    #nombre d'itérations et variable de boucle principale
    n = 0
    running = True

    #aspect aléatoire de la vitesse verticale de la balle au début
  #  balle.vy = rd.randint(-5, 5)

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
            if keys[pg.K_RIGHT]:
                if pause_e:
                    pause = not pause
                    pause_e = False
            else: pause_e = True
        if pause:
            continue

        # + 1 itération à la boucle principale
        n += 1

        #mise à 0 de la vitesse verticale de chaque joueur
        for i in players: i.vy = 0

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