from random import choice, randint
from path_finding_algs import *
from cell import *
import traceback


colors = {'white': (255, 255, 255),
          'green': (0, 255, 0,),
          'blue': (0, 0, 255),
          'yellow': (255, 255, 0),
          'black': (0, 0, 0),
          'woody brown': (179, 89, 0)}


def matrix(n):
    # function to draw a grid of n*n number of cells
    # the magic happens in the object cell and the function determines the size of window and passes the X Y coordinates
    pygame.init()
    screen = 600
    w = screen//n
    screen += 2*w
    screen = pygame.display.set_mode((screen, screen))
    pygame.display.set_caption('Qdr\'s maze generator')
    cells = list()
    y = 0
    for j in range(n):
        allow_quit()
        x = 0
        y += w
        for i in range(n):
            x += w
            square = cell(w)
            square.draw(screen, colors['white'], x, y)
            cells.append(square)
            pygame.display.flip()
    # draws two rects for the starting and finish cells
    pygame.draw.rect(screen, colors['yellow'], (cells[0].xy()[0]-(3*w/4),cells[0].xy()[1]-(3*w/4),w-(w/2),w-(w/2)))
    pygame.draw.rect(screen, colors['green'], (cells[-1].xy()[0]-(3*w/4),cells[-1].xy()[1]-(3*w/4),w-(w/2),w-(w/2)))
    return cells


def generate_maze(matrix):
    # generate the maze from the matrix. it's a randomized version of depth first search.
    w = matrix[0].w
    initial = choice(matrix)
    visited = list()
    queue = list()
    visited.append(initial)
    queue.append(initial)
    while len(queue) != 0:
        allow_quit()
        current_cell = queue.pop(randint(0, len(queue)-1))
        neighbors = list()
        possible_neighbors = directions(current_cell, w)
        for possible_neighbor in possible_neighbors:
            if possible_neighbor in matrix and possible_neighbor not in visited:
                neighbors.append(possible_neighbor)
        if len(neighbors) != 0:
            queue.append(current_cell)
            new_cell = choice(neighbors)
            new_cell = matrix[matrix.index(new_cell)]
            if new_cell == possible_neighbors[0]:
                current_cell.break_wall('r')
                new_cell.break_wall('l')
            elif new_cell == possible_neighbors[1]:
                current_cell.break_wall('l')
                new_cell.break_wall('r')
            elif new_cell == possible_neighbors[2]:
                current_cell.break_wall('b')
                new_cell.break_wall('t')
            else:
                current_cell.break_wall('t')
                new_cell.break_wall('b')
            visited.append(new_cell)
            queue.append(new_cell)
        pygame.display.flip()
    return matrix


if __name__ == '__main__':
    try:
        breadth_depth_first(generate_maze(matrix(10)), 1)
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)

