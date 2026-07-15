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
import player_bot as pb
import pieces

os.chdir(os.path.dirname(__file__))

class Gestionary:
    def __init__(self):
        pg.init()
        self.win = pg.display.set_mode((const.WIDTH + 5 * const.SQUARE, const.HEIGHT))
        pg.display.set_caption("Chess")
        self.win.fill((50, 50, 50))
        self.chess_game = game.Game(self)
        self.mouse_pos = None
        self.previous_mouse_pos = []
        self.input = False

    def run(self):
        running = True

        const.start_sound.play()
        self.chess_game.left_click_up = [None,None,None,None,None]


        while running:
            self.mouse_pos = pg.mouse.get_pos()
            user_input = pg.key.get_pressed()

            if user_input[pg.K_a]:
                board.theme_index = (board.theme_index+1)%const.NMB_THEMES

            if user_input[pg.K_LEFT]:
                pass

            if user_input[pg.K_RIGHT]:
                pass

            if user_input[pg.K_DOWN]:
                pass

            if user_input[pg.K_UP]:
                pass

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False


                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.chess_game.left_click_down = mk.mouse_to_coor(self.mouse_pos)
                    self.input = True


                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.chess_game.left_click_down = 0
                    self.chess_game.left_click_up = mk.mouse_to_coor(self.mouse_pos)
                    self.input = True


            if isinstance(self.chess_game.players[self.chess_game.player_turn], pb.Player):
                if self.input:
                    self.chess_game.input_to_candidate_move()

                if not self.chess_game.list_legal_moves:
                    self.chess_game.get_all_legal_moves(self.chess_game.player_turn)

                if self.chess_game.candidate_move[1]:
                    self.chess_game.players[self.chess_game.player_turn].move(self)
                    self.chess_game.update_position()

            else:
                self.chess_game.players[self.chess_game.player_turn].return_move()



            self.win.fill((50, 50, 50))
            board.draw_board(self)
            board.draw_coor(self)
            board.draw_pieces(self)
            board.blit_legal_moves(self)
            board.draw_selected_piece(self)
            board.write_player_turn(self)

            pg.display.update()

            self.input = False
            self.previous_mouse_pos.append(self.mouse_pos[0])

            if len(self.previous_mouse_pos) > 5: del self.previous_mouse_pos[0]

        #menu.main_menu(gestionary)





if __name__ == "__main__":
    gestionary = Gestionary()
    menu.main_menu(gestionary)
