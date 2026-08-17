"""
Tour de contrôle de tous les scripts.
"""
import sys

import pygame as pg
import os
import const
import board
import game
import mouse_keys as mk
import menu
import player_bot as pb
import sound
from random import choice
import time

os.chdir(os.path.dirname(__file__))

class Gestionary:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Chess")
        pg.display.set_icon(pg.image.load("../Images/icon.png"))
        self.win = pg.display.set_mode((const.WIDTH + 5 * const.SQUARE, const.HEIGHT))
        self.win.fill((50, 50, 50))
        self.chess_game = game.Game(self)
        self.mouse_pos = None
        self.previous_mouse_pos = []
        self.input = False
        self.changed_position = False
        self.illegal_move_time = 0

    def run(self, o):
        """
        :param o: nb of players, difficulty, color
        :return:
        """
        if o[2] not in ["w","b"]: o[2] = choice(["w","b"])
        self.chess_game.players = [pb.Player("w") if o[0]==2 or o[2]=="w" else pb.Bot("w"), pb.Player("b") if o[0]==2 or o[2]=="b" else pb.Bot("b")]


        running = True

        const.start_sound.play()
        self.chess_game.left_click_up = [None,None,None,None,None]

        active_key = None
        cooldown = 0

        self.chess_game.get_all_legal_moves(self.chess_game.player_turn)
        self.chess_game.list_position.append(self.chess_game.status_to_key())


        while running:
            self.mouse_pos = pg.mouse.get_pos()
            if cooldown: cooldown -= 1
            if self.illegal_move_time: self.illegal_move_time -= 1

            ################################

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN: active_key = pg.K_DOWN
                    elif event.key == pg.K_UP: active_key = pg.K_UP
                    elif event.key == pg.K_LEFT: active_key = pg.K_LEFT
                    elif event.key == pg.K_RIGHT: active_key = pg.K_RIGHT
                    elif event.key == pg.K_a: active_key = pg.K_a
                    else: active_key = event.key

                elif event.type == pg.KEYUP:
                    if event.key == active_key:
                        active_key = None

                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.chess_game.left_click_down = mk.mouse_to_coor(self.mouse_pos)
                    self.input = True

                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.chess_game.left_click_down = 0
                    self.chess_game.left_click_up = mk.mouse_to_coor(self.mouse_pos)
                    self.input = True

            ################################

            # change position or theme
            if active_key == pg.K_a:
                if not cooldown:
                    board.theme_index = (board.theme_index+1)%const.NMB_THEMES
                    cooldown = 20

            elif active_key == pg.K_LEFT:
                if not cooldown and self.chess_game.index_position:
                    self.chess_game.index_position -= 1
                    self.chess_game.player_turn ^= 1

                    self.changed_position = True

            elif active_key == pg.K_RIGHT:
                if not cooldown and self.chess_game.index_position + 1 != len(self.chess_game.list_position):
                    self.chess_game.index_position += 1
                    self.chess_game.player_turn ^= 1

                    self.changed_position = True

            elif active_key == pg.K_DOWN:
                if not cooldown and self.chess_game.index_position:
                    self.chess_game.index_position = 0
                    self.chess_game.player_turn = 0

                    self.changed_position = True

            elif active_key == pg.K_UP:
                if not cooldown and self.chess_game.index_position + 1 != len(self.chess_game.list_position):
                    self.chess_game.index_position = len(self.chess_game.list_position) - 1
                    self.chess_game.player_turn = self.chess_game.index_position % 2

                    self.changed_position = True

            elif active_key == pg.K_q:
                running = False

            if self.changed_position:
                self.chess_game.candidate_move = [0, 0]
                self.chess_game.legal_moves = 0

                self.chess_game.key_to_status(self.chess_game.list_position[self.chess_game.index_position])

                cooldown = 20

            ################################

            if isinstance(self.chess_game.players[self.chess_game.player_turn], pb.Player) or self.chess_game.index_position + 1 != len(self.chess_game.list_position):
                if self.input:
                    self.chess_game.input_to_candidate_move()

                if self.chess_game.illegal_move:
                    const.illegal_sound.play()
                    self.illegal_move_time = const.ILLEGAL_MOVE_DURATION

                    self.chess_game.illegal_move = False

                if self.changed_position:
                    sound.play_sound(self)
                    self.chess_game.sound_to_play = 0

                if self.chess_game.candidate_move[1]:
                    self.chess_game.players[self.chess_game.player_turn].move(self)

                    if self.chess_game.check:
                        self.illegal_move_time = const.ILLEGAL_MOVE_DURATION

            else:
                self.chess_game.players[self.chess_game.player_turn].return_move(self)

            self.win.fill((50, 50, 50))
            board.draw_board(self)
            board.draw_coor(self)
            board.blit_legal_moves(self, self.chess_game.player_turn, self.chess_game.candidate_move[0])
            board.draw_pieces(self)
            board.write_player_turn(self)

            pg.display.update()

            if self.chess_game.result is not None:
                print("game ended")
                running = False
                time.sleep(5)

            self.input = False
            self.changed_position = False
            self.previous_mouse_pos.append(self.mouse_pos[0])

            if len(self.previous_mouse_pos) > 5: del self.previous_mouse_pos[0]


    def promoting(self, color, col):
        board.draw_board(self)
        board.draw_coor(self)
        board.draw_pieces(self)

        pg.draw.rect(self.win, (255, 255, 255), (col * const.SQUARE, 4*color*const.SQUARE, const.SQUARE, 4 * const.SQUARE))

        list_pieces = [4, 3, 1, 2]

        for i, piece in enumerate(list_pieces):
            if not color:
                self.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/white{const.PIECES[piece]}.png"),
                    (const.SQUARE, const.SQUARE)),
                    (col * const.SQUARE, i*const.SQUARE))

            else:
                self.win.blit(pg.transform.scale(pg.image.load(f"../Sprites/Pieces_bitboards/black{const.PIECES[piece]}.png"),
                    (const.SQUARE, const.SQUARE)),
                    (col * const.SQUARE, (7 - i)*const.SQUARE))


        pg.display.update()

        promote = True

        while promote:
            mouse_pos = pg.mouse.get_pos()

            coor = mk.mouse_to_coor(mouse_pos).bit_length() - 1
            x = coor%8
            y = coor//8

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if x == col:
                        if not color and 0 <= y <= 3: return list_pieces[y]
                        elif color and 4 <= y <= 7: return list_pieces[7-y]
                    self.chess_game.left_click_down = 0
                    return False


if __name__ == "__main__":
    o = None
    while True:
        c,o = menu.main_menu(o)
        if c == 1: # play game
            gestionary = Gestionary()
            gestionary.run(o)
        elif c == 2: # review previous game (not implemented)
            pass
        else: # quit
            pg.quit()
            sys.exit()