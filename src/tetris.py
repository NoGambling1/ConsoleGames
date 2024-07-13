# experimental, will fix later
# I can tell you worked real hard to code all of this
import random
import time
import os
import sys
import keyboard
# const things
WIDTH = 10
HEIGHT = 20
EMPTY = ' '
BLOCK = '█'
GUIDE = '·'

# shapes (I, O, T, S, Z, J, L)
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

# colors
COLORS = [
    '\033[96m',  # cyan (I)
    '\033[93m',  # yellow (O)
    '\033[95m',  # magenta (T)
    '\033[92m',  # green (S)
    '\033[91m',  # red (Z)
    '\033[94m',  # blue (J)
    '\033[97m',  # white (L)
]

RESET_COLOR = '\033[0m'
GUIDE_COLOR = '\033[90m'  # dark gray

class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class TetrisGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        shape_index = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[shape_index]
        color = COLORS[shape_index]
        return Tetromino(WIDTH // 2 - len(shape[0]) // 2, 0, shape, color)

    def valid_move(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = piece.x + x + dx, piece.y + y + dy
                    if (new_x < 0 or new_x >= WIDTH or
                        new_y >= HEIGHT or
                        (new_y >= 0 and self.board[new_y][new_x] != EMPTY)):
                        return False
        return True

    def place_piece(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[piece.y + y][piece.x + x] = piece.color + BLOCK + RESET_COLOR

    def remove_completed_lines(self):
        lines_to_remove = [i for i, row in enumerate(self.board) if all(cell != EMPTY for cell in row)]
        for line in lines_to_remove:
            del self.board[line]
            self.board.insert(0, [EMPTY for _ in range(WIDTH)])
        return len(lines_to_remove)

    def update_score(self, lines_cleared):
        self.lines_cleared += lines_cleared
        self.score += [0, 40, 100, 300, 1200][lines_cleared] * self.level
        self.level = self.lines_cleared // 10 + 1

    def move_piece(self, dx, dy):
        if self.valid_move(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True
        return False

    def rotate_piece(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if not self.valid_move(self.current_piece):
            self.current_piece.shape = original_shape

    def drop_piece(self):
        while self.move_piece(0, 1):
            pass

    def step(self):
        if not self.move_piece(0, 1):
            self.place_piece(self.current_piece)
            lines_cleared = self.remove_completed_lines()
            self.update_score(lines_cleared)
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if not self.valid_move(self.current_piece):
                self.game_over = True

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # create temp board with the guidelines
        temp_board = [[GUIDE_COLOR + GUIDE + RESET_COLOR if x % 3 == 0 or y % 3 == 0 else EMPTY 
                       for x in range(WIDTH)] for y in range(HEIGHT)]
        
        # add placed pieces to the temp board
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell != EMPTY:
                    temp_board[y][x] = cell

        # add current piece to the temp board
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    temp_board[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color + BLOCK + RESET_COLOR

        # centre board like actual tetris
        terminal_width = os.get_terminal_size().columns
        left_padding = (terminal_width - (WIDTH * 2 + 2)) // 2

        print("\n" * 2)  #  top padding for fullscreen terminal support
        print(" " * left_padding + "┌" + "─" * (WIDTH * 2) + "┐")
        for row in temp_board:
            print(" " * left_padding + "│" + "".join(cell + (RESET_COLOR + ' ' if cell != EMPTY else ' ') for cell in row) + "│")
        print(" " * left_padding + "└" + "─" * (WIDTH * 2) + "┘")

        # game info display
        info = f"score: {self.score}  lvl: {self.level}  lines: {self.lines_cleared}"
        print(" " * ((terminal_width - len(info)) // 2) + info)

        # next piece (VERY EXPERIMENTAL)
        print("\n                                                        next piece:")
        next_piece_str = ["".join(self.next_piece.color + (BLOCK if cell else "  ") + RESET_COLOR for cell in row) for row in self.next_piece.shape]
        for row in next_piece_str:
            print(" " * ((terminal_width - len(row)) // 2) + row )

        # display controls
        controls = [
            "controls:",
            "A/←: move left",
            "D/→: move right",
            "S/↓: soft drop",
            "W/↑: rotate",
            "Space: hard drop",
            "Q: quit"
        ]
        print("\n" + "\n".join(" " * ((terminal_width - len(line)) // 2) + line for line in controls))

def get_input(timeout=0.1):
    if os.name == 'nt':  # windows machines
        import msvcrt
        start_time = time.time()
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':  # arrow keys
                    key = msvcrt.getch()
                    return {b'H': 'w', b'P': 's', b'K': 'a', b'M': 'd'}[key]
                return key.decode('utf-8').lower()
            if time.time() - start_time > timeout:
                return None
    else:  # unix systems (Linux, MacOS)
        import termios
        import tty
        import select
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if rlist:
                key = sys.stdin.read(1)
                if key == '\x1b':  # special key prefix
                    key += sys.stdin.read(2)
                    return {'[A': 'w', '[B': 's', '[D': 'a', '[C': 'd'}[key[1:]]
                return key.lower()
            else:
                return None
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def play_game():
    game = TetrisGame()
    last_move_time = time.time()
    move_delay = 0.5

    print("tetris")
    print("CONTROLS: \nA/←: left, \nD/→: right, \nS/↓: soft drop, \nW/↑: rotate, \nSpace: hard drop, \nQ: quit")
    input("press 'Enter' to start...")

    while not game.game_over:
        game.draw()

        key = get_input()
        if key in ('a', 'd'):
            game.move_piece(-1 if key == 'a' else 1, 0)
        elif keyboard.is_pressed('left'): game.move_piece(-1, 0); time.sleep(0.1)
        elif keyboard.is_pressed('right'): game.move_piece(1, 0); time.sleep(0.1)

        elif key == 's' or keyboard.is_pressed('down'):
            game.move_piece(0, 1)
            time.sleep(0.1)
        elif key == 'w' or keyboard.is_pressed('up'):
            game.rotate_piece()
            time.sleep(0.1)
        elif key == ' ':
            game.drop_piece()
            
        elif key == 'q':
            break

        if time.time() - last_move_time > move_delay:
            game.step()
            last_move_time = time.time()

        move_delay = max(0.1, 0.5 - 0.05 * (game.level - 1))

    game.draw()
    print("game over")
    print(f"final score: {game.score}")
    input("press 'Enter' to return to the main menu...")

if __name__ == "__main__":
    play_game()