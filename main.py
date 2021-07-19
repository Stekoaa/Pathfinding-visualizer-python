import pygame
import json
from astar import a_star
from dijkstra import dijkstra
from grid import draw, make_grid, get_clicked_position, display_failure


pygame.init()


with open('config.json') as config_file:
    data = json.load(config_file)


WIDTH = data["width"]
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Visualizer")
ROWS = data["ROWS"]


def main(win, width):
    grid = make_grid(ROWS, width)
    start = None
    end = None

    run = True
    started = False

    while run:
        draw(ROWS, WIDTH, WIN, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, width, ROWS)
                node = grid[row][col]

                if not start:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    node.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, width, ROWS)
                node = grid[row][col]

                node.reset()

                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    result = a_star(lambda: draw(ROWS, width, win, grid), grid, start, end)

                    if not result:
                        display_failure(WIN, WIDTH)

                    started = False
                if event.key == pygame.K_d and start and end:

                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    result = dijkstra(lambda: draw(ROWS, width, win, grid), grid, start, end)
                    started = False

                    if not result:
                        display_failure(WIN, WIDTH)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)
                    started = False

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
