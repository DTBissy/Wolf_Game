import pygame
from config import *
import math

class Bomb(pygame.sprite.Sprite):
    # Bomb ('X'): Loop on create_tile_map
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = PLAYER_LAYER
        self.x, self.y = x, y
        self.width = 40
        self.height = 30
        # Load the image representing the bomb and set its initial position
        self.images = []
        for num in range(1, 4):
            img = pygame.image.load(f'sprites/pigs/bomb{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (40, 30))
            self.images.append(img)
        for num in range(1,6):
            img = pygame.image.load(f'sprites/pigs/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (40, 30))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.animation_speed = 20 # Adjust speed as necessary
        self.current_frame = 0
        self.active = True # Flag to indicate if the bomb is active
        self.triggered = False # Flag to indicate is bomb has triggered an explosion
        self.timer = 1000
        self.start_ticks = pygame.time.get_ticks()

    def update(self):
        # Animate bomb by cycling through images
        self.current_frame += 1
        if self.current_frame >= self.animation_speed:
            self.current_frame = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            if self.index == 120:
                self.kill()
