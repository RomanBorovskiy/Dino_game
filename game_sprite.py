from enum import Enum

import pygame
from pygame.sprite import Sprite

from game import GameState
from images import images_list
import constants
from constants import GRAVITY, JUMP_SPEED, DUCK_TIME


class DinoState(Enum):
    Waiting = 1
    Running = 2
    Jumping = 3
    Ducking = 4
    Crashed = 5


class ObstacleType(Enum):
    CACTUS_SMALL = 1
    CACTUS_LARGE = 2


class ObstacleWidth(Enum):
    SMALL = 1
    MIDDLE = 2
    BIG = 3


class GameSprite(Sprite):
    world_x: int = 0
    world_y: int = 0
    speed: int = 0
    instances = {}

    def __init__(self, x, y):
        super().__init__()
        self.world_x = x
        self.world_y = y
        self.image: pygame.Surface | None = None
        self.init_image()
        self.rect = self.image.get_rect()

        name = type(self).__name__
        # print(f'new {name}')
        if name in self.instances:
            self.instances[name].append(self)
        else:
            self.instances[name] = [self]

    def kill(self) -> None:
        self.instances[type(self).__name__].remove(self)
        # print(f'kill {type(self).__name__}')
        super().kill()

    def init_image(self):
        """Переопределяем для своего изображения"""
        self.image = pygame.Surface((10, 10))
        self.image.fill(constants.GREEN)

    def update(self, game_state: GameState, time_frame: int):
        self.update_position(game_state, time_frame)
        self.update_animation(game_state)

    def update_animation(self, game_state: GameState):
        """Вызывается перед каждым обновлением"""
        pass

    def update_position(self, game_state: GameState, time_frame):
        if game_state == GameState.Play:
            self.world_x -= self.speed * time_frame / 1000

    def check_kill(self):
        # kill sprite if its right corner is out of screen now
        if self.rect.right < 0:
            self.kill()


class Cloud(GameSprite):
    speed = -400

    def init_image(self):
        self.image = images_list['CLOUD_CLOUD_1']


class Horizon(GameSprite):
    def init_image(self):
        self.image = images_list['HORIZON_1']
        self.world_y -= self.image.get_rect().height // 2


class Pterodactyl(GameSprite):
    ODO_PER_ANIM = 3

    def __init__(self, x, y):
        self.fly_images = [images_list['PTERODACTYL_FLY_1'], images_list['PTERODACTYL_FLY_2']]
        self.speed = -20
        super().__init__(x, y)

    def init_image(self):
        self.image = self.fly_images[0]

    def update_animation(self, game_state: GameState):
        if game_state == GameState.Play:
            anim = int(self.world_x // self.ODO_PER_ANIM) % len(self.fly_images)
            self.image = self.fly_images[anim]


class Obstacle(GameSprite):
    _layer = 0

    def __init__(self, x, obstacle_type: ObstacleType, obstacle_width: ObstacleWidth):
        self.obstacle_type = obstacle_type
        self.obstacle_width = obstacle_width
        super().__init__(x, 0)

    def init_image(self):
        key = f'{self.obstacle_type.name}_{self.obstacle_width.name}'
        self.image = images_list[key]


class Dino(GameSprite):
    _layer = 1

    def __init__(self):
        self.sound_jump = pygame.mixer.Sound(constants.SOUND_PRESS)
        self.run_image = [images_list['TREX_RUNNING_1'], images_list['TREX_RUNNING_2']]
        self.wait_image = [images_list['TREX_WAITING_1'], images_list['TREX_WAITING_2']]
        self.duck_image = [images_list['TREX_DUCK_1'], images_list['TREX_DUCK_2']]
        self.crash_image = [images_list['TREX_CRASHED']]
        self.jump_image = [images_list['TREX_JUMPING']]
        self.state = DinoState.Waiting
        self.speed = 6 * 60 + 100
        # self.speed = 6
        self.max_speed = 1000
        self.acceleration = 6
        self.jump_speed = 0
        self._duck_timer = 0

        super().__init__(0, 0)

    def update_position(self, game_state: GameState, time_frame: int):
        if self.state not in [DinoState.Waiting, DinoState.Crashed] and game_state == GameState.Play:
            self.world_x += self.speed * time_frame / 1000
            self.speed += self.acceleration * time_frame / 1000
            self.speed = min(self.max_speed, self.speed)

        if self.state == DinoState.Jumping:
            dy = int(self.jump_speed * time_frame / 1000)
            self.jump_speed -= GRAVITY * time_frame / 1000
            self.world_y += dy

            if self.world_y <= 0:
                self.world_y = 0
                self.jump_speed = 0
                self.state = DinoState.Running

    def update_animation(self, game_state: GameState):
        if self.state == DinoState.Waiting:
            anim = (pygame.time.get_ticks() // 400) % len(self.wait_image)
            self.image = self.wait_image[anim]

        elif self.state == DinoState.Crashed:
            self.image = self.crash_image[0]

        elif self.state == DinoState.Jumping:
            self.image = self.jump_image[0]

        elif self.state == DinoState.Running:
            self.image = self.run_image[int(self.world_x / 40) % len(self.run_image)]

        elif self.state == DinoState.Ducking:
            self.image = self.duck_image[int(self.world_x / 30) % len(self.duck_image)]
            if self._duck_timer < pygame.time.get_ticks():
                self.state = DinoState.Running

        self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)

    def init_image(self):
        self.image = self.wait_image[0]

    def jump(self):
        if self.state in [DinoState.Jumping, DinoState.Crashed]:
            return

        self.sound_jump.play()

        self.state = DinoState.Jumping
        self.jump_speed = JUMP_SPEED

    def duck(self):
        if self.state in [DinoState.Jumping, DinoState.Crashed]:
            return

        self.state = DinoState.Ducking
        self._duck_timer = pygame.time.get_ticks() + DUCK_TIME * 1000
