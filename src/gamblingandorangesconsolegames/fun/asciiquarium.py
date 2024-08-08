import curses
import random
import time
import os

class Fish:

    def __init__(self, y, x, direction, species):
        self.y = y
        self.x = x
        self.direction = direction
        self.species = species
        self.sprites = {
            'small': ['><>', '<><'],
            'medium': ['>==>', '<==<'],
            'large': ['>===>', '<===<'],
            'shark': [')(>', '<()']
        }

    def move(self):
        if self.direction == 'right':
            self.x += 1
        else:
            self.x -= 1

        # vertical movement
        if random.random() < 0.1:
            self.y += random.choice([-1, 1])

    def draw(self, window, color):
        sprite = self.sprites[self.species][0 if self.direction ==
                                            'right' else 1]
        window.addstr(self.y, self.x, sprite, color)


class Bubble:

    def __init__(self, y, x, size):
        self.y = y
        self.x = x
        self.size = size
        self.chars = {'small': '.', 'medium': 'o', 'large': 'O'}

    def move(self):
        self.y -= 1
        if random.random() < 0.2:
            self.x += random.choice([-1, 0, 1])

    def draw(self, window):
        window.addch(self.y, self.x, self.chars[self.size])


class Seaweed:

    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.animation_frame = 0

    def draw(self, window, sh, color):
        chars = '~^'
        for i in range(self.height):
            char = chars[(i + self.animation_frame) % 2]
            window.addch(sh - 2 - i, self.x, char, color)
        self.animation_frame = (self.animation_frame + 1) % 2


class TreasureChest:

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def draw(self, window, color):
        window.addstr(self.y, self.x, '£', color)

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(100)

    fishes = [
        Fish(random.randint(1, sh - 2), random.randint(1, sw - 2),
             random.choice(['left', 'right']),
             random.choice(['small', 'medium', 'large'])) for _ in range(10)
    ]
    fishes.append(
        Fish(random.randint(1, sh - 2), random.randint(1, sw - 2),
             random.choice(['left', 'right']), 'shark'))

    bubbles = []
    seaweeds = [Seaweed(x, random.randint(2, 5)) for x in range(2, sw - 2, 4)]
    treasure = TreasureChest(sh - 2, random.randint(2, sw - 2))

    day_cycle = 0
    max_cycle = 1000

    while True:
        w.clear()

        # day/night cycle
        day_cycle = (day_cycle + 1) % max_cycle
        if day_cycle < max_cycle // 2:
            bg_color = curses.color_pair(14)  # light blue - day
        else:
            bg_color = curses.color_pair(17)  # dark blue - night

        # draw water surface
        w.addstr(0, 0, '~' * (sw - 1), bg_color)

        # draw and move fishies
        for fish in fishes:
            fish.move()
            if fish.x <= 0 or fish.x >= sw - len(
                    fish.sprites[fish.species][0]):
                fish.direction = 'right' if fish.direction == 'left' else 'left'
            if fish.y <= 1:
                fish.y = 1
            elif fish.y >= sh - 2:
                fish.y = sh - 2
            fish.draw(w, bg_color)

        # draw and move bubbles
        for bubble in bubbles:
            bubble.move()
            if bubble.y > 0 and 0 < bubble.x < sw - 1:
                bubble.draw(w)

        # make new bubbles
        if random.random() < 0.1:
            bubbles.append(
                Bubble(sh - 1, random.randint(1, sw - 2),
                       random.choice(['small', 'medium', 'large'])))

        # remove bubbles that have reached the top
        bubbles = [b for b in bubbles if b.y > 0]

        # draw seaweed
        for seaweed in seaweeds:
            seaweed.draw(w, sh, curses.color_pair(2))  # green color

        # draw treasure chest
        treasure.draw(w, curses.color_pair(3))  # yellow color

        # draw sand at the bottom (avoiding the last cell in the terminal to prevent errors)
        w.addstr(sh - 1, 0, '.' * (sw - 1),
                 curses.color_pair(3))  

        w.refresh()
        time.sleep(0.1)

        if w.getch() == ord('q'):
            break


curses.wrapper(main)
