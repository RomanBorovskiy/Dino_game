"""Load images from data"""

import pygame

from constants import SPRITE_SRC, WHITE

SPRITE_POS = {
    'BACKGROUND_EL': {'x': 166, 'y': 2},
    'CACTUS_LARGE': {'x': 652, 'y': 2},
    'CACTUS_SMALL': {'x': 446, 'y': 2},
    'OBSTACLE_2': {'x': 652, 'y': 2},
    'OBSTACLE': {'x': 446, 'y': 2},
    'CLOUD': {'x': 166, 'y': 2},
    'HORIZON': {'x': 2, 'y': 104},
    'MOON': {'x': 954, 'y': 2},
    'PTERODACTYL': {'x': 260, 'y': 2},
    'RESTART': {'x': 2, 'y': 130},
    'TEXT_SPRITE': {'x': 1294, 'y': 2},
    'TREX': {'x': 1678, 'y': 2},
    'STAR': {'x': 1276, 'y': 2},
    'COLLECTABLE': {'x': 4, 'y': 4},
    'ALT_GAME_END': {'x': 242, 'y': 4},
}
TREX = {
    'WAITING_1': {'x': 44, 'w': 44, 'h': 47},
    'WAITING_2': {'x': 0, 'w': 44, 'h': 47},
    'RUNNING_1': {'x': 88, 'w': 44, 'h': 47},
    'RUNNING_2': {'x': 132, 'w': 44, 'h': 47},
    'DUCK_1': {'x': 264, 'w': 59, 'h': 29, 'y_ofs': 18},
    'DUCK_2': {'x': 323, 'w': 59, 'h': 29, 'y_ofs': 18},
    'JUMPING': {'x': 0, 'w': 44, 'h': 47},
    'CRASHED': {'x': 220, 'w': 44, 'h': 47},
}

PTER = {'FLY_1': {'x': 0, 'w': 46, 'h': 40}, 'FLY_2': {'x': 46, 'w': 46, 'h': 40}}
CLOUD = {'CLOUD_1': {'x': 0, 'w': 46, 'h': 14}}

CACTUS_SMALL = {
    'SMALL': {'x': 0, 'w': 17, 'h': 35},
    'MIDDLE': {'x': 17, 'w': 34, 'h': 35},
    'BIG': {'x': 51, 'w': 51, 'h': 35},
}

CACTUS_LARGE = {
    'SMALL': {'x': 0, 'w': 25, 'h': 50},
    'MIDDLE': {'x': 25, 'w': 50, 'h': 50},
    'BIG': {'x': 75, 'w': 75, 'h': 50},
}
HORIZON = {'1': {'x': 0, 'w': 1200, 'h': 10}}


def load_images():
    def load_sprites(
        sprite_rects: dict[str, dict[str, int]], img_key: str, src: pygame.Surface, dest: dict[str, pygame.Surface]
    ):
        for key, value in sprite_rects.items():
            y_ofs = value['y_ofs'] if 'y_ofs' in value else 0
            rect = pygame.Rect(
                (SPRITE_POS[img_key]['x'] + value['x'] * 2, SPRITE_POS[img_key]['y'] + y_ofs * 2),
                (value['w'] * 2, value['h'] * 2),
            )

            sprite = src.subsurface(rect)
            dest[f'{img_key}_{key}'] = sprite

    images_src = {}

    sheet = pygame.image.load(SPRITE_SRC)

    sheet.set_colorkey(WHITE)

    load_sprites(TREX, 'TREX', sheet, images_src)
    load_sprites(PTER, 'PTERODACTYL', sheet, images_src)
    load_sprites(CACTUS_SMALL, 'CACTUS_SMALL', sheet, images_src)
    load_sprites(CACTUS_LARGE, 'CACTUS_LARGE', sheet, images_src)
    load_sprites(CLOUD, 'CLOUD', sheet, images_src)
    load_sprites(HORIZON, 'HORIZON', sheet, images_src)

    return images_src


images_list = load_images()
