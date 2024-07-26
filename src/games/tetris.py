# experimental, will fix later
# I can tell you worked real hard to code all of this
# hotfix
import random
import time
import os
import sys

# const things
WIDTH = 10
HEIGHT = 20
EMPTY = ' '
BLOCK = '█'
GUIDE = '·'

# shapes (I, O, T, S, Z, J, L)
SHAPES = [[[1, 1, 1, 1]], [[1, 1], [1, 1]], [[0, 1, 0], [1, 1, 1]],
          [[0, 1, 1], [1, 1, 0]], [[1, 1, 0], [0, 1, 1]], [[1, 0, 0],
                                                           [1, 1, 1]],
          [[0, 0, 1], [1, 1, 1]]]

# Colors
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
    """
     otherwords, a tetris piece (yes, thats what they fucking call it)

    attrib:
        x (int): tetromino pos (x)
        y (int): tetromino pos (y)
        shape (List[List[int]]): shape of the tetromino
        color (str): color

    method:
        move(dx, dy): move piece by delta
        rotate(): 90 CW
    """

    def __init__(self, x, y, shape, color):
        """init new tetromino"""
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def move(self, dx, dy):
        """move tetromino by given deltas"""
        self.x += dx
        self.y += dy

    def rotate(self):
        """90 CW"""
        self.shape = list(zip(*self.shape[::-1]))


class TetrisGame:
    """
    logic

    attrib:
        board (List[List[str]]): game board
        score (int): score
        level (int): level
        lines_cleared (int): numLines cleared
        current_piece (Tetromino): current falling piece
        next_piece (Tetromino): next piece to fall
        game_over (bool): game ended? y/n

    Methods:
        new_piece(): new random tetromino
        valid_move(piece, dx=0, dy=0): valid move checker
        place_piece(piece): place piece
        remove_completed_lines(): rm completed liens and update socre
        update_score(lines_cleared): ONLY update score
        move_piece(dx, dy): move current piece along delta
        rotate_piece(): rotate piece
        drop_piece(): hard drop that shit
        step(): piece down or place new piece
        draw(): draw game state
    """

    def __init__(self):
        """init a new game"""
        self.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        """generate new random tetromino"""
        shape_index = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[shape_index]
        color = COLORS[shape_index]
        return Tetromino(WIDTH // 2 - len(shape[0]) // 2, 0, shape, color)

    def valid_move(self, piece, dx=0, dy=0):
        """movement validity checker"""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = piece.x + x + dx, piece.y + y + dy
                    if (new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT or
                        (new_y >= 0 and self.board[new_y][new_x] != EMPTY)):
                        return False
        return True

    def place_piece(self, piece):
        """place piece on board"""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[piece.y +
                               y][piece.x +
                                  x] = piece.color + BLOCK + RESET_COLOR

    def remove_completed_lines(self):
        """rm completed lines and return the numLines cleared"""
        lines_to_remove = [
            i for i, row in enumerate(self.board)
            if all(cell != EMPTY for cell in row)
        ]
        for line in lines_to_remove:
            del self.board[line]
            self.board.insert(0, [EMPTY for _ in range(WIDTH)])
        return len(lines_to_remove)

    def update_score(self, lines_cleared):
        """update score based on the numLines cleared"""
        self.lines_cleared += lines_cleared
        self.score += [0, 40, 100, 300, 1200][lines_cleared] * self.level
        self.level = self.lines_cleared // 10 + 1

    def move_piece(self, dx, dy):
        """move the current piece if the move is returned OK"""
        if self.valid_move(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True
        return False

    def rotate_piece(self):
        """rotate current piece if the rottation is returned OK"""
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if not self.valid_move(self.current_piece):
            self.current_piece.shape = original_shape

    def drop_piece(self):
        """hard drop that shit"""
        while self.move_piece(0, 1):
            pass

    def step(self):
        """piece down or place new piece"""
        if not self.move_piece(0, 1):
            self.place_piece(self.current_piece)
            lines_cleared = self.remove_completed_lines()
            self.update_score(lines_cleared)
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if not self.valid_move(self.current_piece):
                self.game_over = True

    def draw(self):
        """draw game state"""
        os.system('cls' if os.name == 'nt' else 'clear')

        #create temp board with the guidelines
        temp_board = [[
            GUIDE_COLOR + GUIDE +
            RESET_COLOR if x % 3 == 0 or y % 3 == 0 else EMPTY
            for x in range(WIDTH)
        ] for y in range(HEIGHT)]

        # add placed pieces to the temp board
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell != EMPTY:
                    temp_board[y][x] = cell

        # add current piece to the temp board
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    temp_board[self.current_piece.y + y][
                        self.current_piece.x +
                        x] = self.current_piece.color + BLOCK + RESET_COLOR

        # centre board like actual tetris
        terminal_width = os.get_terminal_size().columns
        left_padding = (terminal_width - (WIDTH * 2 + 2)) // 2

        print("\n" * 2)  # top padding for fullscreen terminal support
        print(" " * left_padding + "┌" + "─" * (WIDTH * 2) + "┐")
        for row in temp_board:
            print(" " * left_padding + "│" +
                  "".join(cell + (RESET_COLOR + ' ' if cell != EMPTY else ' ')
                          for cell in row) + "│")
        print(" " * left_padding + "└" + "─" * (WIDTH * 2) + "┘")

        # info display
        info = f"Score: {self.score}  Level: {self.level}  Lines: {self.lines_cleared}"
        print(" " * ((terminal_width - len(info)) // 2) + info)

        # following piece display (terrible, need to rework)
        print("\n" + " " * ((terminal_width - 11) // 2) + "Next piece:")
        next_piece_str = [
            "".join(self.next_piece.color + (BLOCK if cell else "  ") +
                    RESET_COLOR for cell in row)
            for row in self.next_piece.shape
        ]
        for row in next_piece_str:
            print(" " * ((terminal_width - len(row)) // 2) + row)

        # display controls
        controls = [
            "Controls:", "A/←: Move left", "D/→: Move right", "S/↓: Soft drop",
            "W/↑: Rotate", "Space: Hard drop", "Q: Quit"
        ]
        print("\n" + "\n".join(" " * ((terminal_width - len(line)) // 2) + line
                               for line in controls))


def get_input(timeout=0.1):
    """
    wait for key press and return action

    args:
        timeout (float): the max time to wait for a key press in seconds

    returns:
        str: the action mapped to the key or none if no key was pressed within the timeout period
    """
    if os.name == 'nt':  # window's computers
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
                    return {
                        '[A': 'w',
                        '[B': 's',
                        '[D': 'a',
                        '[C': 'd'
                    }[key[1:]]
                return key.lower()
            else:
                return None
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def play_game():
    """game loop"""
    game = TetrisGame()
    last_move_time = time.time()
    move_delay = 0.5

    print("tetris for dummies")
    print(
        "CONTROLS: \nA/←: Left, \nD/→: Right, \nS/↓: Soft drop, \nW/↑: Rotate, \nSpace: Hard drop, \nQ: Quit"
    )
    input("press 'Enter' to start...")

    while not game.game_over:
        game.draw()

        key = get_input()
        if key in ('a', 'd'):
            game.move_piece(-1 if key == 'a' else 1, 0)
        elif key == 's':
            game.move_piece(0, 1)
        elif key == 'w':
            game.rotate_piece()
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
