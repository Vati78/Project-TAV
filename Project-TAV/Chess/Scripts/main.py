"""
Tour de contrôle de tous les scripts.
"""

import pygame as pg
import random
import os
import time
import const
import board
import pieces
import game
import mouse_keys as mk

os.chdir(os.path.dirname(__file__))
pg.init()
win = pg.display.set_mode((const.WIDTH + 5*const.SQUARE, const.HEIGHT))
pg.display.set_caption("Chess")
win.fill((50, 50, 50))
chess_game = game.Game()

def main():
    running = True

    while running:

        mouse_pos = pg.mouse.get_pos()
        user_input = pg.key.get_pressed()

        game.left_click_up = None
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

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

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                chess_game.left_click_up = None
                coor =  mk.mouse_to_coor(mouse_pos)
                if coor and (chess_game.candidate_move[0] is not None or board.color_and_occupied_square(coor[0], coor[1])):
                    chess_game.left_click_down = coor


            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                coor = mk.mouse_to_coor(mouse_pos)
                if coor and chess_game.left_click_down is not None:
                    chess_game.left_click_up = coor

        if chess_game.human:
            chess_game.input_to_candidate_move()
            if all(item is not None for item in chess_game.candidate_move):
                pass
                # if in legal_moves
                    # play_move
                    # if check
                        # put back old position
            pass

        else:
            pass
            # fonctions androïde


        #chess_game.make_move()


        win.fill((50, 50, 50))
        board.draw_board()
        board.draw_pieces()
        board.write_player_turn()

        pg.display.update()



if __name__ == "__main__":
    main()
