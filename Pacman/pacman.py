import pygame
import random
import time

# Initialize Pygame
pygame.init()

# --- Constants ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 105, 180)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
PACMAN_SIZE = 20
GHOST_SIZE = 20

# Pacman starting position (in grid coordinates)
PACMAN_START_X = 1
PACMAN_START_Y = 5

# Ghost starting positions (in grid coordinates)
GHOST1_START_X = 10
GHOST1_START_Y = 8
GHOST2_START_X = 9
GHOST2_START_Y = 9
GHOST3_START_X = 10
GHOST3_START_Y = 9
GHOST4_START_X = 11
GHOST4_START_Y = 9

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STOP = (0, 0)

# Game states
GAME_START = 0
GAME_PLAYING = 1
GAME_OVER = 2
GAME_WIN = 3


# --- Helper Functions ---

def draw_text(surface, text, size, x, y, color):
    """Draws text on the screen."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)



def draw_maze(surface, maze):
    """Draws the maze on the screen."""
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:  # Wall
                pygame.draw.rect(surface, BLUE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)
            elif cell == 0:  # Food
                pygame.draw.circle(surface, YELLOW, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 3)
            elif cell == 2:  # Super Food
                pygame.draw.circle(surface, YELLOW, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 8)



def move_pacman(pacman_x, pacman_y, direction, maze):
    """Moves Pac-Man, handling wall collisions."""
    new_x = pacman_x
    new_y = pacman_y

    if direction == UP:
        new_y -= 1
    elif direction == DOWN:
        new_y += 1
    elif direction == LEFT:
        new_x -= 1
    elif direction == RIGHT:
        new_x += 1

    if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]) and maze[new_y][new_x] != 1:
        return new_x, new_y, direction
    else:
        return pacman_x, pacman_y, STOP



def move_ghost(ghost_x, ghost_y, direction, maze):
    """Moves a ghost, handling wall collisions and random turns."""
    new_x = ghost_x
    new_y = ghost_y

    if random.random() < 0.2:
        possible_directions = [UP, DOWN, LEFT, RIGHT]
        random.shuffle(possible_directions)
        for new_direction in possible_directions:
            if 0 <= ghost_y + new_direction[1] < len(maze) and 0 <= ghost_x + new_direction[0] < len(maze[0]) and maze[ghost_y + new_direction[1]][ghost_x + new_direction[0]] != 1:
                direction = new_direction
                break

    if direction == UP:
        new_y -= 1
    elif direction == DOWN:
        new_y += 1
    elif direction == LEFT:
        new_x -= 1
    elif direction == RIGHT:
        new_x += 1

    if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]) and maze[new_y][new_x] != 1:
        return new_x, new_y, direction
    else:
        return ghost_x, ghost_y, direction



def check_collision(pacman_x, pacman_y, ghost_x, ghost_y):
    """Checks if Pac-Man and a ghost collide."""
    distance = ((pacman_x - ghost_x) ** 2 + (pacman_y - ghost_y) ** 2) ** 0.5
    return distance < 1



def eat_food(pacman_x, pacman_y, maze, score):
    """Pac-Man eats food, updating the maze and score."""
    if maze[pacman_y][pacman_x] == 0:
        maze[pacman_y][pacman_x] = ' '  # Changed from 0 to ' '
        score += 10
    elif maze[pacman_y][pacman_x] == 2:
        maze[pacman_y][pacman_x] = ' '  # Changed from 2 to ' '
        score += 50
        return score, True
    return score, False



def draw_pacman(surface, x, y, direction, mouth_open):
    """Draws Pac-Man with animation."""
    center_x = x * GRID_SIZE + GRID_SIZE // 2
    center_y = y * GRID_SIZE + GRID_SIZE // 2
    radius = PACMAN_SIZE // 2

    if mouth_open:
        if direction == UP:
            start_angle = 30
            end_angle = 330
        elif direction == DOWN:
            start_angle = 210
            end_angle = -30
        elif direction == LEFT:
            start_angle = 120
            end_angle = -120
        elif direction == RIGHT:
            start_angle = -60
            end_angle = 60
        elif direction == STOP:
            start_angle = 0
            end_angle = 360
    else:
        start_angle = 0
        end_angle = 360

    pygame.draw.circle(surface, YELLOW, (center_x, center_y), radius)
    pygame.draw.arc(surface, BLACK,
                     (center_x - radius, center_y - radius, PACMAN_SIZE, PACMAN_SIZE),
                     start_angle * 3.14 / 180, end_angle * 3.14 / 180, 3)



def draw_ghost(surface, x, y, color):
    """Draws a ghost."""
    center_x = x * GRID_SIZE + GRID_SIZE // 2
    center_y = y * GRID_SIZE + GRID_SIZE // 2
    radius = GHOST_SIZE // 2

    # Draw the main body of the ghost
    pygame.draw.circle(surface, color, (center_x, center_y - 2), radius)
    pygame.draw.rect(surface, color, (center_x - radius, center_y - 2, GHOST_SIZE, radius + 2))

    # Draw the eyes
    eye_offset = radius // 3
    pygame.draw.circle(surface, WHITE, (center_x - eye_offset, center_y - 2), 4)
    pygame.draw.circle(surface, WHITE, (center_x + eye_offset, center_y - 2), 4)

    # Draw the pupils
    pupil_offset_x = 2
    pupil_offset_y = 1
    pygame.draw.circle(surface, BLACK, (center_x - eye_offset + pupil_offset_x, center_y - 2 + pupil_offset_y), 2)
    pygame.draw.circle(surface, BLACK, (center_x + eye_offset + pupil_offset_x, center_y - 2 + pupil_offset_y), 2)

    # Draw the wavy bottom of the ghost
    for i in range(-radius, radius + 1, radius // 3):
        pygame.draw.circle(surface, color, (center_x + i, center_y + radius - 2), 3)



# --- Game Variables ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Game")
clock = pygame.time.Clock()

# Game maze (0: food, 1: wall, 2: superfood, ' ': empty)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 'G', 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 'G', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# Find the starting positions of the ghosts in the maze
ghost1_x, ghost1_y = 0, 0
ghost2_x, ghost2_y = 0, 0
ghost3_x, ghost3_y = 0, 0
ghost4_x, ghost4_y = 0, 0

for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == 'G':
            if ghost1_x == 0 and ghost1_y == 0:
                ghost1_x, ghost1_y = x, y
            elif ghost2_x == 0 and ghost2_y == 0:
                ghost2_x, ghost2_y = x, y
            elif ghost3_x == 0 and ghost3_y == 0:
                ghost3_x, ghost3_y = x, y
            elif ghost4_x == 0 and ghost4_y == 0:
                ghost4_x, ghost4_y = x, y
            maze[y][x] = ' '

# Game variables
pacman_x = PACMAN_START_X
pacman_y = PACMAN_START_Y
pacman_direction = STOP
new_direction = STOP
ghost1_direction = RIGHT
ghost2_direction = LEFT
ghost3_direction = DOWN
ghost4_direction = UP
score = 0
game_state = GAME_START
mouth_open = True
frame_count = 0
powerup = False
powerup_duration = 0



# --- Main Game Loop ---
def game_loop():
    global pacman_x, pacman_y, pacman_direction, new_direction
    global ghost1_x, ghost1_y, ghost1_direction
    global ghost2_x, ghost2_y, ghost2_direction
    global ghost3_x, ghost3_y, ghost3_direction
    global ghost4_x, ghost4_y, ghost4_direction
    global score, game_state, mouth_open, frame_count, powerup, powerup_duration
    global maze

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new_direction = UP
                elif event.key == pygame.K_DOWN:
                    new_direction = DOWN
                elif event.key == pygame.K_LEFT:
                    new_direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    new_direction = RIGHT
                elif event.key == pygame.K_SPACE and game_state == GAME_START:
                    game_state = GAME_PLAYING
                elif event.key == pygame.K_r and game_state == GAME_OVER:
                    pacman_x = PACMAN_START_X
                    pacman_y = PACMAN_START_Y
                    pacman_direction = STOP
                    new_direction = STOP
                    ghost1_x = GHOST1_START_X
                    ghost1_y = GHOST1_START_Y
                    ghost2_x = GHOST2_START_X
                    ghost2_y = GHOST2_START_Y
                    ghost3_x = GHOST3_START_X
                    ghost3_y = GHOST3_START_Y
                    ghost4_x = GHOST4_START_X
                    ghost4_y = GHOST4_START_Y
                    ghost1_direction = RIGHT
                    ghost2_direction = LEFT
                    ghost3_direction = DOWN
                    ghost4_direction = UP
                    score = 0
                    game_state = GAME_PLAYING
                    mouth_open = True
                    frame_count = 0
                    powerup = False
                    powerup_duration = 0

                    maze = [
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 1, 0, 1, 'G', 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 1, 'G', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                        [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,0, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                    ]

                    ghost1_x, ghost1_y = 0, 0
                    ghost2_x, ghost2_y = 0, 0
                    ghost3_x, ghost3_y = 0, 0
                    ghost4_x, ghost4_y = 0, 0

                    for y, row in enumerate(maze):
                        for x, cell in enumerate(row):
                            if cell == 'G':
                                if ghost1_x == 0 and ghost1_y == 0:
                                    ghost1_x, ghost1_y = x, y
                                elif ghost2_x == 0 and ghost2_y == 0:
                                    ghost2_x, ghost2_y = x, y
                                elif ghost3_x == 0 and ghost3_y == 0:
                                    ghost3_x, ghost3_y = x, y
                                elif ghost4_x == 0 and ghost4_y == 0:
                                    ghost4_x, ghost4_y = x, y
                                maze[y][x] = ' '


        if game_state == GAME_PLAYING:
            # Move Pac-Man
            pacman_x, pacman_y, pacman_direction = move_pacman(pacman_x, pacman_y, new_direction, maze)
            if new_direction != STOP:
                pacman_direction = new_direction

            # Move ghosts
            ghost1_x, ghost1_y, ghost1_direction = move_ghost(ghost1_x, ghost1_y, ghost1_direction, maze)
            ghost2_x, ghost2_y, ghost2_direction = move_ghost(ghost2_x, ghost2_y, ghost2_direction, maze)
            ghost3_x, ghost3_y, ghost3_direction = move_ghost(ghost3_x, ghost3_y, ghost3_direction, maze)
            ghost4_x, ghost4_y, ghost4_direction = move_ghost(ghost4_x, ghost4_y, ghost4_direction, maze)

            # Eat food
            score, food_eaten = eat_food(pacman_x, pacman_y, maze, score)
            if food_eaten:
                powerup = True
                powerup_duration = 100

            # Check for collisions
            if powerup:
                if (check_collision(pacman_x, pacman_y, ghost1_x, ghost1_y) or
                    check_collision(pacman_x, pacman_y, ghost2_x, ghost2_y) or
                    check_collision(pacman_x, pacman_y, ghost3_x, ghost3_y) or
                    check_collision(pacman_x, pacman_y, ghost4_x, ghost4_y)):
                    score += 200
                    if check_collision(pacman_x, pacman_y, ghost1_x, ghost1_y):
                        ghost1_x = GHOST1_START_X
                        ghost1_y = GHOST1_START_Y
                    elif check_collision(pacman_x, pacman_y, ghost2_x, ghost2_y):
                        ghost2_x = GHOST2_START_X
                        ghost2_y = GHOST2_START_Y
                    elif check_collision(pacman_x, pacman_y, ghost3_x, ghost3_y):
                        ghost3_x = GHOST3_START_X
                        ghost3_y = GHOST3_START_Y
                    elif check_collision(pacman_x, pacman_y, ghost4_x, ghost4_y):
                        ghost4_x = GHOST4_START_X
                        ghost4_y = GHOST4_START_Y
                    powerup = False

                powerup_duration -= 1
                if powerup_duration <= 0:
                    powerup = False
            else:
                if (check_collision(pacman_x, pacman_y, ghost1_x, ghost1_y) or
                    check_collision(pacman_x, pacman_y, ghost2_x, ghost2_y) or
                    check_collision(pacman_x, pacman_y, ghost3_x, ghost3_y) or
                    check_collision(pacman_x, pacman_y, ghost4_x, ghost4_y)):
                    game_state = GAME_OVER

            # Check for win
            food_count = 0
            for row in maze:
                food_count += row.count(0) + row.count(2)
            if food_count == 0:
                game_state = GAME_WIN


        # --- Drawing ---
        screen.fill(BLACK)
        draw_maze(screen, maze)
        draw_pacman(screen, pacman_x, pacman_y, pacman_direction, mouth_open)
        draw_ghost(screen, ghost1_x, ghost1_y, RED)
        draw_ghost(screen, ghost2_x, ghost2_y, BLUE)
        draw_ghost(screen, ghost3_x, ghost3_y, PINK)
        draw_ghost(screen, ghost4_x, ghost4_y, WHITE)
        draw_text(screen, f"Score: {score}", 36, SCREEN_WIDTH // 2, 20, WHITE)

        if game_state == GAME_START:
            draw_text(screen, "Press SPACE to Start", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
        elif game_state == GAME_OVER:
            draw_text(screen, "Game Over!", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, RED)
            draw_text(screen, f"Final Score: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)
            draw_text(screen, "Press R to Restart", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, WHITE)
        elif game_state == GAME_WIN:
            draw_text(screen, "You Win!", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, YELLOW)
            draw_text(screen, f"Final Score: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, WHITE)

        pygame.display.flip()
        clock.tick(10)

        frame_count += 1
        if frame_count % 5 == 0:
            mouth_open = not mouth_open

    pygame.quit()



if __name__ == "__main__":
    game_loop()
