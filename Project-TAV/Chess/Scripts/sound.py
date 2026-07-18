"""
Script qui joue les sons nécessaires.
"""

import const

def play_sound(gestionary):
    sounds = gestionary.chess_game.sound_to_play

    if "end" in sounds: const.end_sound.play()
    elif "check" in sounds: const.check_sound.play()
    elif "promotion" in sounds: const.promote_sound.play()
    elif "castle" in sounds: const.castle_sound.play()
    elif "capture" in sounds: const.capture_sound.play()
    else: const.move_sound.play()