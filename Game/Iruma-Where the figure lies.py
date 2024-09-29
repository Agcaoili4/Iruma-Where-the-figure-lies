import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Iruma - Where the figures lie")

# Set up screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 620
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#clock object to control frame rate
clock = pygame.time.Clock()

# Define background color
BG = (0, 0, 0)

# Load the sprite sheets with transparency support
sprite_sheet_image = pygame.image.load(r"Game\walk.png").convert_alpha()
sprite_sheet_image_2 = pygame.image.load(r"Game\idle.png").convert_alpha()
sprite_sheet_image_3 = pygame.image.load(r"Game\death.png").convert_alpha()
sprite_sheet_image_4 = pygame.image.load(r"Game\left.png").convert_alpha()
sprite_sheet_image_5 = pygame.image.load(`r"Game\right.png").convert_alpha()


def get_image(sheet, x, y, width, height):
    """Extract an image from the sprite sheet, with transparency."""
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    return image

# Character class to handle movement, frames, and rendering
class Character:
    def __init__(self):
        # Load character frames (from walking, idle, and death sprite sheets)
        self.frames = { 
            'walk': get_image(sprite_sheet_image, 0, 0, 35, 31),
            'idle': get_image(sprite_sheet_image_2, 0, 0, 35, 31),
            'dead': get_image(sprite_sheet_image_3, 0, 0, 35, 31),
            'left': get_image(sprite_sheet_image_4, 0, 0, 35, 31),
            'right': get_image(sprite_sheet_image_5, 0, 0, 35, 31)
        }
        
        #resize character
        
        # Set the initial frame (idle) and position
        self.current_frame = self.frames['idle']
        self.rect = self.current_frame.get_rect(topleft=(100, 100))
    
    def update(self, keys, walls):
        # Store the old position
        old_rect = self.rect.copy()
        
        # Handle movement input
        move_speed = 3  # Set a smaller move speed for slower movement
        
        # Handle movement input
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(move_speed, 0)  # Move right
            self.current_frame = self.frames['right']
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.move_ip(-move_speed, 0)  # Move left
            self.current_frame = self.frames['left']
        elif (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.top > 0:
            self.rect.move_ip(0, -move_speed)  # Move up
            self.current_frame = self.frames['walk']
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, move_speed)  # Move down
            self.current_frame = self.frames['walk']
        else:
            
            self.current_frame = self.frames['idle']  # Stay idle if no keys are pressed
        
        # Check for collisions with walls
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = old_rect  # Revert to the old position if collision occurs
                
        # Stay idle if no keys are pressed
        if self.rect == old_rect:
            self.current_frame = self.frames['idle']
    
    def draw(self, surface):
        # Draw the character at its current position
        surface.blit(self.current_frame, self.rect.topleft)

# Create a character instance
character = Character()

# Define walls to create a maze-like structure
walls = [
    # Define the maze structure using rectangular walls (x, y, width, height)
    pygame.Rect(0, 0, SCREEN_WIDTH, 20),  
    pygame.Rect(0, 0, 20, SCREEN_HEIGHT),  
    pygame.Rect(SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT),  
    pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  
    pygame.Rect(100, 150, 20, 100),  
    pygame.Rect(200, 150, 100, 20),
    pygame.Rect(300, 100, 7, 100),  
    pygame.Rect(400, 150, 20, 100), 
    pygame.Rect(500, 50, 100, 20),  
    pygame.Rect(500, 100, 20, 100), 
    pygame.Rect(600, 100, 100, 20), 
    pygame.Rect(700, 150, 20, 100),
    pygame.Rect(800, 100, 20, 100),  
    pygame.Rect(600, 300, 200, 20),  
    pygame.Rect(600, 300, 20, 200),  
    pygame.Rect(800, 300, 20, 200),  
    pygame.Rect(400, 400, 200, 20), 
    pygame.Rect(600, 400, 20, 200),
    pygame.Rect(400, 500, 20, 200),
    pygame.Rect(900, 280,  200, 20),
    pygame.Rect(100, 500, 200, 200),
    pygame.Rect(900, 280,  20, 200),
    pygame.Rect(1000, 280,  20, 200),
]

# Game loop
run = True
while run:
    # Update background
    screen.fill(BG)

    # Get pressed keys
    keys = pygame.key.get_pressed()
    
    # Update the character state based on key inputs
    character.update(keys, walls)
    
    # Draw the character
    character.draw(screen)

    # Draw the walls
    for wall in walls:
        pygame.draw.rect(screen, (50, 50, 50), wall)
    
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Update the display
    pygame.display.update()
    clock.tick(60)

#quit the pygame in background
pygame.quit()