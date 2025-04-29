# import pygame
# import sys
# import math
# import random

# # Initialize Pygame
# pygame.init()

# # --- Constants ---
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# PLAYER_SIZE = 30
# PLAYER_COLOR = (0, 128, 255)  # Blue
# ENEMY_SIZE = 20
# ENEMY_COLOR = (255, 0, 0)  # Red
# BULLET_COLOR = (255, 255, 255)  # White
# BULLET_SIZE = 5
# BULLET_SPEED = 10
# PLAYER_SPEED = 5
# ENEMY_SPEED = 2
# WEAPON_TYPES = ['pistol', 'shotgun', 'rifle']
# DEFAULT_WEAPON = 'pistol'
# MAP_WIDTH = 2000
# MAP_HEIGHT = 1500
# CAMERA_SPEED = 5
# BLACK = (0, 0, 0)
# GREY = (128, 128, 128)
# RED = (255,0,0)
# WHITE = (255,255,255) # Define WHITE

# # --- Game Variables ---
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Mini Militia Clone")
# clock = pygame.time.Clock()
# font = pygame.font.Font(None, 30)

# # --- Helper Functions ---

# def load_images():
#     """Loads game images.  For now, we'll use simple shapes."""
#     images = {}
#     #images['player'] = pygame.image.load('player.png') # Replace with actual image
#     #images['enemy'] = pygame.image.load('enemy.png')
#     #images['bullet'] = pygame.image.load('bullet.png')
#     return images

# def draw_player(surface, position, angle):
#     """Draws the player as a rotated rectangle."""
#     #pygame.draw.rect(surface, PLAYER_COLOR, (position[0] - PLAYER_SIZE // 2, position[1] - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))
#     # Create a rotated surface.  For now, just rotate a simple square.
#     player_rect = pygame.Rect(position[0] - PLAYER_SIZE // 2, position[1] - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
#     rotated_surface = pygame.transform.rotate(pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA), angle)
#     rotated_rect = rotated_surface.get_rect(center=player_rect.center)
#     pygame.draw.rect(surface, PLAYER_COLOR, player_rect) #draw a non-rotated rect
#     surface.blit(rotated_surface, rotated_rect)


# def draw_enemy(surface, position):
#     """Draws the enemy."""
#     pygame.draw.rect(surface, ENEMY_COLOR, (position[0] - ENEMY_SIZE // 2, position[1] - ENEMY_SIZE // 2, ENEMY_SIZE, ENEMY_SIZE))

# def draw_bullet(surface, position):
#     """Draws the bullet."""
#     pygame.draw.circle(surface, BULLET_COLOR, (int(position[0]), int(position[1])), BULLET_SIZE)

# def draw_weapon_indicator(surface, position, weapon):
#     """Draws the current weapon indicator."""
#     text_surface = font.render(f"Weapon: {weapon}", True, WHITE)
#     surface.blit(text_surface, (position[0] - 50, position[1] + PLAYER_SIZE + 10))

# def generate_random_position(width, height):
#     """Generates a random position within the map boundaries."""
#     return [random.randint(0, width), random.randint(0, height)]

# def calculate_distance(pos1, pos2):
#     """Calculates the distance between two points."""
#     return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# def calculate_angle(source_pos, target_pos):
#     """Calculates the angle between two points (in degrees)."""
#     delta_x = target_pos[0] - source_pos[0]
#     delta_y = target_pos[1] - source_pos[1]
#     angle_rad = math.atan2(delta_y, delta_x)
#     return math.degrees(angle_rad)

# def move_player(player_pos, angle, speed):
#     """Moves the player based on the angle and speed."""
#     radians = math.radians(angle)
#     new_x = player_pos[0] + speed * math.cos(radians)
#     new_y = player_pos[1] + speed * math.sin(radians)
#     return [new_x, new_y]

# def move_enemy(enemy_pos, player_pos):
#     """Moves the enemy towards the player."""
#     angle = calculate_angle(enemy_pos, player_pos)
#     return move_player(enemy_pos, angle, ENEMY_SPEED)

# def fire_bullet(player_pos, angle, weapon):
#     """Fires a bullet from the player's position."""
#     if weapon == 'pistol':
#         return {'position': player_pos[:], 'angle': angle, 'speed': BULLET_SPEED, 'damage': 10}
#     elif weapon == 'shotgun':
#         bullets = []
#         for i in range(-10, 11, 5):  # Spread the bullets
#             new_angle = angle + i
#             bullets.append({'position': player_pos[:], 'angle': new_angle, 'speed': BULLET_SPEED, 'damage': 8}) #reduced damage
#         return bullets
#     elif weapon == 'rifle':
#         return {'position': player_pos[:], 'angle': angle, 'speed': BULLET_SPEED * 1.5, 'damage': 12} #increased speed and damage
#     return None

# def move_bullet(bullet):
#     """Moves the bullet based on its angle and speed."""
#     new_x = bullet['position'][0] + bullet['speed'] * math.cos(math.radians(bullet['angle']))
#     new_y = bullet['position'][1] + bullet['speed'] * math.sin(math.radians(bullet['angle']))
#     bullet['position'] = [new_x, new_y]
#     return bullet

# def check_collision_bullet_enemy(bullet, enemy_pos):
#     """Checks if a bullet collides with an enemy."""
#     distance = calculate_distance(bullet['position'], enemy_pos)
#     return distance < ENEMY_SIZE // 2 + BULLET_SIZE

# def handle_game_over(screen, font):
#     """Displays the game over screen."""
#     game_over_text = font.render("Game Over", True, RED)  # Use RED for game over text
#     restart_text = font.render("Press 'R' to Restart", True, WHITE)

#     game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
#     restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

#     screen.blit(game_over_text, game_over_rect)
#     screen.blit(restart_text, restart_rect)
#     pygame.display.flip()

# def reset_game():
#     """Resets the game to its initial state."""
#     global player_pos, player_angle, player_health, bullets, enemies, game_over, current_weapon, camera_x, camera_y
#     player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
#     player_angle = 0
#     player_health = 100
#     bullets = []
#     enemies = [generate_random_position(MAP_WIDTH, MAP_HEIGHT) for _ in range(5)]  # Start with 5 enemies
#     game_over = False
#     current_weapon = DEFAULT_WEAPON
#     camera_x = 0
#     camera_y = 0

# # --- Main Game Loop ---
# def game_loop():
#     """Main game loop."""
#     global player_pos, player_angle, player_health, bullets, enemies, game_over, current_weapon, camera_x, camera_y, score

#     images = load_images()
#     player_health = 100
#     bullets = []
#     enemies = [generate_random_position(MAP_WIDTH, MAP_HEIGHT) for _ in range(5)]  # Start with 5 enemies
#     game_over = False
#     current_weapon = DEFAULT_WEAPON
#     score = 0
#     camera_x = 0
#     camera_y = 0
#     player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2] #define player_pos here
#     player_angle = 0 # define player_angle here

#     running = True
#     while running:
#         screen.fill(BLACK)  # Clear the screen with black background
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE and not game_over:
#                     new_bullets = fire_bullet(player_pos, player_angle, current_weapon)
#                     if isinstance(new_bullets, list):  # Shotgun fires multiple bullets
#                         bullets.extend(new_bullets)
#                     else:
#                         bullets.append(new_bullets)
#                 elif event.key == pygame.K_r and game_over:
#                     reset_game()
#                 elif event.key == pygame.K_1:
#                     current_weapon = WEAPON_TYPES[0]  # Pistol
#                 elif event.key == pygame.K_2:
#                     current_weapon = WEAPON_TYPES[1]  # Shotgun
#                 elif event.key == pygame.K_3:
#                     current_weapon = WEAPON_TYPES[2]  # Rifle

#         if not game_over:
#             keys = pygame.key.get_pressed()
#             # Player movement
#             if keys[pygame.K_w]:
#                 player_pos = move_player(player_pos, 270, PLAYER_SPEED)
#             if keys[pygame.K_s]:
#                 player_pos = move_player(player_pos, 90, PLAYER_SPEED)
#             if keys[pygame.K_a]:
#                 player_pos = move_player(player_pos, 180, PLAYER_SPEED)
#             if keys[pygame.K_d]:
#                 player_pos = move_player(player_pos, 0, PLAYER_SPEED)

#             # Mouse aiming
#             mouse_pos = pygame.mouse.get_pos()
#             player_angle = calculate_angle(player_pos, mouse_pos)

#             # Move and remove bullets
#             bullets = [move_bullet(bullet) for bullet in bullets]
#             bullets = [bullet for bullet in bullets if 0 < bullet['position'][0] < MAP_WIDTH and 0 < bullet['position'][1] < MAP_HEIGHT]

#             # Move enemies
#             for i, enemy in enumerate(enemies):
#                 enemies[i] = move_enemy(enemy, player_pos)

#             # Check for bullet collisions with enemies
#             for bullet in bullets[:]:  # Iterate over a copy to avoid modification issues
#                 for i, enemy in enumerate(enemies[:]):
#                     if check_collision_bullet_enemy(bullet, enemy):
#                         bullets.remove(bullet)
#                         enemies.pop(i)
#                         player_health -= 10 # Reduce player health on hit.
#                         score += 10
#                         if player_health <= 0:
#                             game_over = True
#                             break #important
#                 if game_over:
#                     break

#             # Camera movement to keep player centered
#             camera_x = player_pos[0] - SCREEN_WIDTH // 2
#             camera_y = player_pos[1] - SCREEN_HEIGHT // 2
#             # Clamp the camera to the map edges
#             camera_x = max(0, min(camera_x, MAP_WIDTH - SCREEN_WIDTH))
#             camera_y = max(0, min(camera_y, MAP_HEIGHT - SCREEN_HEIGHT))

#             # Draw the game elements relative to the camera
#             draw_board(screen, camera_x, camera_y)  # Pass the camera offset
#             draw_player(screen, (player_pos[0] - camera_x, player_pos[1] - camera_y), player_angle)
#             for enemy in enemies:
#                 draw_enemy(screen, (enemy[0] - camera_x, enemy[1] - camera_y))
#             for bullet in bullets:
#                 draw_bullet(screen, (bullet['position'][0] - camera_x, bullet['position'][1] - camera_y))
#             draw_weapon_indicator(screen, (player_pos[0] - camera_x, player_pos[1] - camera_y), current_weapon)
#             display_score(screen, score)
#             display_health(screen, player_health, (player_pos[0] - camera_x, player_pos[1] - camera_y))

#             #draw map boundaries
#             pygame.draw.rect(screen, GREY, (0 - camera_x, 0 - camera_y, MAP_WIDTH, MAP_HEIGHT), 5)

#             if game_over:
#                 handle_game_over(screen, font)

#         pygame.display.flip()
#         clock.tick(30)

#     pygame.quit()
#     sys.exit()

# def draw_board(surface, camera_x, camera_y):
#     """Draws the game board (larger than the screen)."""
#     # For a simple example, let's draw a large background rectangle.
#     # In a real game, you'd tile images or draw more complex map elements.
#     pygame.draw.rect(surface, BLACK, (0 - camera_x, 0 - camera_y, MAP_WIDTH, MAP_HEIGHT))

# def display_score(surface, score):
#     """Displays the player's score."""
#     text_surface = font.render(f"Score: {score}", True, WHITE)
#     surface.blit(text_surface, (10, 10))

# def display_health(surface, health, position):
#     """Displays the player's health."""
#     text_surface = font.render(f"Health: {health}", True, WHITE)
#     surface.blit(text_surface, (position[0] - 50, position[1] - PLAYER_SIZE - 10))

# if __name__ == "__main__":
#     game_loop()
import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
PLAYER_COLOR = (0, 128, 255)  # Blue
ENEMY_SIZE = 20
ENEMY_COLOR = (255, 0, 0)  # Red
BULLET_COLOR = (255, 255, 255)  # White
BULLET_SIZE = 5
BULLET_SPEED = 10
PLAYER_SPEED = 5
ENEMY_SPEED = 2
WEAPON_TYPES = ['pistol', 'shotgun', 'rifle']
DEFAULT_WEAPON = 'pistol'
MAP_WIDTH = 2000
MAP_HEIGHT = 1500
CAMERA_SPEED = 5
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255,0,0)
WHITE = (255,255,255) # Define WHITE

# --- Game Variables ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Militia Clone")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# --- Helper Functions ---

def load_images():
    """Loads game images.  For now, we'll use simple shapes."""
    images = {}
    #images['player'] = pygame.image.load('player.png') # Replace with actual image
    #images['enemy'] = pygame.image.load('enemy.png')
    #images['bullet'] = pygame.image.load('bullet.png')
    return images

def draw_player(surface, position, angle):
    """Draws the player as a rotated rectangle."""
    #pygame.draw.rect(surface, PLAYER_COLOR, (position[0] - PLAYER_SIZE // 2, position[1] - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE))
    # Create a rotated surface.  For now, just rotate a simple square.
    player_rect = pygame.Rect(position[0] - PLAYER_SIZE // 2, position[1] - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE)
    rotated_surface = pygame.transform.rotate(pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA), angle)
    rotated_rect = rotated_surface.get_rect(center=player_rect.center)
    pygame.draw.rect(surface, PLAYER_COLOR, player_rect) #draw a non-rotated rect
    surface.blit(rotated_surface, rotated_rect)


def draw_enemy(surface, position):
    """Draws the enemy."""
    pygame.draw.rect(surface, ENEMY_COLOR, (position[0] - ENEMY_SIZE // 2, position[1] - ENEMY_SIZE // 2, ENEMY_SIZE, ENEMY_SIZE))

def draw_bullet(surface, position):
    """Draws the bullet."""
    pygame.draw.circle(surface, BULLET_COLOR, (int(position[0]), int(position[1])), BULLET_SIZE)

def draw_weapon_indicator(surface, position, weapon):
    """Draws the current weapon indicator."""
    text_surface = font.render(f"Weapon: {weapon}", True, WHITE)
    surface.blit(text_surface, (position[0] - 50, position[1] + PLAYER_SIZE + 10))

def generate_random_position(width, height):
    """Generates a random position within the map boundaries."""
    return [random.randint(0, width), random.randint(0, height)]

def calculate_distance(pos1, pos2):
    """Calculates the distance between two points."""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def calculate_angle(source_pos, target_pos):
    """Calculates the angle between two points (in degrees)."""
    delta_x = target_pos[0] - source_pos[0]
    delta_y = target_pos[1] - source_pos[1]
    angle_rad = math.atan2(delta_y, delta_x)
    return math.degrees(angle_rad)

def move_player(player_pos, angle, speed):
    """Moves the player based on the angle and speed."""
    radians = math.radians(angle)
    new_x = player_pos[0] + speed * math.cos(radians)
    new_y = player_pos[1] + speed * math.sin(radians)
    return [new_x, new_y]

def move_enemy(enemy_pos, player_pos):
    """Moves the enemy towards the player."""
    angle = calculate_angle(enemy_pos, player_pos)
    return move_player(enemy_pos, angle, ENEMY_SPEED)

def fire_bullet(player_pos, angle, weapon):
    """Fires a bullet from the player's position."""
    if weapon == 'pistol':
        return {'position': player_pos[:], 'angle': angle, 'speed': BULLET_SPEED, 'damage': 10}
    elif weapon == 'shotgun':
        bullets = []
        for i in range(-10, 11, 5):  # Spread the bullets
            new_angle = angle + i
            bullets.append({'position': player_pos[:], 'angle': new_angle, 'speed': BULLET_SPEED, 'damage': 8}) #reduced damage
        return bullets
    elif weapon == 'rifle':
        return {'position': player_pos[:], 'angle': angle, 'speed': BULLET_SPEED * 1.5, 'damage': 12} #increased speed and damage
    return None

def move_bullet(bullet):
    """Moves the bullet based on its angle and speed."""
    new_x = bullet['position'][0] + bullet['speed'] * math.cos(math.radians(bullet['angle']))
    new_y = bullet['position'][1] + bullet['speed'] * math.sin(math.radians(bullet['angle']))
    bullet['position'] = [new_x, new_y]
    return bullet

def check_collision_bullet_enemy(bullet, enemy_pos):
    """Checks if a bullet collides with an enemy."""
    distance = calculate_distance(bullet['position'], enemy_pos)
    return distance < ENEMY_SIZE // 2 + BULLET_SIZE

def handle_game_over(screen, font):
    """Displays the game over screen."""
    game_over_text = font.render("Game Over", True, RED)  # Use RED for game over text
    restart_text = font.render("Press 'R' to Restart", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()

def reset_game():
    """Resets the game to its initial state."""
    global player_pos, player_angle, player_health, bullets, enemies, game_over, current_weapon, camera_x, camera_y
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    player_angle = 0
    player_health = 100
    bullets = []
    enemies = [generate_random_position(MAP_WIDTH, MAP_HEIGHT) for _ in range(5)]  # Start with 5 enemies
    game_over = False
    current_weapon = DEFAULT_WEAPON
    camera_x = 0
    camera_y = 0

# --- Main Game Loop ---
def game_loop():
    """Main game loop."""
    global player_pos, player_angle, player_health, bullets, enemies, game_over, current_weapon, camera_x, camera_y, score

    images = load_images()
    player_health = 100
    bullets = []
    enemies = [generate_random_position(MAP_WIDTH, MAP_HEIGHT) for _ in range(5)]  # Start with 5 enemies
    game_over = False
    current_weapon = DEFAULT_WEAPON
    score = 0
    camera_x = 0
    camera_y = 0
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2] #define player_pos here
    player_angle = 0 # define player_angle here

    running = True
    while running:
        screen.fill(BLACK)  # Clear the screen with black background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    new_bullets = fire_bullet(player_pos, player_angle, current_weapon)
                    if isinstance(new_bullets, list):  # Shotgun fires multiple bullets
                        bullets.extend(new_bullets)
                    else:
                        bullets.append(new_bullets)
                elif event.key == pygame.K_r and game_over:
                    reset_game()
                elif event.key == pygame.K_1:
                    current_weapon = WEAPON_TYPES[0]  # Pistol
                elif event.key == pygame.K_2:
                    current_weapon = WEAPON_TYPES[1]  # Shotgun
                elif event.key == pygame.K_3:
                    current_weapon = WEAPON_TYPES[2]  # Rifle

        if not game_over:
            keys = pygame.key.get_pressed()
            # Player movement
            if keys[pygame.K_UP]:
                player_pos = move_player(player_pos, 270, PLAYER_SPEED)
            if keys[pygame.K_DOWN]:
                player_pos = move_player(player_pos, 90, PLAYER_SPEED)
            if keys[pygame.K_LEFT]:
                player_pos = move_player(player_pos, 180, PLAYER_SPEED)
            if keys[pygame.K_RIGHT]:
                player_pos = move_player(player_pos, 0, PLAYER_SPEED)

            # Mouse aiming
            mouse_pos = pygame.mouse.get_pos()
            player_angle = calculate_angle(player_pos, mouse_pos)

            # Move and remove bullets
            bullets = [move_bullet(bullet) for bullet in bullets]
            bullets = [bullet for bullet in bullets if 0 < bullet['position'][0] < MAP_WIDTH and 0 < bullet['position'][1] < MAP_HEIGHT]

            # Move enemies
            for i, enemy in enumerate(enemies):
                enemies[i] = move_enemy(enemy, player_pos)

            # Check for bullet collisions with enemies
            for bullet in bullets[:]:  # Iterate over a copy to avoid modification issues
                for i, enemy in enumerate(enemies[:]):
                    if check_collision_bullet_enemy(bullet, enemy):
                        bullets.remove(bullet)
                        enemies.pop(i)
                        player_health -= 10 # Reduce player health on hit.
                        score += 10
                        if player_health <= 0:
                            game_over = True
                            break #important
                if game_over:
                    break

            # Camera movement to keep player centered
            camera_x = player_pos[0] - SCREEN_WIDTH // 2
            camera_y = player_pos[1] - SCREEN_HEIGHT // 2
            # Clamp the camera to the map edges
            camera_x = max(0, min(camera_x, MAP_WIDTH - SCREEN_WIDTH))
            camera_y = max(0, min(camera_y, MAP_HEIGHT - SCREEN_HEIGHT))

            # Draw the game elements relative to the camera
            draw_board(screen, camera_x, camera_y)  # Pass the camera offset
            draw_player(screen, (player_pos[0] - camera_x, player_pos[1] - camera_y), player_angle)
            for enemy in enemies:
                draw_enemy(screen, (enemy[0] - camera_x, enemy[1] - camera_y))
            for bullet in bullets:
                draw_bullet(screen, (bullet['position'][0] - camera_x, bullet['position'][1] - camera_y))
            draw_weapon_indicator(screen, (player_pos[0] - camera_x, player_pos[1] - camera_y), current_weapon)
            display_score(screen, score)
            display_health(screen, player_health, (player_pos[0] - camera_x, player_pos[1] - camera_y))

            #draw map boundaries
            pygame.draw.rect(screen, GREY, (0 - camera_x, 0 - camera_y, MAP_WIDTH, MAP_HEIGHT), 5)

            if game_over:
                handle_game_over(screen, font)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

def draw_board(surface, camera_x, camera_y):
    """Draws the game board (larger than the screen)."""
    # For a simple example, let's draw a large background rectangle.
    # In a real game, you'd tile images or draw more complex map elements.
    pygame.draw.rect(surface, BLACK, (0 - camera_x, 0 - camera_y, MAP_WIDTH, MAP_HEIGHT))

def display_score(surface, score):
    """Displays the player's score."""
    text_surface = font.render(f"Score: {score}", True, WHITE)
    surface.blit(text_surface, (10, 10))

def display_health(surface, health, position):
    """Displays the player's health."""
    text_surface = font.render(f"Health: {health}", True, WHITE)
    surface.blit(text_surface, (position[0] - 50, position[1] - PLAYER_SIZE - 10))

if __name__ == "__main__":
    game_loop()
