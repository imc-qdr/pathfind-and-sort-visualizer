import pygame


def allow_quit(end=False):
    # function that iterate over the events in pygame to allow the user to quit the visualization
    if end:
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
        return True
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True


class cell:
    # main class where the magic happens
    # it draws the cell, opens the walls, saves which walls are open, and backtrack to find the shortest path
    def __init__(self, w):
        self.w = w

    def draw(self, screen, color, x, y):
        self.screen = screen
        pygame.draw.line(screen, color, [x, y], [x + self.w, y])  # top wall of cell
        pygame.draw.line(screen, color, [x, y + self.w], [x + self.w, y + self.w])  # bottom wall of cell
        pygame.draw.line(screen, color, [x, y], [x, y + self.w])  # right wall of cell
        pygame.draw.line(screen, color, [x + self.w, y], [x + self.w, y + self.w])  # left wall of cell
        self.x = x + self.w
        self.y = y + self.w
        self.r_broken = False
        self.l_broken = False
        self.b_broken = False
        self.t_broken = False

    def break_wall(self, side):
        # method to break either left, right, top, or bottom wall
        if side == 'r':
            pygame.draw.line(self.screen, (0, 0, 0), [self.x, self.y-1], [self.x, self.y - self.w+1])
            self.r_broken = True
        elif side == 'l':
            pygame.draw.line(self.screen, (0, 0, 0), [self.x - self.w, self.y-1], [self.x - self.w, self.y - self.w+1])
            self.l_broken = True
        elif side == 't':
            pygame.draw.line(self.screen, (0, 0, 0), [self.x-1, self.y - self.w], [self.x - self.w+1, self.y - self.w])
            self.t_broken = True
        elif side == 'b':
            pygame.draw.line(self.screen, (0, 0, 0), [self.x-1, self.y], [self.x - self.w+1, self.y])
            self.b_broken = True

    def xy(self):
        # returns coordinates
        return self.x, self.y

    def add_path(self, parent):
        # method to backtrack the shortest path from start to end
        self.parent = parent

    def get_routes(self):
        # returns possible routes
        return self.r_broken, self.l_broken, self.b_broken, self.t_broken

    def __eq__(self, other):
        # override equality operator. two cells, or a cell and a tuple, are equal if they have the same coordinates.
        if type(other) == cell:
            if self.xy() == other.xy():
                return True
            return False
        elif type(other) == tuple or type(other) == list:
            if self.xy() == other:
                return True
            return False
        else:
            raise TypeError
