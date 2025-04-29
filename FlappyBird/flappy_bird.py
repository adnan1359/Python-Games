import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FLOOR_HEIGHT = 100
GRAVITY = 0.8
FLAP_SPEED = -10
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = -4
PIPE_FREQUENCY = 2000  # milliseconds
GAME_OVER_TEXT_COLOR = (255, 0, 0)  # Red
FONT_SIZE = 40
WHITE = (255, 255, 255)
GREEN = (0, 255, 0) # Define GREEN color

# --- Game Variables ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Load the bird image
try:
    bird_img = pygame.image.load('flappy.jpg')
    bird_img = pygame.transform.scale(bird_img, (50, 50))  # Resize as needed
except pygame.error as e:
    print(f"Error loading bird image: {e}")
    # Handle the error, e.g., use a placeholder or exit
    sys.exit()

# Bird initial position and velocity
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

# Pipe list: each pipe is a list of [x, top_height, bottom_height]
pipes = []
last_pipe_time = 0

score = 0
game_over = False
start_time = 0 #used to calculate score

def draw_bird():
    """Draws the bird on the screen."""
    screen.blit(bird_img, (bird_x, bird_y))

def draw_pipes():
    """Draws the pipes on the screen."""
    for pipe_x, top_height, bottom_height in pipes:
        # Top pipe
        pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, top_height))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (pipe_x, SCREEN_HEIGHT - bottom_height, PIPE_WIDTH, bottom_height))

def generate_pipes():
    """Generates a new pair of pipes."""
    global last_pipe_time
    current_time = pygame.time.get_ticks()
    if current_time - last_pipe_time > PIPE_FREQUENCY:
        last_pipe_time = current_time
        top_height = random.randint(100, SCREEN_HEIGHT - FLOOR_HEIGHT - PIPE_GAP - 100)
        bottom_height = SCREEN_HEIGHT - FLOOR_HEIGHT - top_height - PIPE_GAP
        pipes.append([SCREEN_WIDTH, top_height, bottom_height])

def move_pipes():
    """Moves the pipes to the left and removes the ones that are off-screen."""
    global pipes, score
    for i in range(len(pipes)):
        pipes[i][0] += PIPE_SPEED
    # Remove pipes that are off-screen
    if pipes and pipes[0][0] < -PIPE_WIDTH:
        pipes.pop(0)
        score += 1

def update_bird():
    """Updates the bird's position and velocity."""
    global bird_velocity, bird_y, game_over
    if not game_over:
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Collision with floor or ceiling
        if bird_y > SCREEN_HEIGHT - FLOOR_HEIGHT or bird_y < 0:
            game_over = True

def check_collision():
    """Checks for collision between the bird and the pipes."""
    global game_over
    if not game_over:
        for pipe_x, top_height, bottom_height in pipes:
            if bird_x + 50 > pipe_x and bird_x < pipe_x + PIPE_WIDTH:  # Adjusted for bird width
                if bird_y < top_height or bird_y + 30 > SCREEN_HEIGHT - bottom_height: #Adjusted for bird height
                    game_over = True
                    break

def draw_floor():
    """Draws the floor."""
    pygame.draw.rect(screen, (200, 200, 200), (0, SCREEN_HEIGHT - FLOOR_HEIGHT, SCREEN_WIDTH, FLOOR_HEIGHT))

def display_game_over():
    """Displays the game over screen."""
    text_surface = font.render("Game Over!", True, GAME_OVER_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(text_surface, text_rect)

    score_text = font.render(f"Final Score: {score}", True, GAME_OVER_TEXT_COLOR)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Press 'R' to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)

def display_score():
    """Displays the current score."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def reset_game():
    """Resets the game state."""
    global bird_y, bird_velocity, pipes, game_over, score, start_time
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = []
    game_over = False
    score = 0
    start_time = pygame.time.get_ticks()


# --- Main Game Loop ---
def game_loop():
    """Main game loop."""
    global bird_velocity, game_over, start_time
    running = True
    start_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = FLAP_SPEED
                elif event.key == pygame.K_r and game_over:
                    reset_game()

        if not game_over:
            generate_pipes()
            move_pipes()
            update_bird()
            check_collision()

        screen.fill((0, 0, 0))  # Black background
        draw_pipes()
        draw_floor()
        draw_bird()
        display_score() #show score

        if game_over:
            display_game_over()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
