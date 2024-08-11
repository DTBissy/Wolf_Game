import pygame
from config import WIN_WIDTH

class Bomb(pygame.sprite.Sprite):
    # Bomb ('X'): Loop on create_tile_map
    def __init__(self, game, x, y):
        super().__init__()
        # Load the image representing the bomb and set its initial position
        self.image = pygame.image.load('sprites/pigs/bomb.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        #self.speed = 5 # Adjust speed as necessary
        self.active = True # Flag to indicate if the bomb is active
        self.triggered = False # Flag to indicate is bomb has triggered an explosion

    def update(self):
        # If bomb is active, update its position
        #if self.active:
            # Move the bomb to the right by the speed value
            #self.rect.x += self.speed # Adjust movement based on desired behavior
            #if self.rect.x > WIN_WIDTH: # If the bomb moves off the screen
                #self.kill() # Remove the bomb sprite from all groups if it goes off-screen

#class Explosion(pygame.sprite.Sprite):
    #def __init__(self, x, y, explosion_images): # added the explosion_images
        """Initialize the explosion at the given position."""
        #super().__init__() # Call parent class (Sprite) initializer
        #self.images = [] # List to store the explosion animation frames

        # load and scale each frame of the explosion animation
        #for num in range(1, 6):
            #try:
                #img = pygame.image.load(f"sprites/pigs/exp{num}.png") # Loads each explosion image
                #img = pygame.transform.scale(img, (100, 100)) # Scale image to 100x100 pixels
                #self.images.append(img) # Add image to list
            #except pygame.error as e:
                #print(f"Error loading image sprites/pigs/exp{num}.png: {e}") # Error message if it fails


        #self.index = 0 # Current frame index of animation
        #self.image = self.images[self.index] # Set the initial image of the explosion to the first frame
        #self.rect = self.image.get_rect(center=(x, y)) # Center the explosion image at the given (x, y) coordinates
        #self.animation_speed = 5 # Set the speed at which the animation frames change (lower is faster)
        #self.current_frame = 0 # Counter to control when the next frame should be displayed

    #def update(self):
        #self.current_frame += 1
        #if self.current_frame >= self.animation_speed:
            #self.current_frame = 0 # Reset counter after reaching animation
            #self.index += 1 # move to next frame
            #if self.index >= len(self.images):
                #self.kill() # Remove explosion sprite from all groups if the animation finishes
            #else:
                #self.image = self.images[self.index] # Update the sprite's image to the next frame