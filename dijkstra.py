import pygame
from queue import PriorityQueue
from astar import reconstruct_path


def dijkstra(draw, grid, start, end):
    open_set = PriorityQueue()
    dist = {node: float("inf") for row in grid for node in row}
    came_from = {}
    visited = []
    dist[start] = 0

    open_set.put((0, start))

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        visited.append(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbour in current.neighbours:
            if dist[neighbour] > dist[current] + 1:
                dist[neighbour] = dist[current] + 1
                came_from[neighbour] = current
                open_set.put((dist[neighbour], neighbour))

                neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False
