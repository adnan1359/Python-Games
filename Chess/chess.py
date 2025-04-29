import pygame
import sys

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE
WHITE = (240, 217, 181)  # Light beige
BLACK = (181, 136, 99)  # Darker beige
SELECTED_COLOR = (255, 255, 0, 128)  # Semi-transparent yellow
POSSIBLE_MOVE_COLOR = (0, 255, 0, 128)  # Semi-transparent green
RED = (255, 0, 0, 128)  # for invalid move
GREY = (128, 128, 128)

# --- Game Variables ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()

# Function to get the correct image name based on the piece string
def get_image_name(piece_string):
    """
    Returns the corresponding image name based on the piece string.
    For example, 'wQ' will return 'white_queen.png'.
    """
    if not piece_string:  #handle None case
        return None
    color = 'white' if piece_string[0] == 'w' else 'black'
    piece_type = piece_string[1]
    piece_name = ""
    if piece_type == 'R':
        piece_name = 'rook'
    elif piece_type == 'N':
        piece_name = 'knight'
    elif piece_type == 'B':
        piece_name = 'bishop'
    elif piece_type == 'Q':
        piece_name = 'queen'
    elif piece_type == 'K':
        piece_name = 'king'
    elif piece_type == 'P':
        piece_name = 'pawn'
    return f"{color}_{piece_name}.png"

# Load piece images (using a dictionary for easier access)
piece_images = {}
for row_prefix in ['w', 'b']:
    for piece_letter in ['R', 'N', 'B', 'Q', 'K', 'P']:
        piece_string = row_prefix + piece_letter
        image_name = get_image_name(piece_string)
        if image_name:
            try:
                piece_images[piece_string] = pygame.image.load(image_name)
                piece_images[piece_string] = pygame.transform.scale(piece_images[piece_string], (SQUARE_SIZE, SQUARE_SIZE))
            except pygame.error as e:
                print(f"Error loading image: {image_name} - {e}")
                # Handle the error, e.g., use a placeholder or exit the game
                sys.exit()

# Initial board setup (using None for empty squares)
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
]

selected_square = None  # (row, col) of the selected square
possible_moves = []  # List of (row, col) tuples for possible moves
turn = 'w'  # 'w' for white, 'b' for black
game_over = False
winner = None

# --- Helper Functions ---

def draw_board():
    """Draws the chessboard on the screen."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    """Draws the pieces on the board."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece:
                image_name = get_image_name(piece) #get image name
                if image_name:
                    screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_possible_moves(row, col):
    """Gets the possible moves for the piece at the given square."""
    piece = board[row][col]
    moves = []

    if piece is None:
        return []

    player = piece[0]  # 'w' or 'b'

    def is_valid_move(new_row, new_col):
        """Helper function to check if a move is within the board bounds."""
        return 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE

    def is_opponent(new_row, new_col, player):
        """Helper function to check if the square contains an opponent's piece."""
        target_piece = board[new_row][new_col]
        return target_piece is not None and target_piece[0] != player

    if piece[1] == 'P':  # Pawn
        direction = -1 if player == 'w' else 1  # White moves up, black moves down
        # One step forward
        new_row = row + direction
        if is_valid_move(new_row, col) and board[new_row][col] is None:
            moves.append((new_row, col))
        # Two steps forward from initial position
        if (row == 6 and player == 'w') or (row == 1 and player == 'b'):
            new_row = row + 2 * direction
            if is_valid_move(new_row, col) and board[new_row][col] is None and board[row + direction][col] is None:
                moves.append((new_row, col))
        # Capture move (diagonal)
        for new_col in [col - 1, col + 1]:
            new_row = row + direction
            if is_valid_move(new_row, new_col) and is_opponent(new_row, new_col, player):
                moves.append((new_row, new_col))

    elif piece[1] == 'R':  # Rook
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            for i in range(1, BOARD_SIZE):
                new_row, new_col = row + i * dr, col + i * dc
                if not is_valid_move(new_row, new_col):
                    break
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif is_opponent(new_row, new_col, player):
                    moves.append((new_row, new_col))
                    break  # Stop after capturing
                else:
                    break  # Stop at own piece

    elif piece[1] == 'N':  # Knight
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(new_row, new_col) and (board[new_row][new_col] is None or is_opponent(new_row, new_col, player)):
                moves.append((new_row, new_col))

    elif piece[1] == 'B':  # Bishop
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, BOARD_SIZE):
                new_row, new_col = row + i * dr, col + i * dc
                if not is_valid_move(new_row, new_col):
                    break
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif is_opponent(new_row, new_col, player):
                    moves.append((new_row, new_col))
                    break
                else:
                    break

    elif piece[1] == 'Q':  # Queen
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for i in range(1, BOARD_SIZE):
                new_row, new_col = row + i * dr, col + i * dc
                if not is_valid_move(new_row, new_col):
                    break
                if board[new_row][new_col] is None:
                    moves.append((new_row, new_col))
                elif is_opponent(new_row, new_col, player):
                    moves.append((new_row, new_col))
                    break
                else:
                    break

    elif piece[1] == 'K':  # King
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(new_row, new_col) and (board[new_row][new_col] is None or is_opponent(new_row, new_col, player)):
                moves.append((new_row, new_col))
    return moves

def draw_possible_moves():
    """Draws the possible moves on the board."""
    if selected_square:
        for row, col in possible_moves:
            pygame.draw.rect(screen, POSSIBLE_MOVE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_selected_square():
    """Draws the selected square."""
    if selected_square:
        row, col = selected_square
        pygame.draw.rect(screen, SELECTED_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def handle_click(pos):
    """Handles a mouse click on the board."""
    global selected_square, possible_moves, turn, game_over, winner
    col = pos[0] // SQUARE_SIZE
    row = pos[1] // SQUARE_SIZE

    if not game_over:
        if selected_square is None:
            # If no piece is selected, try to select the clicked square
            if board[row][col] and board[row][col][0] == turn:
                selected_square = (row, col)
                possible_moves = get_possible_moves(row, col)
        else:
            # If a piece is selected, try to move it
            target_square = (row, col)
            if target_square in possible_moves:
                #valid move
                board[row][col] = board[selected_square[0]][selected_square[1]]
                board[selected_square[0]][selected_square[1]] = None
                selected_square = None
                possible_moves = []
                # Check for game over (very simplified)
                if is_game_over(): #check mate
                    game_over = True
                    winner = turn
                else:
                    #switch turn
                    turn = 'b' if turn == 'w' else 'w'
            elif board[row][col] and board[row][col][0] == turn:
                #same player, different piece
                selected_square = (row, col)
                possible_moves = get_possible_moves(row, col)
            else:
                #invalid move
                selected_square = None
                possible_moves = []

def is_game_over():
    """
    Checks if the game is over (very simplified check for checkmate).
    It checks if the current player has any legal moves.  If not, the game is over.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] and board[row][col][0] == turn:
                if get_possible_moves(row, col):
                    return False  # Found a legal move, game is not over
    return True  # No legal moves found, game is over



def display_game_over():
    """Displays the game over screen."""
    font = pygame.font.Font(None, 48)
    text = f"Game Over! {winner.upper()} wins!"
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()



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

        screen.fill(GREY)  # Clear the screen
        draw_board()
        draw_selected_square()
        draw_possible_moves()
        draw_pieces()
        if game_over:
            display_game_over()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
