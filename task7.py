import pygame
import random
import time
import sys

# Constants
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 20, 20
TILE_SIZE = WIDTH // COLS
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (66, 135, 245)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Maze Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Maze generation using Recursive Backtracking
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = []
    visited = set()

    def visit(r, c):
        maze[r][c] = 0
        visited.add((r, c))
        neighbors = [(r+2, c), (r-2, c), (r, c+2), (r, c-2)]
        random.shuffle(neighbors)
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                wall_r, wall_c = (r + nr) // 2, (c + nc) // 2
                maze[wall_r][wall_c] = 0
                visit(nr, nc)

    visit(0, 0)
    return maze

# Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, maze):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y
            return True
        return False

# Draw maze
def draw_maze(maze, player, goal, moves, start_time):
    screen.fill(BLACK)
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE if maze[r][c] == 0 else GREY
            pygame.draw.rect(screen, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, RED, (goal[0]*TILE_SIZE, goal[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Goal
    pygame.draw.rect(screen, BLUE, (player.x*TILE_SIZE, player.y*TILE_SIZE, TILE_SIZE, TILE_SIZE))  # Player
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, 30))
    elapsed = int(time.time() - start_time)
    screen.blit(font.render(f"Moves: {moves} | Time: {elapsed}s", True, BLACK), (10, 5))

# Game loop
def main():
    maze = generate_maze(ROWS, COLS)
    player = Player(0, 0)
    goal = (COLS - 1, ROWS - 1)
    moves = 0
    start_time = time.time()

    running = True
    won = False

    while running:
        clock.tick(FPS)
        draw_maze(maze, player, goal, moves, start_time)
        pygame.display.flip()

        if (player.x, player.y) == goal:
            won = True
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT]:
            moved = player.move(-1, 0, maze)
        if keys[pygame.K_RIGHT]:
            moved = player.move(1, 0, maze)
        if keys[pygame.K_UP]:
            moved = player.move(0, -1, maze)
        if keys[pygame.K_DOWN]:
            moved = player.move(0, 1, maze)
        if moved:
            moves += 1
            pygame.time.delay(100)

    # Game Over Screen
    end_text = "You Win!" if won else "Game Over"
    while True:
        screen.fill(BLACK)
        screen.blit(font.render(end_text, True, GREEN), (WIDTH//2 - 50, HEIGHT//2 - 30))
        screen.blit(font.render("Press R to Restart or Q to Quit", True, WHITE), (WIDTH//2 - 140, HEIGHT//2 + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
