import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 9, 9
CELL_SIZE = WIDTH // BOARD_COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200, 100)  # Adjust the alpha value for transparency (0-255)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Tic Tac Toe")

boards_won = []

# Function to check for a win in a board
def check_win(board):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:  # Check rows
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:  # Check columns
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != 0:  # Check diagonals
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0


# Function to draw the board lines and markers
def draw_lines(active_board):
    screen.fill(WHITE)  # Fill the background with white
    for i in range(1, BOARD_ROWS):
        if i % 3 == 0:
            pygame.draw.line(
                screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH
            )
            pygame.draw.line(
                screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH
            )
        else:
            pygame.draw.line(
                screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2
            )
            pygame.draw.line(
                screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2
            )

    # Drawing markers on click and greying out inactive boards
    for cell in clicked_cells:
        row, col, player = cell
        cell_center_x = col * CELL_SIZE + CELL_SIZE // 2
        cell_center_y = row * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 3  # Adjust the radius as needed
        if player == 1:
            pygame.draw.circle(screen, RED, (cell_center_x, cell_center_y), radius)
        else:
            pygame.draw.line(
                screen,
                BLUE,
                (cell_center_x - radius, cell_center_y - radius),
                (cell_center_x + radius, cell_center_y + radius),
                2,
            )
            pygame.draw.line(
                screen,
                BLUE,
                (cell_center_x - radius, cell_center_y + radius),
                (cell_center_x + radius, cell_center_y - radius),
                2,
            )

    # Check for wins in small boards and replace with larger marker
    for i in range(3):
        for j in range(3):
            board = [[0 for _ in range(3)] for _ in range(3)]
            for cell in clicked_cells:
                row, col, player = cell
                if (row // 3, col // 3) == (i, j):
                    board[row % 3][col % 3] = player
            winner = check_win(board)
            if winner != 0:
                rect = pygame.Rect(
                    j * CELL_SIZE * 3, i * CELL_SIZE * 3, CELL_SIZE * 3, CELL_SIZE * 3
                )
                pygame.draw.rect(screen, GREY, rect)  # Grey out the winning board
                if winner == 1:
                    pygame.draw.circle(
                        screen, RED, rect.center, CELL_SIZE, 5
                    )  # Draw circle for player 1
                    boards_won.append((i, j))
                else:
                    pygame.draw.line(
                        screen, BLUE, rect.topleft, rect.bottomright, 5
                    )  # Draw cross for player 2
                    pygame.draw.line(screen, BLUE, rect.bottomleft, rect.topright, 5)
                    boards_won.append((i, j))

    # Grey out inactive boards
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if (row // 3, col // 3) != active_board or cell_statuses[row][col] != 0:
                # Grey out the inactive boards or played cells
                grey_rect = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                grey_rect.fill(GREY)
                screen.blit(grey_rect, (col * CELL_SIZE, row * CELL_SIZE))


# Main game loop
running = True
clicked_cells = []  # To store clicked cells (row, col, player)
active_board = None  # Current active board
current_player = 1  # Player 1 starts

# Create a data structure to track cell statuses (0: empty, 1: player 1, 2: player 2)
cell_statuses = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

while running:
    draw_lines(active_board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        ):  # Left mouse button clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE
            print(f"Clicked cell: ({row}, {col})")

            if active_board is None or active_board == (row // 3, col // 3):
                # Check if the selected cell is already played
                if cell_statuses[row][col] == 0:
                    clicked_cells.append((row, col, current_player))
                    if (row % 3, col % 3) not in boards_won:
                        active_board = (row % 3, col % 3)
                    cell_statuses[row][
                        col
                    ] = current_player  # Mark the cell as played by the current player
                    # Alternate players
                    current_player = 1 if current_player == 2 else 2

    pygame.display.update()

pygame.quit()
sys.exit()
