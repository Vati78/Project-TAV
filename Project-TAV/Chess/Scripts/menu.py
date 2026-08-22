import pygame as pg, sys
import time
import main
from pygame.constants import MOUSEBUTTONDOWN


class Button:
    def __init__(self, x, y, w, h, image, image_i=None, enabled=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.transform.scale(pg.image.load(f"../Images/{image}.png"), (self.w,self.h))
        if image_i:
            self.image_i = pg.transform.scale(pg.image.load(f"../Images/{image_i}.png"), (self.w,self.h))
        self.is_invert = False
        self.enabled = enabled

    def draw(self,win):
        if self.enabled: win.blit(self.image, (self.x,self.y))
        #else: pg.draw.rect(win.win, (10,12,35), (self.x,self.y,self.w,self.h))

    def if_input(self, pos):
        """if mouse is in the button"""
        x, y = pos
        if self.x<=x<=self.x+self.w and self.y<=y<=self.y+self.h and self.enabled:
            return True

    def invert(self):
        if self.image_i:
            image = self.image_i
            self.image_i = self.image
            self.image = image
            self.is_invert = not self.is_invert
class Image:
    def __init__(self, x, y, w, h, image, enabled = True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.transform.scale(pg.image.load(f"../Images/{image}.png"), (self.w, self.h))
        self.enabled = enabled

    def draw(self,win):

        if self.enabled: 
            win.blit(self.image, (self.x,self.y))

        #else: pg.draw.rect(win.win, (10, 12, 35), (self.x, self.y, self.w, self.h))


def main_menu(o = None):
    """
    main menu of the game
    :return: (exit: {0 : quit, 1 : play, 2 : review game}, options)
    """
    win = pg.display.set_mode((910, 560))
    win.fill((10, 12, 35))
    buttons = [Button(300,100,300,86,"play"),
               Button(300,230,300,86,"options"),
               Button(300,360,300,86,"exit")]
    
    
    if o is None: o = [2,1,"r",False]
    
    # since the time effect isn't already effective in the script,
    # we separate the time and other options for now

    timer = [10,0] # [Nb of min, Nb of seconds]
    
    cur_partie = True
    
    while cur_partie:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons[0].if_input(pg.mouse.get_pos()):
                        return 1, o # plays a game with o as options

                    if buttons[1].if_input(pg.mouse.get_pos()):
                        o = options(win, o, timer )

                    if buttons[2].if_input(pg.mouse.get_pos()):
                        return 0, o # quit the pygame window
        win.fill((10, 12, 35))
        for button in buttons: button.draw(win)
        pg.display.update()


def options(win, o , timer):
    """

    :param win:
    :param o: current options
    :param timer: temporary, will be integrated in o
    :return: nb of players, difficulty (1-3), color (w,b,r), time [if 2 players else None] [nb of min, nb of sec]
    """
    
    win.fill((10, 12, 35))
    images = [Image(20, 170, 260, 50, "nb_player"),
              Image(20,240, 205, 50, "difficulty"),
              Image(20, 320, 115, 35, "color"),
              Image(20,280, 125, 45, "time", False if o[0] == 1 else True),
              Image(400,280,80,45,"min",False if o[0] == 1 else True),
              Image(700,280,70,45,"sec",False if o[0] == 1 else True),
              Image(300,20,350,100, "options")]
    
    
              
    buttons = [Button(20,420,300,86,"back"),
               Button(400,170,50,50,"1", "1_i"),
               Button(700,170,50,50,"2", "2_i"),
               Button(282,240,158,50,"beginner", "beginner_i"),
               Button(470,240,235,50,"intermediate", "intermediate_i"),
               Button(730,240,127,50,"master", "master_i"),
               Button(225,310,104,50,"white", "white_i"),
               Button(440,310,100,50,"black", "black_i"),
               Button(641,310,146,50,"random", "random_i"),
               Button(275,350,45,45,"-",None,False if o[0] == 1 else True),
               Button(325,350,45,45,"+",None,False if o[0] == 1 else True),
               Button(575,350,45,45,"-",None,False if o[0] == 1 else True),
               Button(625,350,45,45,"+",None,False if o[0] == 1 else True),
               Button(25,350,28*5,45,"activated","activated_i",False if o[0] == 1 else True)]
    
    
    buttons[o[0]].invert()
    buttons[2+o[1]].invert()
    buttons[6 if o[2]=="w" else (7 if o[2]=="b" else 8)].invert()
    
    if o[3]:
        for i in range(9,13):
            buttons[i].enabled = False
        buttons[13].invert()
        images[4].enabled = False
        images[5].enabled = False
    
    for i in range(3, 9):
        buttons[i].enabled = o[0]==1
    for i in range(1,3):
        images[i].enabled = o[0]==1

    ok = True # mdr =)
    fin_de_l_humanite = False
    
    while ok and not(fin_de_l_humanite): # tout va bien !! 
        pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons[0].if_input(pos):
                        ok = False
                        fin_de_l_humanite = True #=((((((
                        #main_menu(win)

                    for i in range(1,3):
                        if buttons[i].if_input(pos):
                            if not buttons[i].is_invert:
                                buttons[1].invert()
                                buttons[2].invert()
                                for j in range(3,14):
                                    if not (( 9 <= j <= 12) and buttons[13].is_invert):
                                        buttons[j].enabled = not buttons[j].enabled
                                
                                for j in range(1,6):
                                    if not (( 4 <= j <= 5) and buttons[13].is_invert):
                                        images[j].enabled = not images[j].enabled
                                
                                #print(images[1].enabled ,images[2].enabled, images[3].enabled)

                    for i in range(3,6):
                        if buttons[i].if_input(pos):
                            if not buttons[i].is_invert:
                                for j in range(3,6):
                                    if buttons[j].is_invert: buttons[j].invert()
                                buttons[i].invert()

                    for i in range(6,9):
                        if buttons[i].if_input(pos):
                            if not buttons[i].is_invert:
                                for j in range(6,9):
                                    if buttons[j].is_invert: buttons[j].invert()
                                buttons[i].invert()
                                
                    if buttons[13].if_input(pos):
                        buttons[13].invert()
                        
                        for i in range(9,13):
                            buttons[i].enabled = not buttons[i].enabled
                            
                        for i in range(4,6):
                            images[i].enabled = not images[i].enabled
                        
                        
                                
                    if buttons[9].if_input(pos):
                        if timer[0] > 0:
                            timer[0] -= 1
                            
                    if buttons[10].if_input(pos):
                        if timer[0] < 20:
                            timer[0] += 1
                            
                    if buttons[11].if_input(pos):
                        
                        if timer[1] == 59:
                            timer[1] = 55
                        elif timer[1] > 0:
                            timer[1] -= 5
                            
                    if buttons[12].if_input(pos):
                        if timer[1] < 55:
                            timer[1] += 5
                            
                        elif timer[1] == 55:
                            timer[1] = 59
                        

        win.fill((10,12,35))
        
        for button in buttons:
            button.draw(win)
            #print(button.is_invert, end ="; ")
        #print()
        
        
        for image in images: image.draw(win)
        
        if buttons[2].is_invert and  not buttons[13].is_invert:
            nb_min = str(timer[0])
            nb_sec = str(timer[1])
            
            for indice_min in range(len(nb_min) - 1,-1,-1):
                nom_chiffre = str(timer[0])[indice_min] + "_chiffre"
                image_indice_min = pg.transform.scale(pg.image.load(f"../Images/{nom_chiffre}.png"), (30, 45))              
                win.blit(image_indice_min, (330 - (len(str(timer[0])) - indice_min - 1) * 35 , 280))
                      
            for indice_sec in range(len(nb_sec) - 1,-1,-1):               
                nom_chiffre = str(timer[1])[indice_sec] + "_chiffre"
                image_indice_sec = pg.transform.scale(pg.image.load(f"../Images/{nom_chiffre}.png"), (30, 45))
                win.blit(image_indice_sec, (630 - (len(str(timer[1])) - indice_sec - 1) * 35 , 280))
                 
        
        pg.display.update()
        #print(timer)

        
    if buttons[1].is_invert:
        #print(1 if buttons[1].is_invert else 2, 1 if buttons[3].is_invert else (2 if buttons[4].is_invert else 3), "w" if buttons[6].is_invert else ("b" if buttons[7].is_invert else "r") , buttons[13].is_invert)
        return [1 if buttons[1].is_invert else 2, 1 if buttons[3].is_invert else (2 if buttons[4].is_invert else 3), "w" if buttons[6].is_invert else ("b" if buttons[7].is_invert else "r") , buttons[13].is_invert]
    else:
        if not buttons[13].is_invert:
            #print(1 if buttons[1].is_invert else 2, 1 if buttons[3].is_invert else (2 if buttons[4].is_invert else 3), "w" if buttons[6].is_invert else ("b" if buttons[7].is_invert else "r") , buttons[13].is_invert)

            return [1 if buttons[1].is_invert else 2, 1 if buttons[3].is_invert else (2 if buttons[4].is_invert else 3), "w" if buttons[6].is_invert else ("b" if buttons[7].is_invert else "r") , buttons[13].is_invert] #, timer
        else:
            #print(1 if buttons[1].is_invert else 2, 1 if buttons[3].is_invert else (2 if buttons[4].is_invert else 3), "w" if buttons[6].is_invert else ("b" if buttons[7].is_invert else "r") , buttons[13].is_invert)

            return [1 if buttons[1].is_invert else 2, 1 if buttons[3].is_invert else (2 if buttons[4].is_invert else 3), "w" if buttons[6].is_invert else ("b" if buttons[7].is_invert else "r") , buttons[13].is_invert]

