import pygame

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

IMAGES_DIR = './data/images/'
SPRITE_SRC = IMAGES_DIR + 'sprites.png'

SOUNDS_DIR = './data/sounds/'
SOUND_PRESS = SOUNDS_DIR + 'button-press.mp3'
SOUND_HIT = SOUNDS_DIR + 'hit.mp3'
SOUND_SCORE = SOUNDS_DIR + 'score-reached.mp3'

FPS = 100
WIDTH = 1366
HEIGHT = 768

KEYS_JUMP = [pygame.K_SPACE, pygame.K_UP]
KEYS_DUCK = [pygame.K_DOWN]

GROUND = 200  # высота земли от нижнего края экрана
GROUND_OFS = 20
START_X = 190  # смещение позиции дино от края экрана
JUMP_SPEED = 25 * 60 - 100  # скорость прыжка начальная
GRAVITY = 1 * 60 * 60  # гравитация
DUCK_TIME = 0.007  # задержка после "приседания" дино
