import pygame
from config import *
import math
import random
from health_sys import *
from explosion import *
import sys


class SpriteSheet:
    # This is the SpriteSheet call. Think of it as the
    # Sprite getter and converter. It does the general
    # Pygame surface which we need so that we can blit(draw) our sprites(imgs) on the screen
    # The color key makes the edge of the sprite transparant
    def __init__(self, file):
        # Load sprite sheet image and convert it to include transparency (alpha channel)
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        # Create new surface to hold the sprite, with the given width & height
        sprite = pygame.Surface((width, height)).convert_alpha()
        # Copy the specified area from the sprite sheet onto the new surface.
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        # Set color key to make black transparent.
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    # This class represents the player character
    # Handles all player functionality.
    def __init__(self, game, x, y, max_hp=100):
        # Ensures Player object is properly initialzed as a sprite, inheriting essential functionality.
        super().__init__()
        # Store a reference to the game instance and set the layer for rendering.
        self.game = game
        self.layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Initialize the player's position in pixels based on the tile size.
        # Tile size is set to 32 pixels in the config so that we can keep everything simple
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        # Set player's width & height, matching sprite's unique dimensions
        self.width = 30
        self.height = 50
        # Variables to track the player's movement along the x and y axes.
        self.x_change = 0
        self.y_change = 0
        # The player is idle standing facing down
        self.facing = 'down'
        # Starting index for our animation loop
        self.animation_lopp = 1
        self.max_hp = max_hp
        self.hp = max_hp
        self.health_bar = HealthBar(900, 15, 250, 40, 100)
        self.damage_cooldown = 0
        self.damage_cooldown_max = 60





        # Load initial sprite for the player from the sprite sheet
        # 9 and 16 being the top left pixels that the sprite sheet starts at in the
        # Photoshop or gimp photo viewer
        self.image = self.game.character_spritesheet.get_sprite(9, 16, self.width, self.height)
        # Create Rectangle Around Sprite for Positioning and Collision Detection
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # These are the spritesheet imgs. There literlly just in a list and we get the different pictures
        # By top left pixel spot in the spritesheet picture and loop through it to animate movement

        # Load animations for the player walking different directions(down, up, left, right)
        self.down_animations = [self.game.character_spritesheet.get_sprite(57, 144, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(10, 144, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(105, 144, self.width, self.height)]
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
    # This function handles switching the player's sprite to create an animation effect.
        if self.facing == 'down':
            if self.y_change == 0:
                # If player is not moving, display idle sprite for facing down
                self.image = self.game.character_spritesheet.get_sprite(57, 144, self.width, self.height)
            else:
                # If player is moving, cycle through the walking animation frames
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
        # This function is called every frame to update the player's position and handle animations.
        self.movement()
        self.animate()
        self.collide_enemy()



        # Update player's position based on movement.
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        # Reset movement changes for the next frame.
        self.x_change = 0
        self.y_change = 0
        # This is what movement looks like lol
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change = -PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change = PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_change = -PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_change = PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        # Without a health system implemented anytime you make contact with a enemy sprite
        # it Kills the player
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        if hits and self.damage_cooldown <= 0:
            self.hp -= 50
            self.health_bar.update(self.hp)
            if self.hp <= 0:
                self.game.playing = False
            self.damage_cooldown = self.damage_cooldown_max
        elif self.damage_cooldown > 0:
            self.damage_cooldown -= 1
            print(self.hp)


    def collide_blocks(self, direction):
        # This function handles collision between the player and blocks (e.g., walls)
        # This controls the camera and keeps the player in bounds
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:  # Moving right; hit something
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:  # Moving left; hit something
                    self.rect.left = hits[0].rect.right

        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:  # Moving down; hit something
                    self.rect.bottom = hits[0].rect.top
                if self.y_change < 0:  # Moving up; hit something
                    self.rect.top = hits[0].rect.bottom

    def take_damage(self, damage):
        self.hp -= damage
        print(f"Player HP: {self.hp}")
        if self.hp <= 0:
            self.game.playing = False



class enemy(pygame.sprite.Sprite):
    # Represents pigs, which move autonomously
    def __init__(self, game, x, y, max_hp = 100):
        super().__init__()
        self.game = game
        # Piggies exist on the enemy layer also in config
        self.layer = ENEMYLAYER
        # Add the enemy to the game's sprite groups
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Set enemy's initial position on the grid
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        # Again we have to set the width and height of our sprite
        # Because of the sprite sheet's specific size we have to set the width and height of our sprite manually
        # 23 and 30 are the pixels we need from the sprite sheet to make our piggy
        self.width = 23
        self.height = 30

        # Variables to track movement changes
        self.x_change = 0
        self.y_change = 0
        # Enemy Ai is very simple atm so all the pigs do is run right and left
        # With their animation loops following the same
        # Their loop is random so they dont all walk the same way but it does have a max distance
        self.facing = random.choice(["left", "right"])
        self.animation_loop = 1 # Start animation loop
        self.movement_loop = 0 # Track movement distance
        self.max_travel = random.randint(20, 30) # Random max distance to travel before changing direction

        # Initial image taken from the sprite sheet
        self.image = self.game.pig_rich_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image.set_colorkey(BLACK) # Set transparency color to black

        # Set the rectangle area for collision detection and positioning
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.max_hp = max_hp
        self.hp = max_hp

        self.last_bomb_time = pygame.time.get_ticks()
        self.bomb_cooldown = 1000
# Same as with player animations we manually go in and find the top left pixel location for each image
# and put them in a list so we can loop through it and simualate moving

        # Load animations for left and right movements by extracting sprites from the sprite sheet
        self.left_animations = [self.game.pig_rich_spritesheet.get_sprite(68, 128, self.width, self.height),
                           self.game.pig_rich_spritesheet.get_sprite(36, 130, self.width, self.height),
                           self.game.pig_rich_spritesheet.get_sprite(4, 128, self.width, self.height),
                           self.game.pig_rich_spritesheet.get_sprite(100, 130, self.width, self.height),]

        self.right_animations = [self.game.pig_rich_spritesheet.get_sprite(70, 96, self.width, self.height),
                            self.game.pig_rich_spritesheet.get_sprite(102, 98, self.width, self.height),
                            self.game.pig_rich_spritesheet.get_sprite(6, 96, self.width, self.height),
                            self.game.pig_rich_spritesheet.get_sprite(38, 98, self.width, self.height)]

    def spawn_bomb(self):
        now = pygame.time.get_ticks()
        if now - self.last_bomb_time > self.bomb_cooldown:
            bomb = Bomb(self.game, self.rect.x, self.rect.y)
            self.game.bombs.add(bomb)
            self.last_bomb_time = now



    def update(self):
        # Update the enemy's movement and animation on each game loop iteration
        self.movement()
        self.animate()
        # Apply changes in position
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        # Reset movement changes to prepare for the next update
        self.x_change = 0
        self.y_change = 0


    # Enemys move automatically But we decide what they do based of the direction
    # From the random gen up there how fast and whether they go left or right
    # Again simple implmentation for now but we could add there y-axis for sure
    def movement(self):
        # Controls enemy movement based on its current facing direction
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED # Move left
            self.movement_loop -= 1 # Update movement loop counter
            if self.movement_loop <= -self.max_travel: # Change direction if max travel is reached
                self.facing = 'right'
        if self.facing == 'right':
            self.x_change += ENEMY_SPEED # Move right
            self.movement_loop += 1 # Update movement loop counter
            if self.movement_loop >= self.max_travel: # Change direction if max travel is reached
                self.facing = 'left'

    def take_damage(self, damage):
        # Reduce the enemy's health by the specified damage amount
        self.hp -= damage
        print(self.hp)
        # If the enemy's health reaches zero or below, remove it from the game
        if self.hp <= 0:
            self.kill()
    def animate(self):
    # Pig's animation loop through the list we set
    # Update enemy's sprite based on its facing direction & movement
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



class Block(pygame.sprite.Sprite):
    # THis is the block layer so like the rocks we see and cant walk through.
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BLOCK_LAYER # Define rendering layer for the block
        self.groups = self.game.all_sprites, self.game.blocks # Add block to sprite groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        # As sprites they get initalized like player and enemy but since they're static
        # objects we just leave them be or put them in the way

        # Set block position & dimensions
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
        self.layer = GROUND_LAYER # Set the rendering layer for ground tiles
        self.groups = self.game.all_sprites # Add ground tile to sprite groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        # Set ground tile position & dimensions
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
    # Hay ('G'): We loop for on create_tile_map()
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = BLOCK_LAYER # Set rendering layer for haystack
        self.groups = self.game.all_sprites # Add haystack to sprite groups
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Set haystack position and dimensions
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = 95 # Haystack-specific dimensions
        self.height = 79
#HAAAYYY
        # Get haystack's image from terrain sprite sheet
        self.image = self.game.terrain_spritesheet.get_sprite(480, 271, self.width, self.height)
        # Set rectangle area for collision detection and positioning
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Brickhouse(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Set position and dimensions
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE

        self.scaled_width = 150
        self.scaled_height = 150

        # Get house's image from sprite sheet
        self.image = self.game.brick_house_image
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))

        # Set rectangle area for collision detection and positioning
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Strawhouse(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Set position and dimensions
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE


        self.scaled_width = 150
        self.scaled_height = 150

        # Get house's image from sprite sheet
        self.image = self.game.straw_house_image
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))

        # Set rectangle area for collision detection and positioning
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Stickhouse(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Set position and dimensions
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE


        self.scaled_width = 150
        self.scaled_height = 150

        # Get house's image from sprite sheet
        self.image = self.game.stick_house_image
        self.image = pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height))

        # Set rectangle area for collision detection and positioning
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    # Defines Button, which can be used in game's intro or other screens
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
       # Initialize Button with position, size, colors, content, and font size.
       self.font = pygame.font.Font('fonts/Cantarell-Bold.ttf', 64) # font for button text
       self.content = content # The text that will be displayed on the button.

       # Position and size of button
       self.x =x
       self.y = y
       self.width = width
       self.height = height
       # Foreground & background colors of the button
       self.fg = fg
       self.bg = bg
       # Create surface for the button with specified size and fill with background color
       self.image = pygame.Surface((self.width, self.height))
       self.image.fill(self.bg)
       # Create rectangle object to define the button's boundaries
       self.rect = self.image.get_rect()
       self.rect.x =self.x # x-coordinate of buttons rectangle
       self.rect.y = self.y # y-coordinate of buttons rectangle

       # Render button's text with specified font and foreground color
       self.text = self.font.render(self.content, True, self.fg)
       # Center the text within the button
       self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
       # Blit the text onto the button's surface
       self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        # Check if button is clicked based on the mouse position and button press state
        if self.rect.collidepoint(pos): # If mouse pos is within buttons rectangle
            if pressed[0]: # If left mouse button is pressed
                return True # The button is pressed
            return False # The button is not pressed, even if the mouse is over it.
        return False # The mouse is not over the button, so it can't be pressed.


class Attack(pygame.sprite.Sprite):

    # Now the Attack is alot like the player class except we spawn make it do stuff
    # Then get rid of it based on player postion
    def __init__(self, game, x, y, direction, speed=PLAYER_SPEED):
        super().__init__()
        # Reference to game instance to access game resources and state.
        self.game = game
        # Shares our layer because its our attack
        # Set layer for rendering the attack, used to control the draw order
        self.layer = PLAYER_LAYER
        # Add this attack to both the all_sprites and attacks groups for updating and drawing.
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Initial position and size of the attack
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.width = 40
        self.height = 56
        # Animation frame index for cycling through attack frames.
        self.animation_loop = 0
        # Load initial image for the attack from the attack spritesheet
        self.image = self.game.attack_spritesheet.get_sprite(5, 5, self.width,
            self.height)

        # Create a rectangle representing the attack's boundaries and set its position
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.damaging = False
        self.damage_timer = 0
        self.damage_interval = 60
        self.x_change = 0
        self.y_change = 0
        # Define animations for the attack in different directions
        # Each direction has multiple frames for creating the animation effect.
        # Yup it gets animations and all so that it simulates movement.
        self.right_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(53, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(148, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(197, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(245, 5, self.width, self.height)]

        self.down_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(53, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(148, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(197, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(245, 5, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(53, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(148, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(197, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(245, 5, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite(5, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(53, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(101, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(148, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(197, 5, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(245, 5, self.width, self.height)]

        # self.rotated_right_animations = [pygame.transform.rotate(sprite, -90) for sprite in self.right_animations]
        # self.rotated_down_animations = [pygame.transform.rotate(sprite, 180) for sprite in self.down_animations]
        # self.rotated_left_animations = [pygame.transform.rotate(sprite, 90) for sprite in self.left_animations]
        # self.rotated_up_animations = [pygame.transform.rotate(sprite, 0) for sprite in self.up_animations]
    def update(self):
        # Update the attack's state, including animation and collision detection
        self.animate()
        self.collide()

        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed


    def collide(self):
        # Check for collisions between the attack & enemies
        # If a collision occurs, remove the enemy form the game
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        if hits:
            hits[0].take_damage(4)
            print("\n hit")

    def animate(self):
        # Update attack's image based in the direction the player is facing
        # Animate the attack sprite and remove it after completing the animation
        direction = self.game.player.facing # Get current direction player is facing

        if direction == "up":
            # Update image to next frame in the upward animation sequence
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1 # Increment the animation frame index
            if self.animation_loop >= 5: # Check if the animation has completed
                self.kill() # Remove the attack from the game

        if direction == "down":
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 5:
                self.kill()

        if direction == "left":
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 5:
                self.kill()

        if direction == "right":
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 5:
                self.kill()
