"""
Script qui joue les sons nécessaires.
"""

import const

def play_sound(gestionary):
    sound = gestionary.chess_game.sound_to_play

    if sound == 5: const.end_sound.play()
    elif sound == 4: const.check_sound.play()
    elif sound == 3: const.promote_sound.play()
    elif sound == 2: const.castle_sound.play()
    elif sound == 1: const.capture_sound.play()
    else: const.move_sound.play()