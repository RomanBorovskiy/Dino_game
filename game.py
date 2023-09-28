import random
from enum import Enum
import logging

import pygame

import constants


class GameState(Enum):
    Play = 1
    Stopped = 2
    Crashed = 3


from game_sprite import (  # noqa: E402
    Dino,
    Obstacle,
    Cloud,
    Pterodactyl,
    ObstacleWidth,
    ObstacleType,
    DinoState,
    Horizon,
)


class GameApp:
    def __init__(self):
        self.zero_x = constants.START_X
        self.zero_y = constants.GROUND
        self.fps = constants.FPS

        self.odometer = 0
        self.state = GameState.Stopped

        self.dino: Dino | None = None

        logging.info('init pygame')

        pygame.init()
        pygame.mixer.init()
        self.sound_hit = pygame.mixer.Sound(constants.SOUND_HIT)

        pygame.font.init()
        self.font = pygame.font.SysFont('Purisa', 30)

        pygame.key.set_repeat()
        pygame.display.set_caption('Dino')
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.obstacles = pygame.sprite.Group()
        self.init_game()

    def init_game(self):
        self.odometer = 0
        self.state = GameState.Stopped

        self.all_sprites.empty()
        self.obstacles.empty()

        self.dino = Dino()
        self.all_sprites.add(self.dino)

        self.all_sprites.add(Horizon(-constants.START_X, constants.GROUND_OFS))

        # self.img = images.images_list['HORIZON_1']

    def add_pterodactyl(self, altitude):
        pterodactyl = Pterodactyl(self.screen.get_width() + self.odometer - 100, altitude)
        self.obstacles.add(pterodactyl)
        self.all_sprites.add(pterodactyl)

    def add_obstacle(self, obstacle_type, obstacle_width):
        obstacle = Obstacle(self.screen.get_width() + self.odometer, obstacle_type, obstacle_width)

        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def draw_txt(self, x: int, y: int, text: str, color: tuple[int, int, int] = (0, 0, 0)):
        text_surface = self.font.render(text, False, color)
        self.screen.blit(text_surface, (x, y))

    def world_to_screen_position(self, x: int, y: int) -> tuple[int, int]:
        new_x = x - self.odometer + self.zero_x
        new_y = self.screen.get_height() - y - self.zero_y
        return int(new_x), int(new_y)

    def update(self, time_frame: int):
        self.all_sprites.update(self.state, time_frame)
        self.odometer = int(self.dino.world_x)

    def draw_info(self, fps):
        path = str(f'odo:{self.odometer // 100: 06d}')
        self.draw_txt(self.screen.get_width() - 300, 50, path)

    def on_key(self, event_key):
        if self.state == GameState.Stopped:
            self.state = GameState.Play
            self.dino.state = DinoState.Running

        elif self.state == GameState.Crashed:
            # restart game
            self.init_game()

        else:
            match event_key:
                case _ as key if key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False
                case _ as key if key in constants.KEYS_JUMP:
                    self.dino.jump()
                case pygame.K_p:
                    self.add_pterodactyl(100)
                case pygame.K_k:
                    self.add_obstacle(ObstacleType.CACTUS_LARGE, ObstacleWidth.BIG)

    def on_key_pressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.dino.duck()

    def draw_back(self):
        self.screen.fill(constants.WHITE)

        if Horizon.__name__ in Horizon.instances:
            last_horizon = Horizon.instances[Horizon.__name__][-1]
            last_x = last_horizon.rect.width + last_horizon.world_x
            if last_x - self.odometer < self.screen.get_width():
                self.all_sprites.add(Horizon(last_x, constants.GROUND_OFS))

    def draw_sprites(self):
        for sprite in self.all_sprites.sprites():
            sprite.rect.bottomleft = self.world_to_screen_position(sprite.world_x, sprite.world_y)
            sprite.check_kill()

        self.all_sprites.draw(self.screen)

    def check_collision(self):
        if self.state != GameState.Play:
            return

        collided_callback = pygame.sprite.collide_rect_ratio(0.7)
        is_collided: bool = pygame.sprite.spritecollide(self.dino, self.obstacles, False, collided_callback)
        if is_collided:
            self.sound_hit.play()
            self.state = GameState.Crashed
            self.dino.state = DinoState.Crashed

    def event_process(self):
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.on_key(event.key)

    def gen_clouds(self):
        MAX_CLOUDS = 5
        min_distance = 100

        if Cloud.__name__ in Cloud.instances:
            count = len(Cloud.instances[Cloud.__name__])
        else:
            count = 0

        if count == 0:
            self.all_sprites.add(Cloud(self.odometer + constants.WIDTH, 200))

        elif count < MAX_CLOUDS:
            last_cloud = Cloud.instances[Cloud.__name__][-1]

            last_x = last_cloud.world_x
            pos = last_x - self.odometer + min_distance
            if pos < constants.WIDTH:
                self.all_sprites.add(
                    Cloud(
                        self.odometer + constants.WIDTH + random.randint(0, 300),
                        random.randint(200, constants.HEIGHT - constants.GROUND - 200),
                    )
                )

    def gen_obstacles(self):
        last_x = 0
        min_distance = 800
        if len(self.obstacles.sprites()) >= 2:
            return

        for sprite in self.obstacles.sprites():
            last_x = max(last_x, sprite.world_x)

        pos = last_x - self.odometer + min_distance

        if pos < constants.WIDTH:
            if random.randint(1, 10) == 1:
                self.add_pterodactyl(random.choice([60, 150, 200]))
            else:
                self.add_obstacle(
                    random.choice([el for el in ObstacleType]), random.choice([el for el in ObstacleWidth])
                )

    def draw_game_over(self):
        text = 'GAME OVER'
        font = pygame.font.SysFont('Purisa', 80)
        text_surface = font.render(text, False, constants.RED)
        rect = text_surface.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2))
        self.screen.blit(text_surface, rect)

    def run(self):
        while self.running:
            frame_time = self.clock.tick(self.fps)
            fps = self.clock.get_fps()

            self.event_process()
            self.on_key_pressed()

            self.update(frame_time)
            self.gen_clouds()
            self.gen_obstacles()

            self.draw_back()
            self.draw_sprites()
            self.draw_info(fps)

            self.check_collision()
            if self.state == GameState.Crashed:
                self.draw_game_over()
            pygame.display.update()

    @staticmethod
    def close():
        pygame.quit()
