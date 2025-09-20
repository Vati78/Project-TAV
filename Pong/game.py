import pygame as pg, math, os, time, random as rd

pg.init()
os.chdir(os.path.abspath(__file__)[0:-8])

"""
Constants and initialization
"""
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

#création de la classe BALLE
class Ball:
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

    #détection d'un rebond 
    def rebond(self, p_vy, loop, position):
        #p_vy: vy de la plateforme; position: relative to the plateform; touche_exterieur: haut ou bas de l'écran
        bord = -1 if position in ("above","below","wall") else 1
        signe_x = -1 if (self.vx < 0) else 1
        if position in ("right","left"): signe_x = 1 if position == "left" else -1
        #signe_y = -1 if self.vy < 0 else 1
        #sens = -1 if self.vy > 0 and p_vy > 0 else 1
        self.vx = - self.vx_i * bord * (1 + loop/2000) * signe_x
        self.vy =  self.vy * bord + p_vy*0.1 #*sens
        if position in ("above","below"):
            self.vy += p_vy

    #affichage de la balle
    def draw(self):
        win.blit(self.image, (self.x-self.radius, self.y-self.radius))

    #déplacement de la balle
    def move(self):
        self.x += self.vx
        self.y += self.vy

#création de la classe PLATEFORME
class Plateform:
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
                if self.diff != "":
                    if self.count >= self.diff + int(self.diff * (rd.random()- 0.5)/4):
                        self.count = 0
                        self.y_v = rd.randint(self.ymin, self.ymax-self.ly)
            elif ball.vx<0: self.y_v = None
            if self.y_v == None: y_v = ((self.ymin + self. ymax)/2 - self.ly/2)
            else: y_v = self.y_v
            vy=0
            if abs(y_v - self.y) >= self.vmax: vy = 1 if y_v - self.y > 0 else -1
        vy *= self.vmax
        if self.ymin < self.y + vy < self.y + vy + self.ly < self.ymax:
            self.y += vy
            self.vy = vy


    #remise à 0 de la vitesse verticale
    def reset(self):
        self.vy = 0

    #affichage de la PLATEFORME
    def draw(self):
        win.blit(self.img, (self.x, self.y))

#détection des différentes interactions entre les objets
def interactions(players, balle, n):
    #si la balle se déplace vers la gauche
    if balle.vx < 0:
        #si la balle se trouve sur la ligne verticale de la plateforme
        if players[0].x + players[0].lx == balle.x -balle.radius:
            #si elle est au niveau de la plateforme
            if players[0].y - (math.sqrt(2) * balle.radius // 2) < balle.y < players[0].y + players[0].ly + (math.sqrt(2) * balle.radius // 2):
                balle.rebond(players[0].vy, n, "right")

            

        #si à la prochaine itération la balle dépassera la ligne vertivale de la plateforme
        elif balle.x -balle.radius + balle.vx < players[0].x + players[0].lx < balle.x -balle.radius:
            #si à la prochaine itération, la balle tapera au milieu de la raquette
            if players[0].y + players[0].vy - (math.sqrt(2) * balle.radius // 2) - 5< balle.y + balle.vy < players[0].y + players[0].ly + players[0].vy + (math.sqrt(2) * balle.radius // 2) + 5:
                balle.vx = players[0].x + players[0].lx - balle.x + balle.radius
            
        if balle.vy >= 0:
            if balle.x - balle.radius <= players[0].x <= balle.x + balle.radius and balle.y < players[0].y < balle.y + balle.radius + 10:
                balle.rebond(players[0].vy, n, "above")
                
            
        if balle.vy <= 0:
            if balle.x - balle.radius <= players[0].x <= balle.x + balle.radius and balle.y > players[0].y + players[0].ly < balle.y + balle.radius + 10:
                balle.rebond(players[0].vy, n, "below")
   
    #si la balle se déplace vers la droite
    if balle.vx > 0:
        if balle.x >= players[1].x and balle.x - balle.vx >= players[1].x:
            return False
        elif (players[1].y <= balle.y <= players[1].y + players[1].ly
                and balle.x + balle.radius >= players[1].x):
            balle.rebond(players[1].vy, n, 0)
        # if the ball is above the Plateform
        elif players[1].y - balle.radius + 1 <= balle.y <= players[1].y and math.sqrt((balle.y - players[1].y) ** 2 + (balle.x - players[1].x) ** 2) <= balle.radius:
                balle.rebond(players[1].vy, n, players[1].y-balle.y-balle.radius)
        # if the ball is below the Plateform
        elif players[1].y + players[1].ly <= balle.y <= players[1].y + players[1].ly + balle.radius:
            if math.sqrt(
                    (balle.y - (players[1].y + players[1].ly)) ** 2 + (balle.x - players[1].x) ** 2) <= balle.radius:
                balle.rebond(players[1].vy, n, players[1].y+players[1].ly-balle.y-balle.radius)

    #si la balle touche le haut ou la bas du terrain
    if balle.y - balle.radius <= 120 or balle.y + balle.radius >= HEIGHT-20:
        balle.rebond(0, n, "wall")

    #si la balle touche la gauche ou la droite du terrain
    if balle.x - balle.radius < 0 or balle.x + balle.radius > WIDTH:
        #arreter le jeu
        return False

    #continuer le jeu
    return True

#fonction principale
def main():
    #création des objets
    players = [Plateform(100,     (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 0),
               Plateform(WIDTH-110, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 1, True, 15)]
    balle = Ball(WIDTH//2, HEIGHT//2 - 10, 5, 0, 35)

    #nombre d'itérations et variable de boucle principale
    n = 0
    running = True

    #aspect aléatoire de la vitesse verticale de la balle au début
    balle.vy = rd.randint(-5, 5)

    #initialisation de l'horloge
    clock = pg.time.Clock()

    #chargement des images de fond
    fond = pg.image.load(f"Images/terrain.png")
    haut = pg.image.load(f"Images/haut.png")
    police = pg.font.SysFont("Arial", 45)

    #boucle principale
    while running:
        # + 1 itération à la boucle principale
        n += 1

        #mise à 0 de la vitesse verticale de chaque joueur
        for i in players: i.reset()

        #détection d'un éventuel évenement menant à une fermeture de pygame
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        #collecte de tous les éléments
        keys = pg.key.get_pressed()

        #mouvements du jour 0
        if keys[pg.K_DOWN]:
            players[0].move(1)
        if keys[pg.K_UP]:
            players[0].move(-1)

        #mouvement de la balle
        balle.move()

        #mouvement du bot
        #players[1].y = balle.y - players[1].ly//2
        players[1].move(0, balle)

        #terminer le jeu si aucune interaction quand la balle sort du terrain
        if running:
            #pas d'interaction+
            if not interactions(players, balle, n): # n  loop (car loop != 0)
                time.sleep(1)
                # attitrage des points
                if balle.vx < 0:
                    players[1].nmb_points += 1
                else:
                    players[0].nmb_points += 1
                del balle
                #recréation d'une nouvelle partie
                for i in (0, 1):
                    players[i].y = (HEIGHT-100)//2
                balle = Ball(WIDTH // 2, HEIGHT // 2 - 10, 5, 0, 35)
                balle.vy = rd.randint(-1,-1)
                n = 0

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