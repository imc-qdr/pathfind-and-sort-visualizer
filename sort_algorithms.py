import pygame
import time
from cell import allow_quit


def v_bubble_sort(lst, w, screen, delay):
    delay = delay/100
    comparisons = 0
    swaps = 0
    font = pygame.font.Font('freesansbold.ttf', 15)
    for i in range(len(lst)):
        for j in range(len(lst)-i-1):
            comparisons += 1
            if lst[j] > lst[j+1]:
                time.sleep(delay)
                swaps += 1
                lst[j], lst[j+1] = lst[j+1], lst[j]
                screen.fill((0, 0, 0))
                x = 0
                text = font.render(f'comparisons: {comparisons}, swaps: {swaps}', True, (255, 255, 255), (0, 0, 0))
                for v in range(len(lst)):
                    color = (255, 255, 255)
                    if v == j+1:
                        color = (255, 0, 0)
                    elif v > len(lst)-i-1:
                        color = (0, 255, 0)
                    pygame.draw.rect(screen,
                                     color,
                                     (x, 600, w, -lst[v]))
                    screen.blit(text, (1, 1))
                    x += w+((1/4)*w*2)
            pygame.display.flip()
            allow_quit()
    return swaps, comparisons


class count_quick:
    def __init__(self):
        self.swaps = 0
        self.comparisons = 0
        self.pivots = []


def v_quick_sort(lst, w, screen, delay, left=0, right=None, first_rec=True):
    global count
    font = pygame.font.Font('freesansbold.ttf', 15)
    if first_rec:
        count = count_quick()
    if type(right) != int:
        right = len(lst)-1
    if left >= right:
        screen.fill((0, 0, 0))
        x = 0
        count.pivots = count.pivots + [left, right]
        text = font.render(f'comparisons: {count.comparisons}, swaps: {count.swaps}', True, (255, 255, 255), (0, 0, 0))
        for v in range(len(lst)):
            color = (255, 255, 255)
            if v in count.pivots:
                color = (0, 255, 0)
            screen.blit(text, (1, 1))
            pygame.draw.rect(screen, color, (x, 600, w, -lst[v]))
            x += w+((1/4)*w*2)
        time.sleep(delay/100)
        pygame.display.flip()
        return
    i = left
    j = right - 1
    pivot = lst[right]
    while i < j:
        while i < right and lst[i] < pivot:
            count.comparisons += 1
            i = i + 1
        while j > left and lst[j] >= pivot:
            count.comparisons += 1
            j = j - 1
        if i < j:
            count.comparisons += 1
            tmp = lst[i]
            lst[i] = lst[j]
            lst[j] = tmp
            count.swaps += 1
            screen.fill((0, 0, 0))
            x = 0
            text = font.render(f'comparisons: {count.comparisons}, swaps: {count.swaps}', True, (255, 255, 255),
                               (0, 0, 0))
            for v in range(len(lst)):
                color = (255, 255, 255)
                if v == j:
                    color = (255, 0, 0)
                elif v == i:
                    color = (0, 0, 255)
                elif v in count.pivots:
                    color = (0, 255, 0)
                pygame.draw.rect(screen, color, (x, 600, w, -lst[v]))
                screen.blit(text, (1, 1))
                x += w+((1/4)*w*2)
            allow_quit()
            time.sleep(delay/100)
            pygame.display.flip()
        else:
            count.pivots.append(i)
    if lst[i] > pivot:
        count.comparisons += 1
        count.swaps += 1
        tmp = lst[i]
        lst[i] = lst[right]
        lst[right] = tmp
    v_quick_sort(lst, w, screen, delay, left, i-1, False)
    v_quick_sort(lst, w, screen, delay, i+1, right, False)
    return count.swaps, count.comparisons


def v_insertion_sort(lst, w, screen, delay):
    delay = delay/100
    comparisons = 0
    swaps = 0
    font = pygame.font.Font('freesansbold.ttf', 16)
    for i in range(len(lst)):
        for j in range(i, -1, -1):
            x = 0
            screen.fill((0, 0, 0))
            if j != 0:
                comparisons += 1
                if lst[j-1] < lst[i] < lst[j]:
                    swaps += 1
                    lst.insert(j, lst.pop(i))
                    time.sleep(delay)
                    text = font.render(f'comparisons: {comparisons}, swaps: {swaps}', True, (255, 255, 255), (0, 0, 0))
                    for v in range(len(lst)):
                        color = (255, 255, 255)
                        if v == i+1:
                            color = (255, 0, 0)
                        if v == j:
                            color = (0, 255, 0)
                        pygame.draw.rect(screen,
                                         color,
                                         (x, 600, w, -lst[v]))
                        x += w+((1/4)*w*2)
                        screen.blit(text, (1, 1))
                    pygame.display.flip()
                    allow_quit()
                    break
            else:
                comparisons += 1
                if lst[i] < lst[j]:
                    swaps += 1
                    lst.insert(j, lst.pop(i))
                    time.sleep(delay)
                    text = font.render(f'comparisons: {comparisons}, swaps: {swaps}', True, (255, 255, 255), (0, 0, 0))
                    for v in range(len(lst)):
                        color = (255, 255, 255)
                        pygame.draw.rect(screen,
                                         color,
                                         (x, 600, w, -lst[v]))
                        x += w+((1/4)*w*2)
                        screen.blit(text, (1, 1))
                    pygame.display.flip()
                    allow_quit()
                    break
    return swaps, comparisons
