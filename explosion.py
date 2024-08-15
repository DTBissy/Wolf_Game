import pygame
from config import *
import math

class Bomb(pygame.sprite.Sprite):
    # Bomb ('X'): Loop on create_tile_map
    def __init__(self, game, x, y, facing='right'):
        super().__init__()
        self.game = game
        self.layer = ENEMYLAYER  # Placed in the enemy layer
        self.groups = self.game.all_sprites, self.game.bombs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.initial_y = y
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animation_loop = 0
        self.facing = facing

        # Initialize the bomb's image
        self.image = self.game.bomb_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Movement variables
        self.x_speed = 5 if self.facing == 'right' else -5  # Horizontal speed
        self.y_speed = -7  # Initial upward speed
        self.gravity = 0.5  # Gravity to bring the bomb down

        # Timing for the bomb explosion
        self.explosion_time = 2000  # milliseconds before detonation
        self.spawn_time = pygame.time.get_ticks()
        self.stopped = False

    def update(self):
        if not self.stopped:
            # Handle movement
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            self.y_speed += self.gravity  # Apply gravity to simulate the arc

            # Check if the bomb has returned to the initial x position
            if self.rect.y >= self.initial_y:
                self.x_speed = 0 # Stop horizontal movement
                self.y_speed = 0 # Stop vertical movement
                self.stopped = True  # Mark bomb as stopped

            # Check if it's time to detonate the bomb
            if pygame.time.get_ticks() - self.spawn_time > self.explosion_time:
                self.detonate()
            else:
                self.animate()
        else:
            self.detonate()

    def animate(self):
        # Animate the bomb itself before detonation
        if self.animation_loop < len(self.game.bomb_images):
            self.image = self.game.bomb_images[math.floor(self.animation_loop)]
            self.animation_loop += 0.05
        else:
            self.animation_loop = 0  # Loop the animation

    def detonate(self):
        # Switch to the explosion animation
        if self.animation_loop < len(self.game.explosion_images):
            self.image = self.game.explosion_images[math.floor(self.animation_loop)]
            self.animation_loop += 0.2
        else:
            self.kill()  # Remove the bomb after the explosion animation

        # Handle the explosion logic, targeting the player
        if pygame.sprite.collide_rect(self, self.game.player):
            self.game.player.take_damage(50)
# Apply damage to the player if within the blast radius


