
import pygame
import sys
import copy
import random
import time

sys.setrecursionlimit(10000000)

WIDTH, HEIGHT = 500, 500
GRID_SIZE = 10
n = 10
cols = 10
CELL_SIZE = WIDTH // GRID_SIZE
BALL_COLORS = {
    0: (0, 0, 0),  # Black for empty cells
    1: (255, 0, 0),  # Red
    2: (0, 255, 0),  # Green
    3: (0, 0, 255), # Blue
    4: (255, 255, 0),  # Yellow
    5: (255, 165, 0),  # Orange
    6: (128, 0, 128),  #Purple
    7: (165, 42, 42),  #Brown
    8: (255, 0, 255),  #Magenta
    9: (0, 255, 255),  #Cyan
    10: (128, 128, 128),  #Grey
    100: (255, 255, 255)  # White Glaze
}
FPS = 60
K = 3  # Minimum size of group to clear
k = K
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Fusion")
clock = pygame.time.Clock()


def initialize_grid(n, cols):
    return [[random.randint(1, 10) for _ in range(cols)] for _ in range(n)]


def apply_gravity(grid, n):
    for j in range(cols):
        top = n - 1;
        bottom = n - 1
        while top >= 0:
            while top >= 0 and grid[top][j] == 0: top -= 1
            if top >= 0:
                grid[bottom][j] = grid[top][j]
                top -= 1;
                bottom -= 1
        while bottom >= 0:
            grid[bottom][j] = 0
            bottom -= 1
    return


def draw_grid(grid):
    screen.fill((0, 0, 0))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = BALL_COLORS[grid[i][j]]
            pygame.draw.circle(screen, color, (j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2),
                               CELL_SIZE // 3)
    pygame.display.flip()


grid = initialize_grid(n, GRID_SIZE)
selected = None
for row in grid:
    print(*row)
print()


def swap_balls(grid, pos1, pos2):       # Swap without animation
    i1, j1 = pos1
    i2, j2 = pos2
    grid[i1][j1], grid[i2][j2] = grid[i2][j2], grid[i1][j1]

def animate_swap(screen, grid, pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2

    x1, y1 = c1 * CELL_SIZE + CELL_SIZE // 2, r1 * CELL_SIZE + CELL_SIZE // 2
    x2, y2 = c2 * CELL_SIZE + CELL_SIZE // 2, r2 * CELL_SIZE + CELL_SIZE // 2

    steps = 20  # Number of frames for the animation
    dx, dy = (x2 - x1) / steps, (y2 - y1) / steps

    ball1_color = BALL_COLORS[grid[r1][c1]]
    ball2_color = BALL_COLORS[grid[r2][c2]]
    temp1, temp2 = grid[r1][c1], grid[r2][c2]
    grid[r1][c1], grid[r2][c2] = 0, 0
    for i in range(steps):
        screen.fill((0, 0, 0))
        draw_grid(grid)
        pygame.draw.circle(screen, ball1_color, (int(x1 + dx * i), int(y1 + dy * i)), CELL_SIZE // 3)
        pygame.draw.circle(screen, ball2_color, (int(x2 - dx * i), int(y2 - dy * i)), CELL_SIZE // 3)
        pygame.display.flip()
        pygame.time.delay(10)

    # Final positions
    grid[r1][c1], grid[r2][c2] = temp2, temp1


visited = [[0 for i in range(cols)] for j in range(n)]
di = [1, -1, 0, 0]
dj = [0, 0, 1, -1]
cc_num = 0
path = []
white_balls = []

def dfs(i, j):
    global cc_num
    visited[i][j] = 1
    cc_num += 1
    path.append([i, j])
    for _ in range(4):
        ni, nj = i + di[_], j + dj[_]
        if 0 <= ni < n and 0 <= nj < cols and grid[ni][nj] == grid[i][j]:
            if not visited[ni][nj]:
                dfs(ni, nj)


def solve():
    global cc_num, k, n, path, white_balls
    old_grid = copy.deepcopy(grid)
    for i in range(n):
        for j in range(cols):
            if grid[i][j] != 0:
                if not visited[i][j]:
                    cc_num = 0
                    path = []
                    dfs(i, j)

                if cc_num >= k:

                    for idx in path:
                        grid[idx[0]][idx[1]] = 100
                    draw_grid(grid)
                    time.sleep(0.2)
                    white_balls.extend(path)
                    '''
                    for idx in path:
                        grid[idx[0]][idx[1]] = 0
                    draw_grid(grid)
                    time.sleep(0.1)
                    '''
    for idx in white_balls:
        grid[idx[0]][idx[1]] = 0
    draw_grid(grid)
    #time.sleep(0.1)
    apply_gravity(grid, n)

    draw_grid(grid)
    #time.sleep(0.2)

    flag = 0
    for i in range(n):
        for j in range(cols):
            if grid[i][j] != old_grid[i][j]:
                flag = 1
                break
    return flag


while True:
    draw_grid(grid)
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))       ###############
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            i, j = y // CELL_SIZE, x // CELL_SIZE
            if selected:
                ni, nj = selected
                if abs(ni - i) + abs(nj - j) == 1:
                    animate_swap(screen, grid, (ni, nj), (i, j))
                    time.sleep(0.1)
                    draw_grid(grid)
                    flag = 1
                    while flag:
                        visited = [[0 for i in range(cols)] for j in range(n)]
                        white_balls = []
                        flag = solve()
                        #time.sleep(0.2)
                        draw_grid(grid)
                selected = None
            else:
                selected = (i, j)
    clock.tick(FPS)

