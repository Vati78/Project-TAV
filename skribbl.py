"""
Script pour skribble.io
Utilisez Microsoft Edge avec un zoom à 67%.
Sauvegardez une image en tant que a.png puis appuyez sur espace pour lancer le jeu
"""


import pyautogui as pag
import cv2
import numpy as np
import keyboard
from collections import defaultdict

# ========== CONFIGURATION - AJUSTEZ ICI ==========
IMAGE_PATH = "a.png"
MAX = 120
h, w = img = cv2.imread(IMAGE_PATH).shape[:2]

if w > h:
    CANVAS_WIDTH = min(w, MAX)
    CANVAS_HEIGHT = int(h * (CANVAS_WIDTH/w))
else:
    CANVAS_HEIGHT = min(h, MAX)
    CANVAS_WIDTH = int(w * (CANVAS_HEIGHT/h))

PIXEL_SPACING = 2
BRUSH_SIZE = 5
DRAW_SPEED = 0
# ==================================================

pag.PAUSE = 0
pag.FAILSAFE = True

COLORS = {
    "white": [(255, 255, 255), (575, 875)],
    "gray": [(193, 193, 193), (600, 875)],
    "red": [(239, 19, 11), (625, 875)],
    "orange": [(255, 113, 0), (650, 875)],
    "yellow": [(255, 228, 0), (675, 875)],
    "green": [(0, 204, 0), (700, 875)],
    "turquoise": [(0, 255, 145), (725, 875)],
    "ciel": [(0, 178, 255), (750, 875)],
    "blue": [(35, 31, 211), (775, 875)],
    "violet": [(163, 0, 186), (800, 875)],
    "pink": [(223, 105, 167), (825, 875)],
    "beige": [(255, 172, 142), (850, 875)],
    "brown": [(160, 82, 45), (875, 875)],
    "black": [(0, 0, 0), (575, 900)],
    "d_gray": [(80, 80, 80), (600, 900)],
    "d_red": [(116, 11, 7), (625, 900)],
    "d_orange": [(194, 56, 0), (650, 900)],
    "d_yellow": [(232, 162, 0), (675, 900)],
    "d_green": [(0, 70, 25), (700, 900)],
    "d_turquoise": [(0, 120, 93), (725, 900)],
    "d_ciel": [(0, 86, 158), (750, 900)],
    "d_blue": [(14, 8, 101), (775, 900)],
    "d_violet": [(85, 0, 105), (800, 900)],
    "d_pink": [(135, 53, 84), (825, 900)],
    "d_beige": [(204, 119, 77), (850, 900)],
    "d_brown": [(99, 48, 13), (875, 900)]
}

# Position du sélecteur de taille de pinceau (si nécessaire)
BRUSH_POSITIONS = {
    1: (540, 875),  # Petit
    2: (540, 900),  # Moyen
    3: (540, 925),  # Gros
    4: (540, 950)  # Énorme
}


def load_and_process_image(path, width, height):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image non trouvée: {path}")
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def map_colors_vectorized(img, color_palette):
    h, w = img.shape[:2]
    pixels = img.reshape(-1, 3)[:, ::-1]  # BGR -> RGB

    color_names = list(color_palette.keys())
    color_values = np.array([color_palette[name][0] for name in color_names])

    # Calcul vectorisé des distances
    distances = np.linalg.norm(pixels[:, None, :] - color_values[None, :, :], axis=2)
    closest_indices = np.argmin(distances, axis=1)

    # Grouper les pixels par couleur
    color_groups = defaultdict(list)
    for idx, color_idx in enumerate(closest_indices):
        y, x = divmod(idx, w)
        color_name = color_names[color_idx]
        if color_name != "white":  # Ignorer le blanc
            color_groups[color_name].append((x, y))

    return color_groups


def sort_pixels_by_proximity(pixels):
    if len(pixels) <= 1:
        return pixels

    sorted_pixels = [pixels[0]]
    remaining = set(pixels[1:])

    while remaining:
        last = sorted_pixels[-1]
        closest = min(remaining, key=lambda p: (p[0] - last[0]) ** 2 + (p[1] - last[1]) ** 2)
        sorted_pixels.append(closest)
        remaining.remove(closest)

    return sorted_pixels


def draw_optimized(pos, color_groups, colors):
    pos_x, pos_y = pos
    current_color = None

    if BRUSH_SIZE in BRUSH_POSITIONS:
        pag.click(*BRUSH_POSITIONS[BRUSH_SIZE])

    total_pixels = sum(len(p) for p in color_groups.values())
    drawn = 0

    for color_name, pixels in color_groups.items():
        if not pixels:
            continue

        if current_color != color_name:
            pag.click(*colors[color_name][1])
            current_color = color_name

        pixels_sorted = sort_pixels_by_proximity(pixels)

        for x, y in pixels_sorted:
            screen_x = pos_x + x * PIXEL_SPACING
            screen_y = pos_y + y * PIXEL_SPACING
            pag.click(screen_x, screen_y)

            drawn += 1
            if drawn % 50 == 0:
                print(f"Progression: {drawn}/{total_pixels} pixels ({drawn * 100 // total_pixels}%)")


def main_mode():
    """Mode principal de dessin"""
    try:
        img = load_and_process_image(IMAGE_PATH, CANVAS_WIDTH, CANVAS_HEIGHT)
        color_groups = map_colors_vectorized(img, COLORS)

        def quick_draw(e):
            pos = pag.position()
            draw_optimized(pos, color_groups, COLORS)
            print("Dessin terminé!")

        keyboard.on_press_key("space", quick_draw)
        keyboard.wait("esc")
    except Exception as e:
        print(f"Erreur: {e}")

main_mode()