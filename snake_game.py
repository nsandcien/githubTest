import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
CELL_SIZE = 20

# Colors
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

# Frames per second controller
FPS = 10
clock = pygame.time.Clock()

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game for Erika!")

# Font for score display
font_style = pygame.font.SysFont(None, 35)


def message(msg, color, x, y):
    """Display a message on the screen."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [x, y])


def game_loop():
    # Initial snake position. The snake is represented as a list of [x, y] positions.
    snake_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
    snake_body = [list(snake_pos)]

    # Initial food position
    food_pos = [random.randrange(1, (WINDOW_WIDTH // CELL_SIZE)) * CELL_SIZE,
                random.randrange(1, (WINDOW_HEIGHT // CELL_SIZE)) * CELL_SIZE]
    food_spawn = True

    # Initial movement direction: [dx, dy]
    dx = 0
    dy = 0

    score = 0

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Control the snake with arrow keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -CELL_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = CELL_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -CELL_SIZE
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = CELL_SIZE

        # Update snake position
        snake_pos[0] += dx
        snake_pos[1] += dy

        # Check collision with walls
        if (snake_pos[0] < 0 or snake_pos[0] >= WINDOW_WIDTH or
                snake_pos[1] < 0 or snake_pos[1] >= WINDOW_HEIGHT):
            game_over = True

        # Update snake body
        snake_body.insert(0, list(snake_pos))

        # Check if snake has eaten the food, increase score and respawn food
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            # remove last segment of snake's tail
            snake_body.pop()

        if not food_spawn:
            food_pos = [
                random.randrange(1, WINDOW_WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(1, WINDOW_HEIGHT // CELL_SIZE) * CELL_SIZE,
            ]
            food_spawn = True

        # Check if snake collision with itself
        for segment in snake_body[1:]:
            if snake_pos == segment:
                game_over = True

        # Draw everything
        screen.fill(BLACK)

        # Draw snake with head in blue and body in green
        for i, pos in enumerate(snake_body):
            if i == 0:
                pygame.draw.rect(screen, pygame.Color(0, 0, 255), pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

        # Draw food
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

        # Display score
        message(f"Score: {score}", WHITE, 10, 10)

        pygame.display.update()

        clock.tick(FPS)

    # Game over screen
    screen.fill(BLACK)
    message("Game Over!", RED, WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 20)
    message(f"Final Score: {score}", WHITE, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()
