import random
import time
import os
import sys
import select

# const
WIDTH = 30
HEIGHT = 20
SNAKE_CHAR = "■"
FRUIT_CHAR = "●"
EMPTY_CHAR = "·"

# colour
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


class SnakeGame:

    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.snake = [[4, 5], [3, 5], [2, 5]]
        self.direction = "RIGHT"
        self.fruit = self.spawn_fruit()
        self.score = 0
        self.game_over = False
        self.buffer = ""

    def spawn_fruit(self):
        while True:
            pos = [
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            ]
            if pos not in self.snake:
                return pos

    def move_snake(self):
        head = self.snake[0].copy()
        if self.direction == "UP":
            head[1] -= 1
        elif self.direction == "DOWN":
            head[1] += 1
        elif self.direction == "LEFT":
            head[0] -= 1
        elif self.direction == "RIGHT":
            head[0] += 1

        if (head[0] < 0 or head[0] >= self.width or head[1] < 0
                or head[1] >= self.height or head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, head)

        if head == self.fruit:
            self.score += 1
            self.fruit = self.spawn_fruit()
        else:
            self.snake.pop()

    def draw(self):
        self.buffer = ""
        terminal_width = os.get_terminal_size().columns
        left_padding = (terminal_width - (self.width * 2 + 2)) // 2

        self.buffer += "\033[H"  # Move cursor to home position
        self.buffer += "\n" * 2  # automatic padding for all terminals
        self.buffer += " " * left_padding + "┌" + "─" * (self.width *
                                                         2) + "┐\n"

        for y in range(self.height):
            self.buffer += " " * left_padding + "│"
            for x in range(self.width):
                char = EMPTY_CHAR
                if [x, y] == self.snake[0]:  # head
                    char = GREEN + SNAKE_CHAR + RESET
                elif [x, y] in self.snake:  # body
                    char = GREEN + SNAKE_CHAR + RESET
                elif [x, y] == self.fruit:
                    char = RED + FRUIT_CHAR + RESET
                self.buffer += char + " "
            self.buffer += "│\n"

        self.buffer += " " * left_padding + "└" + "─" * (self.width *
                                                         2) + "┘\n"

        info = f"Score: {self.score}"
        self.buffer += " " * ((terminal_width - len(info)) // 2) + info + "\n"

        controls = [
            "Controls:",
            "W/↑: Up",
            "A/←: Left",
            "S/↓: Down",
            "D/→: Right",
            "Q: Quit",
        ]
        self.buffer += "\n" + "\n".join(" " * (
            (terminal_width - len(line)) // 2) + line for line in controls)

        print(self.buffer)


def get_key():
    if os.name == 'nt':  # for Windows
        import msvcrt
        return msvcrt.getch().decode('utf-8').lower()
    else:  # for Unix systems
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()


def play_game():
    game = SnakeGame()
    last_update = time.time()
    update_interval = 0.15

    print("\033[?25l", end="")  # hide cursor
    print("\033[2J", end="")  # clr screen
    print("\033[H", end="")  # move cursor to home position

    print("Snake Game")
    print("use arrow keys or WASD to control the snake")
    print("press 'Q' to quit.")
    input("Press 'Enter' to start...")

    while not game.game_over:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = get_key()
            if key == 'q':
                break
            elif key in ['w', '\x1b[A']:  # 'w' or up arrow
                if game.direction != "DOWN":
                    game.direction = "UP"
            elif key in ['s', '\x1b[B']:  # 's' or down arrow
                if game.direction != "UP":
                    game.direction = "DOWN"
            elif key in ['a', '\x1b[D']:  # 'a' or left arrow
                if game.direction != "RIGHT":
                    game.direction = "LEFT"
            elif key in ['d', '\x1b[C']:  # 'd' or right arrow
                if game.direction != "LEFT":
                    game.direction = "RIGHT"

        current_time = time.time()
        if current_time - last_update > update_interval:
            game.move_snake()
            game.draw()
            last_update = current_time

    print("\033[?25h", end="")  # show cursor
    print("Game Over")
    print(f"Final Score: {game.score}")


if __name__ == "__main__":
    play_game()
