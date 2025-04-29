import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (0, 255, 0)  # Green
DOODLE_WIDTH = 50
DOODLE_HEIGHT = 50
GRAVITY = 0.8
JUMP_SPEED = -20
MOVE_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# --- Game Variables ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doodle Jump")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Load the doodle image
try:
    doodle_img = pygame.image.load('doodle.png')
    doodle_img = pygame.transform.scale(doodle_img, (DOODLE_WIDTH, DOODLE_HEIGHT))  # Resize as needed
except pygame.error as e:
    print(f"Error loading doodle image: {e}")
    # Handle the error, e.g., use a placeholder or exit
    sys.exit()

# Doodle initial position and velocity
doodle_x = SCREEN_WIDTH // 2 - DOODLE_WIDTH // 2
doodle_y = SCREEN_HEIGHT - DOODLE_HEIGHT
doodle_velocity = 0
doodle_on_platform = False

# Platform list: each platform is [x, y]
platforms = [[SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT - 10],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 + 100, SCREEN_HEIGHT - PLATFORM_HEIGHT - 150],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 - 100, SCREEN_HEIGHT - PLATFORM_HEIGHT - 250],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 + 50, SCREEN_HEIGHT - PLATFORM_HEIGHT - 350],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 - 50, SCREEN_HEIGHT - PLATFORM_HEIGHT - 450]]

# Game over flag
game_over = False
score = 0

def draw_doodle():
    """Draws the doodle on the screen."""
    screen.blit(doodle_img, (doodle_x, doodle_y))

def draw_platforms():
    """Draws the platforms on the screen."""
    for platform_x, platform_y in platforms:
        pygame.draw.rect(screen, PLATFORM_COLOR, (platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT))

def update_doodle():
    """Updates the doodle's position and velocity."""
    global doodle_velocity, doodle_y, game_over, doodle_on_platform, doodle_x #added doodle_x to global
    if not game_over:
        doodle_velocity += GRAVITY
        doodle_y += doodle_velocity

        # Side boundaries
        if doodle_x < 0:
            doodle_x = 0
        elif doodle_x > SCREEN_WIDTH - DOODLE_WIDTH:
            doodle_x = SCREEN_WIDTH - DOODLE_WIDTH

        # Bottom boundary (Game Over)
        if doodle_y > SCREEN_HEIGHT:
            game_over = True

        doodle_on_platform = False #reset
        # Platform collision
        for platform_x, platform_y in platforms:
            if (doodle_x < platform_x + PLATFORM_WIDTH and
                    doodle_x + DOODLE_WIDTH > platform_x and
                    doodle_y + DOODLE_HEIGHT > platform_y and
                    doodle_y < platform_y + PLATFORM_HEIGHT / 2 and #only collide with the top half
                    doodle_velocity >= 0):
                doodle_y = platform_y - DOODLE_HEIGHT
                doodle_velocity = JUMP_SPEED
                doodle_on_platform = True
                break

def move_platforms():
    """Moves the platforms up."""
    global platforms, score
    if doodle_velocity < 0 and doodle_y < SCREEN_HEIGHT / 3: # Move platforms when doodle jumps to the top 1/3 of screen
        for i in range(len(platforms)):
            platforms[i][1] += -doodle_velocity
        # Generate new platforms
        if platforms[-1][1] > 0:
            new_platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
            new_platform_y = platforms[-1][1] - PLATFORM_HEIGHT - random.randint(70, 120)
            platforms.append([new_platform_x, new_platform_y])
            score += 1
        # Remove off-screen platforms
        platforms = [platform for platform in platforms if platform[1] < SCREEN_HEIGHT]

def handle_input():
    """Handles user input."""
    keys = pygame.key.get_pressed()
    global doodle_x #added doodle_x to global
    if keys[pygame.K_LEFT]:
        doodle_x -= MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        doodle_x += MOVE_SPEED
    for event in pygame.event.get(): #important
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()

def display_game_over():
    """Displays the game over screen."""
    text_surface = font.render("Game Over!", True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    score_text = font.render(f"Final Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Press 'R' to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

def display_score():
    """Displays the current score."""
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def reset_game():
    """Resets the game to its initial state."""
    global doodle_x, doodle_y, doodle_velocity, platforms, game_over, score
    doodle_x = SCREEN_WIDTH // 2 - DOODLE_WIDTH // 2
    doodle_y = SCREEN_HEIGHT - DOODLE_HEIGHT
    doodle_velocity = 0
    game_over = False
    score = 0
    platforms = [[SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT - 10],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 + 100, SCREEN_HEIGHT - PLATFORM_HEIGHT - 150],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 - 100, SCREEN_HEIGHT - PLATFORM_HEIGHT - 250],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 + 50, SCREEN_HEIGHT - PLATFORM_HEIGHT - 350],
             [SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2 - 50, SCREEN_HEIGHT - PLATFORM_HEIGHT - 450]]

# --- Main Game Loop ---
def game_loop():
    """Main game loop."""
    global doodle_velocity, game_over

    running = True
    while running:
        screen.fill(WHITE)  # White background
        handle_input()

        if not game_over:
            update_doodle()
            move_platforms()

        draw_platforms()
        draw_doodle()
        display_score()

        if game_over:
            display_game_over()
            keys = pygame.key.get_pressed() #get keys
            if keys[pygame.K_r]:
                reset_game()
                game_over = False # added this line

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
