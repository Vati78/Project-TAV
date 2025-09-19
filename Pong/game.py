import pygame as pg
import math
import random as rd
import os
import time


pg.init()

os.chdir(os.path.abspath(__file__)[0:-8])

"""
Constants and initialization
"""
#dimensions de la fenetre PYGAME
WIDTH = 1000
HEIGHT = 600

#création de la fenetre PYGAME
win = pg.display.set_mode((WIDTH, HEIGHT))
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
        self.vx_i = vx
        self.vy_i = vy
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.image = pg.image.load(f"Images/Balle.png")

    #détection d'un rebond 
    def rebond(self, p_vy, loop, coeff, touche_exterieur=False): #p_vy: vy de la plateforme; touche_exterieur: haut ou bas de l'écran
        bord = -1 if touche_exterieur else 1
        signe_x = -1 if self.vx < 0 else 1
        #signe_y = -1 if self.vy < 0 else 1
        #sens = -1 if self.vy > 0 and p_vy > 0 else 1
        if coeff != 0:
            #A = math.pi/2 - coeff/self.radius * math.pi/2
            #print(A, coeff)
          #  vx = self.vx
           # self.vx = -math.cos(2*A)*self.vx + math.sin(2*A)*self.vy
            #self.vy = math.sin(2*A)*vx + math.cos(2*A)*self.vy
            #del vx
            nx, ny = coeff, self.radius * (1 if coeff > 0 else -1)
            norm = math.sqrt(nx*nx + ny*ny)
            nx, ny = nx / norm, ny / norm

            # réflexion vectorielle
            dot = self.vx * nx + self.vy * ny
            self.vx = self.vx - 2 * dot * nx
            self.vy = self.vy - 2 * dot * ny

        else:
            self.vx = - self.vx_i * bord * (1 + loop/2000) * signe_x
            self.vy =  self.vy * bord + p_vy*0.1 #*sens

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
    def __init__(self, x, y, lx, ly, ymax, ymin, color, index):
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

    #déplacement de la PLATEFORME
    def move(self, vy):
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
        if balle.x <= players[0].x + players[0].lx and balle.x - balle.vx <= players[0].x + players[0].lx:
            pass#return False
        elif (players[0].y <= balle.y <= players[0].y + players[0].ly
                and balle.x - balle.radius <= players[0].x + players[0].lx):
            balle.rebond(players[0].vy, n, 0)
        # if the ball is above the plateform
        elif players[0].y - balle.radius + 1 <= balle.y <= players[0].y and math.sqrt(
                    (balle.y - players[0].y) ** 2 + (balle.x - (players[0].x + players[0].lx)) ** 2) <= balle.radius:
                balle.rebond(players[0].vy, n, players[0].y-balle.y-balle.radius)
        # if the ball is below the Plateform
        elif players[0].y + players[0].ly <= balle.y <= players[0].y + players[0].ly + balle.radius:
            if math.sqrt((balle.y - (players[0].y + players[0].ly)) ** 2 + (
                    balle.x - (players[0].x + players[0].lx)) ** 2) <= balle.radius:
                balle.rebond(players[0].vy, n, players[0].y+players[0].ly-balle.y-balle.radius)

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
        balle.rebond(0, n, 0, True)

    #si la balle touche la gauche ou la droite du terrain
    if balle.x - balle.radius < 0 or balle.x + balle.radius > WIDTH:
        #arreter le jeu
        return False

    #continuer le jeu
    return True

#fonction principale
def main():
    #création des objets
    players = [Plateform(100, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 0), Plateform(WIDTH-110, (HEIGHT-100)//2, 10, 100, HEIGHT-20, 120, GREEN, 1)]
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
        players[1].y = balle.y - players[1].ly//2

        #terminer le jeu si aucune interaction quand la balle sort du terrain
        if running:
            #pas d'interaction+
            if not interactions(players, balle, n):
                time.sleep(1)
                del balle
                for i in range(1): del players[i]
                #recréation d'une nouvelle partie
                players = [Plateform(100, (HEIGHT - 100) // 2, 10, 100, HEIGHT - 20, 120, GREEN, 0),
                           Plateform(WIDTH - 110, (HEIGHT - 100) // 2, 10, 100, HEIGHT - 20, 120, GREEN, 1)]
                balle = Ball(WIDTH // 2, HEIGHT // 2 - 10, 5, 0, 35) 
                n = 0

        #affichage de tous les éléments
        win.blit(fond, (0, 100))
        win.blit(haut, (0, 0))
        balle.draw()
        for i in enumerate(players): i[1].draw()

        #mise à jour de la fenetre pygame
        pg.display.update()
        clock.tick(120)

main()


