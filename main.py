import pygame
from sprite import *
from config import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        #Screen is measured in pixels
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        #this sets the frames
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True
        self.font = pygame.font.Font('fonts/Cantarell-Bold.ttf', 64)

        self.character_spritesheet = SpriteSheet('sprites/player/werewolf-NESW.png')
        self.terrain_spritesheet = SpriteSheet('sprites/enviroment/terrain.png')
        self.pig_red_spritesheet = SpriteSheet('sprites/pigs/pendleton_pig_red.png')
        self.pig_brown_spritesheet = SpriteSheet('sprites/pigs/pendleton_pig_brown.png')
        self.pig_rich_spritesheet = SpriteSheet('sprites/pigs/pendleton_pig_Rich.png')
        self.attack_spritesheet = SpriteSheet('sprites/player/attack.png')
        self.intro_background = pygame.image.load('sprites/introbackground.png')
        self.go_background = pygame.image.load('sprites/gameover.png')

    def new(self):
        # a new game starts
        self.playing = True
        #Updates all things below at once with LayeredUpdates
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_Tile_map()

    def create_Tile_map(self):
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "f":
                    Ground2(self, j, i)
                if column == "g":
                    Hay(self, j, i)



    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == "up":
                        Attack(self, self.player.rect.x, self.player.rect.y - TILE_SIZE)
                    if self.player.facing == "down":
                        Attack(self, self.player.rect.x, self.player.rect.y + TILE_SIZE)
                    if self.player.facing == "left":
                        Attack(self, self.player.rect.x - TILE_SIZE, self.player.rect.y)
                    if self.player.facing == "right":
                        Attack(self, self.player.rect.x + TILE_SIZE, self.player.rect.y - TILE_SIZE)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.flip()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()


    def game_over(self):
        #Player dies
        text = self.font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.go_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        #Sets intro variable to true
        intro = True

        #Creating title in title rect and naming the game
        title = self.font.render('Down With The House', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 64)

        #A loop to check if yu quit while in the title screen
        while intro:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    intro = False
                    self.running = False

            #Gets the mouse position and checks if the mouse is pressed
            #which is an array
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            #checks if the play button is pressed and if it is pressed sets the
            #intro variable to false
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            #Draws everything like normal and updates the screen
            # at 60 fps
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
            #and when ever this screen is broken out of it moves on to
            # the next line in the interpreter.

g = Game()
g.intro_screen()
g.new()
while(g.running):
    g.main()
    g.game_over()

pygame.quit()
sys.exit()
