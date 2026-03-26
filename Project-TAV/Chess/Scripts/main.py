"""
Tour de contrôle de tous les scripts.
"""

import pygame as pg
import os
import const
import board
import game
import mouse_keys as mk
import menu

os.chdir(os.path.dirname(__file__))


class Gestionary:
    def __init__(self):
        pg.init()
        self.win = pg.display.set_mode((const.WIDTH + 5 * const.SQUARE, const.HEIGHT))
        pg.display.set_caption("Chess")
        self.win.fill((50, 50, 50))
        self.chess_game = game.Game(self)
        self.mouse_pos = None

    def run(self):
        running = True

        const.start_sound.play()

        while running:
            self.mouse_pos = pg.mouse.get_pos()
            user_input = pg.key.get_pressed()

            game.left_click_up = None
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if user_input[pg.K_a]:
                    board.theme_index = (board.theme_index+1)%const.NMB_THEMES

                if user_input[pg.K_LEFT]:
                    if self.chess_game.index_position > 0:
                        self.chess_game.index_position -= 1
                        self.chess_game.update_position()

                if user_input[pg.K_RIGHT]:
                    if self.chess_game.index_position + 1 < len(self.chess_game.list_position):
                        self.chess_game.index_position += 1
                        self.chess_game.update_position()

                if user_input[pg.K_DOWN]:
                    self.chess_game.index_position = 0
                    self.chess_game.update_position()

                if user_input[pg.K_UP]:
                    self.chess_game.index_position = len(self.chess_game.list_position)-1
                    self.chess_game.update_position()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.chess_game.left_click_up = None
                    coor =  mk.mouse_to_coor(self.mouse_pos)
                    if coor and (self.chess_game.candidate_move[0] is not None or board.color_and_occupied_square(self, coor[0], coor[1])):
                        self.chess_game.left_click_down = coor

                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    coor = mk.mouse_to_coor(self.mouse_pos)
                    if coor is None: #if click up out of the board
                        self.chess_game.left_click_down = None
                    elif coor and self.chess_game.left_click_down:
                        self.chess_game.left_click_up = coor


            if self.chess_game.human:
                self.chess_game.input_to_candidate_move()
                if (all(item is not None for item in self.chess_game.candidate_move[:2])
                    and board.color_and_occupied_square(self, self.chess_game.candidate_move[0], self.chess_game.candidate_move[1]) == self.chess_game.player_turn):
                    if ((len(self.chess_game.legal_moves_list) == 0 or len(self.chess_game.illegal_moves_list) == 0)
                        or self.chess_game.calculated != self.chess_game.candidate_move[:2]):
                        self.chess_game.get_all_legal_moves()
                        self.chess_game.calculated = self.chess_game.candidate_move[:2]
                    if all(item is not None for item in self.chess_game.candidate_move[2:]):
                        eval(f"self.chess_game.{self.chess_game.player_turn}_player.move(self)")

            else:
                pass

            print(self.chess_game.left_click_down)
            self.win.fill((50, 50, 50))
            board.draw_board(self)
            board.draw_coor(self)
            board.draw_pieces(self)
            board.blit_legal_moves(self)
            board.write_player_turn(self)

            pg.display.update()

        #menu.main_menu(gestionary)





if __name__ == "__main__":
    gestionary = Gestionary()
    menu.main_menu(gestionary)
    #gestionary.run()
