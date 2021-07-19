import pygame
import colors
import time

pygame.init()

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.color = colors.WHITE
        self.neighbours = []

    def get_pos(self):
        return self.row, self.col

    def is_start(self):
        return self.color == colors.ORANGE

    def is_end(self):
        return self.color == colors.TURQUOISE

    def is_barrier(self):
        return self.color == colors.BLACK

    def is_open(self):
        return self.color == colors.GREEN

    def is_closed(self):
        return self.color == colors.RED

    def reset(self):
        self.color = colors.WHITE

    def make_start(self):
        self.color = colors.ORANGE

    def make_end(self):
        self.color = colors.TURQUOISE

    def make_barrier(self):
        self.color = colors.BLACK

    def make_path(self):
        self.color = colors.PURPLE

    def make_open(self):
        self.color = colors.GREEN

    def make_closed(self):
        self.color = colors.RED

    def update_neighbours(self, grid):
        self.neighbours = []

        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.col])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col - 1])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbours.append(grid[self.row][self.col + 1])

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False


TEXT_FONT = pygame.font.SysFont('comicsans', 40)
TEXT = TEXT_FONT.render("End node is not reachable from the start node", True, (0, 0, 0))


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(rows, width, win):

    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, colors.GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, colors.GREY, (j * gap, 0), (j * gap, width))


def draw(rows, width, win, grid):
    win.fill(colors.WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(rows, width, win)
    pygame.display.update()


def get_clicked_position(pos, width, rows):
    gap = width // rows
    row = pos[0] // gap
    col = pos[1] // gap

    return row, col


def display_failure(WIN, WIDTH):
    WIN.blit(TEXT, (WIDTH // 10, WIDTH // 2))
    pygame.display.update()
    time.sleep(2.0)