import pygame
import sys

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOARD_SIZE = 3
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
X_COLOR = (255, 0, 0)  # Red for X
O_COLOR = (0, 0, 255)  # Blue for O
GREY = (128,128,128)

# --- Game Variables ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 100)  # Increased font size for better visibility

board = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
]  # Use None for empty squares
player = 'X'  # 'X' or 'O'
game_over = False
winner = None

# --- Helper Functions ---

def draw_board():
    """Draws the Tic-Tac-Toe board on the screen."""
    screen.fill(GREY)  # Clear the screen
    # Draw vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, SCREEN_HEIGHT), 3)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, SCREEN_HEIGHT), 3)
    # Draw horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (SCREEN_WIDTH, SQUARE_SIZE), 3)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (SCREEN_WIDTH, 2 * SQUARE_SIZE), 3)

def draw_pieces():
    """Draws the X's and O's on the board."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell = board[row][col]
            if cell:
                if cell == 'X':
                    color = X_COLOR
                else:
                    color = O_COLOR
                text_surface = font.render(cell, True, color)
                text_rect = text_surface.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                screen.blit(text_surface, text_rect)

def check_win():
    """Checks if there is a winner."""
    global game_over, winner
    # Check rows and columns
    for i in range(BOARD_SIZE):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            game_over = True
            winner = board[i][0]
            return
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            game_over = True
            winner = board[0][i]
            return
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        winner = board[0][0]
        return
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        game_over = True
        winner = board[0][2]
        return
    # Check for a tie
    for row in board:
        if None in row:
            return  # Game is not over
    game_over = True  # If no empty spaces, it's a tie
    winner = None

def handle_click(pos):
    """Handles a mouse click on the board."""
    global player
    if not game_over:
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] is None:
            board[row][col] = player
            check_win()
            if not game_over:
                player = 'O' if player == 'X' else 'X'

def display_game_over():
    """Displays the game over screen."""
    if winner:
        text = f"Player {winner} wins!"
    else:
        text = "It's a tie!"
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def reset_game():
    """Resets the game to its initial state."""
    global board, player, game_over, winner
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]
    player = 'X'
    game_over = False
    winner = None

# --- Main Game Loop ---
def game_loop():
    """Main game loop."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        draw_board()
        draw_pieces()
        if game_over:
            display_game_over()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
