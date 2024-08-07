import curses
import random
import time


class Fish:

    def __init__(self, y, x, direction):
        self.y = y
        self.x = x
        self.direction = direction

    def move(self):
        if self.direction == 'right':
            self.x += 1
        else:
            self.x -= 1


class Bubble:

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def move(self):
        self.y -= 1


def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(100)

    fishes = [
        Fish(random.randint(1, sh - 2), random.randint(1, sw - 2),
             random.choice(['left', 'right'])) for _ in range(5)
    ]
    bubbles = []

    while True:
        w.clear()
        
        w.border()

        # drawing and moving each fishie
        for fish in fishes:
            fish.move()
            if fish.x <= 0 or fish.x >= sw - 3:  
                fish.direction = 'right' if fish.direction == 'left' else 'left'
            fish_sprite = '><>' if fish.direction == 'right' else '<><'
            w.addstr(fish.y, fish.x,
                     fish_sprite)  # avoiding a type error by using it like this

        for bubble in bubbles:
            bubble.move()
            if bubble.y > 0:
                w.addch(bubble.y, bubble.x, 'o')

        # make new bubbles
        if random.random() < 0.1:
            bubbles.append(Bubble(sh - 1, random.randint(1, sw - 2)))

        # remove bubbles that have reached the top
        bubbles = [b for b in bubbles if b.y > 0]

        w.refresh()
        time.sleep(0.1)

        if w.getch() == ord('q'):
            break


curses.wrapper(main)
