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
    mode = wintypes.DWORD()
    ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode))
    mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    ctypes.windll.kernel32.SetConsoleMode(handle, mode)

# ---------
# gonna use  __slots__ for memory efficiency (ik you don't know this so just leave it pls)
class CMatrix:
    __slots__ = ['val', 'is_head']
    def __init__(self, val=-1, is_head=False):
        self.val = val
        self.is_head = is_head
# ---------

def finish():
    try:
        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    except curses.error:
        pass  # ignore curses errors when finishing
    sys.exit(0)

# ---------
# optimizing by using list comprehension for initialization instead of what you had before
def resize_screen(stdscr):
    global LINES, COLS, matrix, length, spaces, updates
    try:
        LINES, COLS = stdscr.getmaxyx()
        LINES, COLS = max(LINES, 10), max(COLS, 10)
       
        matrix = [[CMatrix() for _ in range(COLS)] for _ in range(LINES + 1)]
        length = [random.randint(3, LINES - 3) for _ in range(COLS)]
        spaces = [random.randint(1, LINES) for _ in range(COLS)]
        updates = [random.randint(1, 3) for _ in range(COLS)]

        for j in range(0, COLS, 2):
            matrix[1][j].val = ' '

        stdscr.clear()
        stdscr.refresh()
    except curses.error:
        finish()  # exit smoothly if there's a curses error during resizing the windows!
# ---------

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        print("Warning: Failed to set locale. Using default.")

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
    args = parser.parse_args(args)

    curses.wrapper(run_matrix, args)

def run_matrix(stdscr, args):
    global LINES, COLS, matrix, length, spaces, updates

    try:
        curses.curs_set(0)
        stdscr.timeout(0)

        if curses.has_colors():
            curses.start_color()
            if curses.can_change_color():
                curses.use_default_colors()
                for i in range(8):
                    curses.init_pair(i + 1, i, -1)
            else:
                for i in range(8):
                    curses.init_pair(i + 1, i, curses.COLOR_BLACK)

        resize_screen(stdscr)

        randmin, randnum = 33, 90
       
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

        # ---------
        # we're gonna optimize this by precomputing some values hun <3
        update_delay = args.u * 0.01
        is_async = args.a
        is_rainbow = args.r
        is_lambda = args.m
        is_changing = args.k
        bold_style = curses.A_BOLD if args.b or args.B else 0
        # ---------

        while True:
            for j in range(0, COLS, 2):
                if is_async or random.randint(1, 4) == 1:
                    if matrix[0][j].val == -1 and matrix[1][j].val == ' ':
                        if spaces[j] > 0:
                            spaces[j] -= 1
                        else:
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
                            if is_changing and random.randint(1, 8) == 1:
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

            for i in range(1, LINES + 1):
                for j in range(0, COLS, 2):
                    try:
                        stdscr.move(i - 1, j)
                        cell = matrix[i][j]
                        if cell.val == 0 or (cell.is_head and not is_rainbow):
                            stdscr.addch('&', curses.color_pair(curses.COLOR_WHITE + 1) | bold_style)
                        else:
                            if is_rainbow:
                                mcolor = random.choice(list(color_map.values()))
                            if cell.val == 1:
                                stdscr.addch('|', curses.color_pair(mcolor + 1) | bold_style)
                            elif cell.val == -1 or cell.val == ' ':
                                stdscr.addch(' ')
                            elif is_lambda and cell.val != ' ':
                                stdscr.addstr("λ", curses.color_pair(mcolor + 1) | (bold_style if args.B or (args.b and cell.val % 2 == 0) else 0))
                            else:
                                char = cell.val if isinstance(cell.val, str) else chr(cell.val)
                                stdscr.addch(char, curses.color_pair(mcolor + 1) | (bold_style if args.B or (args.b and cell.val % 2 == 0) else 0))
                    except curses.error:
                        pass  # ignore curses errors when drawing these special characters! i will add jp characters soon too

            try:
                stdscr.refresh()
            except curses.error:
                pass  # ignoring refresh errors

            time.sleep(update_delay)

            try:
                ch = stdscr.getch()
                if ch == ord('q'):
                    break
                elif ch == curses.KEY_RESIZE:
                    resize_screen(stdscr)
            except curses.error:
                pass  # ignoring input errors
    except Exception as e:
        finish()
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        os.system('cls' if sys.platform.startswith('win') else 'clear')
        
# ---------

# did you think i did too much? 

# ----------
