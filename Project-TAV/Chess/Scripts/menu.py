import pygame as pg, sys
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

    def draw(self,gestionary):
        if self.enabled: gestionary.win.blit(self.image, (self.x,self.y))
        else: pg.draw.rect(gestionary.win, (10,12,35), (self.x,self.y,self.w,self.h))

    def if_input(self, pos):
        """if mouse is in the button"""
        x, y = pos
        if self.x<=x<=self.x+self.w and self.y<=y<=self.y+self.h:
            return True

    def invert(self):
        if self.image_i:
            image = self.image_i
            self.image_i = self.image
            self.image = image
            self.is_invert = not self.is_invert
class Image:
    def __init__(self, x, y, w, h, image):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pg.transform.scale(pg.image.load(f"../Images/{image}.png"), (self.w, self.h))
        self.enabled = True

    def draw(self,gestionary):
        if self.enabled: gestionary.win.blit(self.image, (self.x,self.y))
        else: pg.draw.rect(gestionary.win, (10, 12, 35), (self.x, self.y, self.w, self.h))

def main_menu(gestionary):
    gestionary.win.fill((10, 12, 35))
    buttons = [Button(300,100,300,86,"play"),
               Button(300,230,300,86,"options"),
               Button(300,360,300,86,"exit")]
    o = [1,1,"r"]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons[0].if_input(pg.mouse.get_pos()):
                        gestionary.run(o)
                        pg.quit()
                        sys.exit()

                    if buttons[1].if_input(pg.mouse.get_pos()):
                        o = options(gestionary, o)

                    if buttons[2].if_input(pg.mouse.get_pos()):
                        pg.quit()
                        sys.exit()
        gestionary.win.fill((10, 12, 35))
        for button in buttons: button.draw(gestionary)
        pg.display.update()

def options(gestionary, o):
    """

    :param gestionary:
    :param o: current options
    :return: nb of players, difficulty (1-3), color (w,b,r)
    """
    gestionary.win.fill((10, 12, 35))
    images = [Image(20, 170, 260, 50, "nb_player"),
              Image(20,240, 205, 50, "difficulty"),
              Image(20, 320, 115, 35, "color"),
              Image(300,20,350,100, "options")]
    buttons = [Button(20,420,300,86,"back"),
               Button(400,170,50,50,"1", "1_i"),
               Button(700,170,50,50,"2", "2_i"),
               Button(282,240,158,50,"beginner", "beginner_i"),
               Button(470,240,235,50,"intermediate", "intermediate_i"),
               Button(730,240,127,50,"master", "master_i"),
               Button(225,310,104,50,"white", "white_i"),
               Button(440,310,100,50,"black", "black_i"),
               Button(641,310,146,50,"random", "random_i")]
    buttons[o[0]].invert()
    buttons[2+o[1]].invert()
    buttons[6 if o[2]=="w" else (7 if o[2]=="b" else 8)].invert()
    for i in range(3, 9):
        buttons[i].enabled = o[0]==1
    for i in range(1,3):
        images[i].enabled = o[0]==1

    ok = True
    while ok:
        pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons[0].if_input(pos):
                        ok = False
                        #main_menu(gestionary)

                    for i in range(1,3):
                        if buttons[i].if_input(pos):
                            if not buttons[i].is_invert:
                                buttons[1].invert()
                                buttons[2].invert()
                                for j in range(3,9):
                                    buttons[j].enabled = not buttons[j].enabled
                                images[1].enabled = not images[1].enabled
                                images[2].enabled = not images[2].enabled

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

        for button in buttons:
            button.draw(gestionary)
            print(button.is_invert, end ="; ")
        print()
        for image in images: image.draw(gestionary)
        pg.display.update()
    return [1 if buttons[1].is_invert else 2, 1 if buttons[3].is_invert else (2 if buttons[4].is_invert else 3), "w" if buttons[6].is_invert else ("b" if buttons[7].is_invert else "r")]

