from cell import *
import time


def directions(cell, w):
    possible_directions = ((cell.xy()[0] + w, cell.xy()[1]),
                           (cell.xy()[0] - w, cell.xy()[1]),
                           (cell.xy()[0], cell.xy()[1] + w),
                           (cell.xy()[0], cell.xy()[1] - w))
    return possible_directions


def breadth_depth_first(maze, delay, breadth=True):
    # the difference between depth first search and breadth first search is the first uses a queue
    # and the second uses a stack. so I made function for the both with a keyword parameter to choose which
    font = pygame.font.Font('freesansbold.ttf', 15)
    cells_scanned = 0
    screen = maze[0].screen
    start = maze[0]
    goal = maze[-1]
    w = maze[0].w
    queue = list()
    visited = list()
    queue.append(start)
    visited.append(start)
    while len(queue) != 0:
        n = 0
        if not breadth:
            n = -1
        current_cell = queue.pop(n)
        if current_cell == goal:
            while current_cell != start:
                current_cell = current_cell.parent
                if current_cell != start:
                    pygame.draw.circle(screen, (0, 155, 50),
                                       (current_cell.xy()[0]-(w-2)//2,
                                        current_cell.xy()[1]-(w-2)//2),
                                       (w//4))
                    pygame.display.flip()
                time.sleep(delay/200)
                allow_quit()
            allow_quit(end=True)
            return cells_scanned
        possible_routes = directions(current_cell, w)
        text = font.render(f'cells scanned: {cells_scanned}', True, (255, 255, 255), (0, 0, 0))
        for i in range(len(current_cell.get_routes())):    
            if current_cell.get_routes()[i]:
                new_cell = maze[maze.index(possible_routes[i])]
                if new_cell not in visited:
                    cells_scanned += 1
                    visited.append(new_cell)
                    if i == 0:
                        x, y = current_cell.xy()[0]-w+1, current_cell.xy()[1]-w+1
                        w1, w2 = (w*2)-2, w-2
                    elif i == 1:
                        x, y = new_cell.xy()[0]-w+1, new_cell.xy()[1]-w+1
                        w1, w2 = (w*2)-2, w-2
                    elif i == 2:
                        x, y = current_cell.xy()[0]-w+1, current_cell.xy()[1]-w+1
                        w1, w2 = w-2, (w*2)-2
                    else:
                        x, y = new_cell.xy()[0]-w+1, new_cell.xy()[1]-w+1
                        w1, w2 = w-2, (w*2)-2
                    time.sleep(delay/100)
                    if allow_quit():
                        return
                    if current_cell not in (start, goal) and new_cell not in (start, goal):
                        pygame.draw.rect(screen, (0, 0, 128), (x, y, w1, w2))
                    pygame.draw.rect(screen, (0, 0, 0), (1, 1, 150, 15))
                    screen.blit(text, (1, 1))
                    new_cell.add_path(current_cell)
                    queue.append(new_cell)
                    pygame.display.flip()


def wall_follower(maze, delay):
    # simple algorithm but was a bit difficult to code.
    # wall follower simply follows a wall until it reaches the end
    # the difficulty was in changes directions because right, left, top, bottom are relative to where you are facing
    font = pygame.font.Font('freesansbold.ttf', 15)
    screen = maze[0].screen
    w = maze[0].w
    start = maze[0]
    goal = maze[-1]
    current_cell = start
    last = None
    face = None
    image = pygame.image.load('me.png')
    image.convert()
    image = pygame.transform.scale(image, ((image.get_size()[0]*(w-2))//image.get_size()[1], w-2))
    cells_scanned = 0
    while current_cell != goal:
        cells_scanned += 1
        text = font.render(f'cells scanned: {cells_scanned}', True, (255, 255, 255), (0, 0, 0))
        possible_routes = directions(current_cell, w)
        if last is None:
            last = current_cell
            if current_cell.get_routes()[0]:
                face = 'r'
                current_cell = maze[maze.index(possible_routes[0])]
            elif current_cell.get_routes()[2]:
                face = 'b'
                current_cell = maze[maze.index(possible_routes[2])]
            current_cell.xy()
        else:
            last = current_cell
            if face == 'r':
                if current_cell.get_routes()[3]:
                    current_cell = maze[maze.index(possible_routes[3])]
                    face = 't'
                elif current_cell.get_routes()[0]:
                    current_cell = maze[maze.index(possible_routes[0])]
                else:
                    face = 'b'
            elif face == 'l':
                if current_cell.get_routes()[2]:
                    current_cell = maze[maze.index(possible_routes[2])]
                    face = 'b'
                elif current_cell.get_routes()[1]:
                    current_cell = maze[maze.index(possible_routes[1])]
                else:
                    face = 't'
            elif face == 't':
                if current_cell.get_routes()[1]:
                    current_cell = maze[maze.index(possible_routes[1])]
                    face = 'l'
                elif current_cell.get_routes()[3]:
                    current_cell = maze[maze.index(possible_routes[3])]
                else:
                    face = 'r'
            elif face == 'b':
                if current_cell.get_routes()[0]:
                    current_cell = maze[maze.index(possible_routes[0])]
                    face = 'r'
                elif current_cell.get_routes()[2]:
                    current_cell = maze[maze.index(possible_routes[2])]
                else:
                    face = 'l'
            screen.blit(image,(current_cell.xy()[0]-w+1+(w//5), current_cell.xy()[1]-w+1))
            if last != current_cell and last is not None:
                pygame.draw.rect(screen, (0, 0, 0),
                                 (last.xy()[0]-w+1,
                                  last.xy()[1]-w+1,
                                  w-1, w-1))
                pygame.draw.circle(screen, (255, 0, 0),
                                   (last.xy()[0]-(w-2)//2,
                                    last.xy()[1]-(w-2)//2),
                                   (w//4))
                pygame.draw.rect(screen, (0, 0, 0), (1, 1, 150, 15))
                screen.blit(text, (1, 1))
        time.sleep(delay/50)
        pygame.display.flip()
        allow_quit()
    allow_quit(end=True)
    return cells_scanned
