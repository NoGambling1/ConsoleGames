# (c) 2024 destinee shiina
# i reserve all my rights, this is my first actual contribution!!
#
# @orangejuiceplz told me to put all this for now lol
#
# contributors: feel free to add improvements or new features below this line


import curses
import random
import time
import locale
import os
import sys
import argparse


if sys.platform.startswith('win'):
    import ctypes
    from ctypes import wintypes


# -- orangejuiceplz here, just doing this nt based shit for her since she doesn't know this yet.
# -- okay, cool? - destinee


    # for windows based machiens only: console constants
    STD_OUTPUT_HANDLE = -11
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004


    # get the windows console handle
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
   
    # enable vt100 mode. this allows for terminal processing.


#   this should be all. i'll let you handle the rest from here dest.
#   thanks! <3 - destinee
    mode = wintypes.DWORD()
    ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode))
    mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    ctypes.windll.kernel32.SetConsoleMode(handle, mode)


class CMatrix:
    def __init__(self, val=-1, is_head=False):
        self.val = val
        self.is_head = is_head


def finish():
    curses.curs_set(1)
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    sys.exit(0)


def resize_screen(stdscr):
    global LINES, COLS, matrix, length, spaces, updates
    LINES, COLS = stdscr.getmaxyx()
    if LINES < 10:
        LINES = 10
    if COLS < 10:
        COLS = 10
   
    matrix = [[CMatrix() for _ in range(COLS)] for _ in range(LINES + 1)]
    length = [0] * COLS
    spaces = [0] * COLS
    updates = [0] * COLS


    for j in range(0, COLS, 2):
        spaces[j] = random.randint(1, LINES)
        length[j] = random.randint(3, LINES - 3)
        matrix[1][j].val = ' '
        updates[j] = random.randint(1, 3)


    stdscr.clear()
    stdscr.refresh()


def main(stdscr):
    global LINES, COLS, matrix, length, spaces, updates


    locale.setlocale(locale.LC_ALL, '')


    # the different arguments you can use; for example, -r -b -u 2!!!!
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', help='screensaver mode')
    parser.add_argument('-a', action='store_true', help='asynchronous scroll')
    parser.add_argument('-b', action='store_true', help='bold characters on')
    parser.add_argument('-B', action='store_true', help='all bold characters')
    parser.add_argument('-n', action='store_true', help='no bold characters')
    parser.add_argument('-u', type=int, default=4, help='screen update delay')
    parser.add_argument('-C', default='green', help='matrix color')
    parser.add_argument('-r', action='store_true', help='rainbow mode')
    parser.add_argument('-m', action='store_true', help='lambda mode')
    parser.add_argument('-k', action='store_true', help='characters change while scrolling')
    args = parser.parse_args()


    curses.curs_set(0)
    stdscr.timeout(0)


    # we can create the colours based on the os!!
    if curses.has_colors():
        curses.start_color()
        if curses.can_change_color():
            curses.use_default_colors()
            for i in range(8):
                curses.init_pair(i + 1, i, -1)
        else:
            for i in range(8):
                curses.init_pair(i + 1, i, curses.COLOR_BLACK)


    LINES, COLS = stdscr.getmaxyx()
    matrix = [[CMatrix() for _ in range(COLS)] for _ in range(LINES + 1)]
    length = [0] * COLS
    spaces = [0] * COLS
    updates = [0] * COLS


    randmin, randnum = 33, 90
   
    for j in range(0, COLS, 2):
        spaces[j] = random.randint(1, LINES)
        length[j] = random.randint(3, LINES - 3)
        matrix[1][j].val = ' '
        updates[j] = random.randint(1, 3)


    color_map = {
        'green': curses.COLOR_GREEN,
        'red': curses.COLOR_RED,
        'blue': curses.COLOR_BLUE,
        'white': curses.COLOR_WHITE,
        'yellow': curses.COLOR_YELLOW,
        'cyan': curses.COLOR_CYAN,
        'magenta': curses.COLOR_MAGENTA,
        'black': curses.COLOR_BLACK
    }
    mcolor = color_map.get(args.C.lower(), curses.COLOR_GREEN)


    # this is the main loop for the project. its the (somewhat?) the same thing as in the c version, just in python
    while True:
        for j in range(0, COLS, 2):
            if args.a or random.randint(1, 4) == 1:
                if matrix[0][j].val == -1 and matrix[1][j].val == ' ' and spaces[j] > 0:
                    spaces[j] -= 1
                elif matrix[0][j].val == -1 and matrix[1][j].val == ' ':
                    length[j] = random.randint(3, LINES - 3)
                    matrix[0][j].val = random.randint(randmin, randmin + randnum)
                    spaces[j] = random.randint(1, LINES)


                i = 0
                while i <= LINES:
                    while i <= LINES and (matrix[i][j].val == ' ' or matrix[i][j].val == -1):
                        i += 1
                    if i > LINES:
                        break


                    z = i
                    y = 0
                    while i <= LINES and matrix[i][j].val != ' ' and matrix[i][j].val != -1:
                        matrix[i][j].is_head = False
                        if args.k and random.randint(1, 8) == 1:
                            matrix[i][j].val = random.randint(randmin, randmin + randnum)
                        i += 1
                        y += 1


                    if i > LINES:
                        matrix[z][j].val = ' '
                        continue


                    matrix[i][j].val = random.randint(randmin, randmin + randnum)
                    matrix[i][j].is_head = True


                    if y > length[j]:
                        matrix[z][j].val = ' '
                        matrix[0][j].val = -1
                    i += 1


        # we iterate over it so we can properly draw the matrix
        for i in range(1, LINES + 1):
            for j in range(0, COLS, 2):
                stdscr.move(i - 1, j)
                if matrix[i][j].val == 0 or (matrix[i][j].is_head and not args.r):
                    stdscr.addch('&', curses.color_pair(curses.COLOR_WHITE + 1) | (curses.A_BOLD if args.b or args.B else 0))
                else:
                    if args.r:
                        mcolor = random.choice(list(color_map.values()))
                    if matrix[i][j].val == 1:
                        stdscr.addch('|', curses.color_pair(mcolor + 1) | (curses.A_BOLD if args.b or args.B else 0))
                    elif matrix[i][j].val == -1 or matrix[i][j].val == ' ':
                        stdscr.addch(' ')
                    elif args.m and matrix[i][j].val != ' ':
                        stdscr.addstr("λ", curses.color_pair(mcolor + 1) | (curses.A_BOLD if args.B or (args.b and matrix[i][j].val % 2 == 0) else 0))
                    else:
                        char = matrix[i][j].val if isinstance(matrix[i][j].val, str) else chr(matrix[i][j].val)
                        stdscr.addch(char, curses.color_pair(mcolor + 1) | (curses.A_BOLD if args.B or (args.b and matrix[i][j].val % 2 == 0) else 0))


        stdscr.refresh()
        time.sleep(args.u * 0.01)


        ch = stdscr.getch()
        if ch == ord('q'):
            break
        elif ch == curses.KEY_RESIZE:
            resize_screen(stdscr)


# i'm stealing this from you @orangejuiceplz

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    finally:
        if sys.platform.startswith('win'):
            os.system('cls')  
        else:
            os.system('clear')  

