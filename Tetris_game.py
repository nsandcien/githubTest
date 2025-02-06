import pygame, sys, random

pygame.init()

# Global variables
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30  # Size of single tetris block
COLUMN_COUNT = SCREEN_WIDTH // BLOCK_SIZE  # 10
ROW_COUNT = SCREEN_HEIGHT // BLOCK_SIZE  # 20

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Shapes formats in 4x4 grid format; each shape is a list of rotations.
SHAPES = {
    'S': [
        ['.....',
         '.....',
         '..00.',
         '.00..',
         '.....'],
        ['.....',
         '..0..',
         '..00.',
         '...0.',
         '.....']
    ],
    'Z': [
        ['.....',
         '.....',
         '.00..',
         '..00.',
         '.....'],
        ['.....',
         '..0..',
         '.00..',
         '.0...',
         '.....']
    ],
    'I': [
        ['..0..',
         '..0..',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '0000.',
         '.....',
         '.....',
         '.....']
    ],
    'O': [
        ['.....',
         '.....',
         '.00..',
         '.00..',
         '.....']
    ],
    'J': [
        ['.....',
         '.0...',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..00.',
         '..0..',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '...0.',
         '.....'],
        ['.....',
         '..0..',
         '..0..',
         '.00..',
         '.....']
    ],
    'L': [
        ['.....',
         '...0.',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..0..',
         '..0..',
         '..00.',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '.0...',
         '.....'],
        ['.....',
         '.00..',
         '..0..',
         '..0..',
         '.....']
    ],
    'T': [
        ['.....',
         '..0..',
         '.000.',
         '.....',
         '.....'],
        ['.....',
         '..0..',
         '..00.',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '.000.',
         '..0..',
         '.....'],
        ['.....',
         '..0..',
         '.00..',
         '..0..',
         '.....']
    ]
}

SHAPE_COLORS = {
    'S': GREEN,
    'Z': RED,
    'I': CYAN,
    'O': YELLOW,
    'J': BLUE,
    'L': ORANGE,
    'T': PURPLE
}


class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[shape]
        self.rotation = 0  # integer index from 0 to len(shape rotations)-1


def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
    # Fill grid with locked positions
    for (col, row), color in locked_positions.items():
        if row >= 0:
            grid[row][col] = color
    return grid


def convert_shape_format(piece):
    positions = []
    format = SHAPES[piece.shape][piece.rotation % len(SHAPES[piece.shape])]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 2))
    return positions


def valid_space(piece, grid):
    accepted_positions = [[(j, i) for j in range(COLUMN_COUNT) if grid[i][j] == BLACK] for i in range(ROW_COUNT)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(locked_positions):
    for (col, row) in locked_positions:
        if row < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(list(SHAPES.keys())))


def draw_grid(grid, surface):
    # Draw grid lines for better visualization
    for i in range(ROW_COUNT):
        pygame.draw.line(surface, WHITE, (0, i * BLOCK_SIZE), (SCREEN_WIDTH, i * BLOCK_SIZE))
    for j in range(COLUMN_COUNT):
        pygame.draw.line(surface, WHITE, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, SCREEN_HEIGHT))


def clear_rows(grid, locked):
    cleared = 0
    for i in range(ROW_COUNT - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            cleared += 1
            # Remove positions from locked
            for j in range(COLUMN_COUNT):
                try:
                    del locked[(j, i)]
                except:
                    continue
            # Shift every row above down
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                col, row_num = key
                if row_num < i:
                    newKey = (col, row_num + 1)
                    locked[newKey] = locked.pop(key)
    return cleared


def draw_window(surface, grid, score=0):
    surface.fill(BLACK)
    # Draw title
    font = pygame.font.SysFont("comicsans", 40)
    label = font.render("Tetris", True, WHITE)
    surface.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 10))
    # Draw score
    font_small = pygame.font.SysFont("comicsans", 25)
    score_label = font_small.render("Score: " + str(score), True, WHITE)
    surface.blit(score_label, (10, SCREEN_HEIGHT - 40))
    # Draw grid blocks
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            pygame.draw.rect(surface, grid[i][j],
                             (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    # Draw grid lines
    draw_grid(grid, surface)
    pygame.display.update()


def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5  # seconds before piece falls one block

    score = 0

    while True:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(SHAPES[current_piece.shape])
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(SHAPES[current_piece.shape])

        shape_pos = convert_shape_format(current_piece)

        # Draw current piece on the grid
        for pos in shape_pos:
            x, y = pos
            if y > -1:
                grid[y][x] = current_piece.color

        # Once piece hit the ground
        if change_piece:
            for pos in shape_pos:
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # Clear full rows and update score
            cleared = clear_rows(grid, locked_positions)
            if cleared > 0:
                score += cleared * 10

        draw_window(screen, grid, score)
        if check_lost(locked_positions):
            font = pygame.font.SysFont("comicsans", 50)
            label = font.render("GAME OVER", True, WHITE)
            screen.blit(label,
                        (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - label.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            break


if __name__ == "__main__":
    main()
