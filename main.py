import pygame
from sprite import *
from config import *
from explosion import Bomb
from health_sys import HealthBar
import sys


class Game:
    def __init__(self):
        pygame.init()
        # Set up display window with given width & height
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Down With The House")
        # Creates clock object to manage frames per second
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        # Set the game loop control variable
        self.running = True
        self.font = pygame.font.Font('fonts/Cantarell-Bold.ttf', 64) # loads the font for rendering text

        # Load all necessary spritesheets and images
        self.character_spritesheet = SpriteSheet('sprites/player/werewolf-NESW.png')
        self.terrain_spritesheet = SpriteSheet('sprites/enviroment/terrain.png')
        self.pig_red_spritesheet = SpriteSheet('sprites/pigs/pendleton_pig_red.png')
        self.pig_brown_spritesheet = SpriteSheet('sprites/pigs/pendleton_pig_brown.png')
        self.pig_rich_spritesheet = SpriteSheet('sprites/pigs/pendleton_pig_Rich.png')
        self.attack_spritesheet = SpriteSheet('sprites/player/tornado.png')
        self.intro_background = pygame.image.load('sprites/introbackground.png')
        self.go_background = pygame.image.load('sprites/gameover.png')
        self.brick_house_image = pygame.image.load('houses/brickhouse.png').convert_alpha()
        self.straw_house_image = pygame.image.load('houses/strawhouse.png').convert_alpha()
        self.stick_house_image = pygame.image.load('houses/stickhouse.png').convert_alpha()


        # Load bomb and explosion sprites
        self.bomb_images = [pygame.image.load(f'sprites/pigs/bomb{num}.png') for num in range(1, 4)]
        self.explosion_images = [pygame.image.load(f'sprites/pigs/exp{num}.png') for num in range(1, 6)]


    def new(self):
        # New Game Starts
        self.playing = True # Set the playing state to true
        # Updates all things below at once with LayeredUpdates
        # Create sprite groups to manage different entities
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.bombs = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_Tile_map() # Generate the game world based on the tile map

    def create_Tile_map(self):
        # Create game world based on TILEMAP layout
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                Ground(self, j, i,)
                if column == "B":
                    Block(self, j, i,)
                if column == "E":
                    enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "f":
                    Ground2(self, j, i,)
                if column == "g":
                    Hay(self, j, i)
                if column == "X":
                    bomb = Bomb(self, j * TILE_SIZE, i * TILE_SIZE)
                    self.bombs.add(bomb)
                    self.all_sprites.add(bomb) # add bomb to all_sprites group for general updates
                if column == "H":
                    Brickhouse(self, j, i)
                if column == "S":
                    Strawhouse(self, j, i)
                if column == "W":
                    Stickhouse(self, j, i)


    def events(self):
        # Handle all events during the game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False # Exit the game loop
                self.running = False # Stop the game entirely

            if event.type == pygame.KEYDOWN:
                # Handle player attack based on the direction they're facing
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y - TILE_SIZE, "up")
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TILE_SIZE,'down')
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TILE_SIZE, self.player.rect.y, 'left')
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TILE_SIZE, self.player.rect.y, 'right')

    def update(self):
        # Update all sprites in the game
        self.all_sprites.update()
        self.bombs.update()

    def draw(self):
        # Render all elements on screen
        self.screen.fill(BLACK) # Clear screen by filling it with black color
        self.all_sprites.draw(self.screen) # Draw all sprites onto screen
        self.player.health_bar.draw(self.screen)
        self.player.health_bar.update(self.player.hp)


        # Draw bombs if they are in a separate group
        self.bombs.draw(self.screen)

        # Cap the frame rate and update display
        self.clock.tick(FPS) # Cap the frame rate
        pygame.display.flip() # Update the full display surface to the screen

    def main(self):
        # Main Game Loop
        while self.playing:
            self.events() # Process events
            self.update() # Update game state
            self.draw() # Draw everything on the screen


    def game_over(self):
        # Handle the game over state (player dies)
        text = self.font.render("Game Over", True, WHITE) # Render "Game Over" text
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2)) # Center the text on the screen

        restart_button = Button(WIN_WIDTH/2 - 100, WIN_HEIGHT/2 + 60, 250, 50, WHITE, BLACK, 'Restart', 32) # Creates restart button

        for sprite in self.all_sprites:
            sprite.kill() # Remove all sprites from the game

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False # Exit the game

            mouse_pos = pygame.mouse.get_pos() # Get current mouse position
            mouse_pressed = pygame.mouse.get_pressed() # Check if mouse is pressed

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new() # Start a new game
                self.main() # Run the main game loop

            # Draw the game over screen elements
            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS) # Cap the frame rate
            pygame.display.update() # Updates the display

    def intro_screen(self):
        # Display intro screen
        intro = True # Control variable for the intro screen

        # Render the game title
        title = self.font.render('Down With The House', True, BLACK)
        title_rect = title.get_rect(x=10, y=10) # Position title to top left

        # Play Button
        play_button = Button((WIN_WIDTH/2) - 125, (WIN_HEIGHT/2 - 50), 150, 75, WHITE, BLACK, 'Play', 64)
        how_to_button = Button((WIN_WIDTH/2) - 125, (WIN_HEIGHT/2 + 75), 420, 75, WHITE, BLACK, 'How to Play', 64)

        # loop to check if you quit while in the title screen
        while intro:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    intro = False # Exit the intro screen
                    self.running = False # Stop the game

            # Gets the mouse position and checks if the mouse is pressed
            # which is an array
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            #checks if the play button is pressed and if it is pressed sets the
            #intro variable to false
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False  #Start Game if play button is pressed
            elif how_to_button.is_pressed(mouse_pos, mouse_pressed):
                self.how_to_screen()

            # Draws everything like normal and updates the screen
            # at 60 fps
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(how_to_button.image, how_to_button.rect)
            self.clock.tick(FPS) # Cap the frame rate
            pygame.display.update() # Update the display
            # When this screen is broken out of it moves on to
            # the next line in the interpreter.

    def how_to_screen(self):
        """Displays the How to Play screen with instructions."""
        how_to_play = True
        instructions = [
            "Use arrow keys to move the player.", " ",
            "Press SPACE to attack.", " ",
            "Avoid enemies and obstacles.", " ",
            "Collect items to score points."
        ]

        while how_to_play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    how_to_play = False
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    how_to_play = False  # Pressing ESC exits how to play screen

            self.screen.blit(self.intro_background, (0, 0))
            y_offset = 100
            for line in instructions:
                text = self.font.render(line, True, WHITE)
                text_rect = text.get_rect(center=(WIN_WIDTH / 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 50

            back_text = self.font.render("Press ESC to return", True, WHITE)
            back_rect = back_text.get_rect(center=(WIN_WIDTH / 2, y_offset + 50))
            self.screen.blit(back_text, back_rect)

            self.clock.tick(FPS)
            pygame.display.update()

g = Game() # Create Game object
g.intro_screen() # Show the intro screen
g.new() # Start a new game
while(g.running):
    g.main() # Run the main game loop
    g.game_over() # Handle the game over state

pygame.quit() # Quit pygame
sys.exit() # Exit the program
