from sort_algorithms import *
from random import shuffle
import time


def visualize_sort(n, alg, delay):
    # generates the list and its visualization, take an algorithm as argument.
    pygame.init()
    screen = 600
    # width of the bar
    w = (screen/n)
    # the calculation inside is fit all bars in the screen with spaces between them
    screen = pygame.display.set_mode((screen+round(n*((1/4)*w*2)), screen))
    lst = shuffled_n_list(n)
    x = 0
    y = 600
    for i in range(n):
        pygame.draw.rect(screen, (255, 255, 255), (x, y, w, -lst[i]))
        time.sleep(0.009)
        pygame.display.flip()
        # the X coordinate of the next bar is the coordinate the last plus the width and a space between them
        x += w+((1/4)*w*2)
        if allow_quit():
            # I was getting a strange error from the OS that exits tkinter when I quit pygame.
            # returning from the function after quiting solved it
            return
    v = alg(lst, w, screen, delay)
    allow_quit(end=True)
    return v


def shuffled_n_list(n):
    # function that creates a shuffled list with n elements proportional to the size of the screen.
    lst = list(map(lambda x: x*600//n, list(range(1, n+1))))
    shuffle(lst)
    return lst


if __name__ == '__main__':
    print(visualize_sort(100, v_quick_sort, 1))
