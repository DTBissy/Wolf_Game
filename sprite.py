import pygame
from config import *
import math
import random

class SpriteSheet:
    # This is the SpriteSheet call think of it as the
    # Sprite getter and converter. It does the general
    #Pygame surface which we need so that we can blit(draw) our sprites(imgs) on the screen
    # And the color key makes the edge of the sprite transparant
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height)).convert_alpha()
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    # The player class Where all functions and player related actions are made and
    # Called
    def __init__(self, game, x, y):
        super().__init__()
      # We use super to pull in game, the Layer our sprite is on and
      # The 'Games' sprite classes , Player Layer is in the Config File
        self.game = game
        self.layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
#  Tile size is set to 32 pixels in the config so that we can keep everything simple
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
# self.width and height are manually set here because the sprites needed them to be
# Reset to their width size and height in pixels because of their unique image size
        self.width = 30
        self.height = 50

        self.x_change = 0
        self.y_change = 0
# The player is idle standing facing down
        self.facing = 'down'
# THis is so we have a starting index for our animation loop
        self.animation_lopp = 1

# Calld the get sprite sheet on the chrachter spritesheet in the main.py file
# 9 and 16 being the top left pixels that the sprite sheet starts at in the
# Photoshop or gimp photo viewer
        self.image = self.game.character_spritesheet.get_sprite(9, 16, self.width, self.height)
# Get rect is we can assign a rectangle to our player sprite so that we can
# Move it around and use it for collision detection
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
# These are the spritesheet imgs. There literlly just in a list and we get the different pictures
# By top left pixel spot in the spritesheet picture and loop through it to animate movement
        self.down_animations = [self.game.character_spritesheet.get_sprite(57, 144, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(10, 144, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(105, 144, self.width, self.height)]
#Legit just busy work at this point because you gotta do it for every direction
        self.up_animations = [self.game.character_spritesheet.get_sprite(9, 16, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(55, 14, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(106, 16, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(8, 208, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(56, 206, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(104, 208, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite(13, 80, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(62, 80, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(106, 80, self.width, self.height)]
# A function to assign the directional list to a direction pressed on keyboard input
    def animate(self):
# idle stance for the ifs, and if y isnt changing so not moving
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(57, 144, self.width, self.height)
            else:
# Non idle so walk animation
                self.image = self.down_animations[math.floor(self.animation_lopp)]
                self.animation_lopp += 0.1
                if self.animation_lopp >= 3:
                    self.animation_lopp = 1
# same for every direction
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(9, 14, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_lopp)]
                self.animation_lopp += 0.1
                if self.animation_lopp >= 3:
                    self.animation_lopp = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(8, 208, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_lopp)]
                self.animation_lopp += 0.1
                if self.animation_lopp >= 3:
                    self.animation_lopp = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(13, 80, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_lopp)]
                self.animation_lopp += 0.1
                if self.animation_lopp >= 3:
                    self.animation_lopp = 1


# All the functions you call in the update method because everything is changing at 60 frames per second
# Again to simulate movement, But you do check for collisons every frame too so ya know.
    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')


        self.x_change = 0
        self.y_change = 0
# This is what movement looks like lol
    def movement(self):
        # call so that we can take input
        keys = pygame.key.get_pressed()
        # Left is negative on a x or horizontal axis therefor we subtract the postion of our character
        #  on a x-xis to again mimic movement
        #Player_speed is in config.py its just the rate at which our player increments or decrements
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
          # Same for right but that increases on a x-axis so we add to the postion of our character or x.change
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
            #because pygame starts its y axis at 0 we subbtract from it to go up anytime
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
          # and since we subtract to go up on the y-axis its only logical we add to go down.
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        # Without a health system implemented anytime you make contact with a enemy sprite
        # it Kills the player
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        # This controls the camara and keeps the player in bounds
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED
                    self.rect.x = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED
                    self.rect.y = hits[0].rect.bottom

class enemy(pygame.sprite.Sprite):
    # Alot simpler than the player class and this holds all functions and calls
    # For our little piggies
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        # Piggies exist on the enemy layer also in config
        self.layer = ENEMYLAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        # Again we have to set the width and height of our sprite
        # Because of the sprite sheet's specific size we have to set the width and height of our sprite manually
        # 23 and 30 are the pixels we need from the sprite sheet to make our piggy
        self.width = 23
        self.height = 30

        self.x_change = 0
        self.y_change = 0
# Enemy Ai is very simple atm so all the pigs do is run right and left
# With their animation loops following the same
# Their loop is random so they dont all walk the same way but it does have a max distance
        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.pig_rich_spritesheet.get_sprite(0, 0, self.width, self.height)



        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
# Same as with player animations we manually go in and find the top left pixel location for each image
# and put them in a list so we can loop through it and simualate moving

        self.left_animations = [self.game.pig_rich_spritesheet.get_sprite(68, 128, self.width, self.height),
                           self.game.pig_rich_spritesheet.get_sprite(36, 130, self.width, self.height),
                           self.game.pig_rich_spritesheet.get_sprite(4, 128, self.width, self.height),
                           self.game.pig_rich_spritesheet.get_sprite(100, 130, self.width, self.height),]

        self.right_animations = [self.game.pig_rich_spritesheet.get_sprite(70, 96, self.width, self.height),
                            self.game.pig_rich_spritesheet.get_sprite(102, 98, self.width, self.height),
                            self.game.pig_rich_spritesheet.get_sprite(6, 96, self.width, self.height),
                            self.game.pig_rich_spritesheet.get_sprite(38, 98, self.width, self.height)]

    def update(self):
        self.movement()
        self.animate()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    # Enemys move automatically But we decide what they do based of the direction
    # From the random gen up there how fast and whether they go left or right
    # Again simple implmentation for now but we could add there y-axis for sure
    def movement(self):
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

    def animate(self):
# Their animation loop through the list we set

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.pig_rich_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.pig_rich_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
class Explosion(pygame.sprite.Sprite):
    # Unfinished but for the bomb the pigs are gonna throw
    def Explom(bomb=""):
      pass


class Block(pygame.sprite.Sprite):
    # THis is the block layer so like the rocks we see and cant walk through.
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
# As sprites they get initalized like player and enemy but since their static
#Objects we just leave them be or put them in the way
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    #This is Grass and its the 'j' we loop for on create_tile_map()
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
#Grassss
        self.image = self.game.terrain_spritesheet.get_sprite(67, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground2(pygame.sprite.Sprite):
    #This is ALT Grass so when we call whatever this is set to on the
    #Create Tile map this will show up
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = DECOR_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE
#Alt grass

        self.image = self.game.terrain_spritesheet.get_sprite(252, 352, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Hay(pygame.sprite.Sprite):
    # Prints when G is ran into on create TileMap
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = 95
        self.height = 79
#HAAAYYY
        self.image = self.game.terrain_spritesheet.get_sprite(480, 271, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Button:
    #This for our intro im pretty sure but i could be mistaken, Either way
    #Its exaclty as said a button
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
       self.font = pygame.font.Font('fonts/Cantarell-Bold.ttf', 64)
       self.content = content

       self.x =x
       self.y = y
       self.width = width
       self.height = height

       self.fg = fg
       self.bg = bg

       self.image = pygame.Surface((self.width, self.height))
       self.image.fill(self.bg)
       self.rect = self.image.get_rect()

       self.rect.x =self.x
       self.rect.y = self.y

       self.text = self.font.render(self.content, True, self.fg)
       self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
       self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False


class Attack(pygame.sprite.Sprite):
    # Now the Attack is alot like the player class except we spawn make it do stuff
    # Then get rid of it based on player postion
    def __init__(self, game, x, y):
        super().__init__()

        self.game = game
        # Shares our layer because its our attack
        self.layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width,
            self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # Yup it gets animations and all so that it simulates movement.
        self.right_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width + TILE_SIZE * 0.5, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(54, 5, self.width + TILE_SIZE * 0.5, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width + TILE_SIZE * 0.5, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(147, 5, self.width + TILE_SIZE * 0.5, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(195, 5, self.width + TILE_SIZE * 0.5, self.height * 2)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(54, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(147, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(195, 5, self.width, self.height * 2)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(54, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(147, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(195, 5, self.width, self.height * 2)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(54, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(147, 5, self.width, self.height * 2),
                           self.game.attack_spritesheet.get_sprite(195, 5, self.width, self.height * 2)]

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        # we call it to the direction the player is facing so that we can save some
        # Coding but it still works the same way when it comes to stating its loop
        # Direction
        direction = self.game.player.facing

        if direction == "up":
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
