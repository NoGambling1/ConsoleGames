import random
import time
import os
import sys
import select
import keyboard

# add msvcrt import for Windows
if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty

# const stuff
WIDTH = 30
HEIGHT = 20
SNAKE_CHAR = "■"
FRUIT_CHAR = "●"
EMPTY_CHAR = "·"

# color
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

        if (
            head[0] < 0
            or head[0] >= self.width
            or head[1] < 0
            or head[1] >= self.height
            or head in self.snake
        ):
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
        self.buffer += " " * left_padding + "┌" + "─" * (self.width * 2) + "┐\n"

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

        self.buffer += " " * left_padding + "└" + "─" * (self.width * 2) + "┘\n"

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
        self.buffer += "\n" + "\n".join(
            " " * ((terminal_width - len(line)) // 2) + line for line in controls
        )

        print(self.buffer)


def get_key(timeout=0.1):
    start_time = time.time()
    while True:
        if keyboard.is_pressed("q"):  # Assuming 'Q' is uppercase
            return "QUIT"
        elif keyboard.is_pressed("w") or keyboard.is_pressed("up"):
            return "UP"
        elif keyboard.is_pressed("s") or keyboard.is_pressed("down"):
            return "DOWN"
        elif keyboard.is_pressed("a") or keyboard.is_pressed("left"):
            return "LEFT"
        elif keyboard.is_pressed("d") or keyboard.is_pressed("right"):
            return "RIGHT"
        if time.time() - start_time > timeout:
            return None


def play_game():
    game = SnakeGame()
    last_update = time.time()
    update_interval = 0.15
    key_queue = []  # Initialize an empty list to hold queued keys

    print("\033[?25l", end="")  # Hide cursor
    print("\033[2J", end="")  # Clear screen
    print("\033[H", end="")  # Move cursor to home position

    print("Snake Game")
    print("Use arrow keys or WASD to control the snake.")
    print("Press 'Q' to quit.")
    input("Press 'Enter' to start...")

    while not game.game_over:
        key = get_key()
        if key == "Q":
            break
        elif key in ["UP", "DOWN", "LEFT", "RIGHT", "W", "A", "S", "D"]:
            key_queue.append(key)  # Add the key to the queue

        # Process the queue every frame
        while key_queue:
            current_key = key_queue.pop(
                0
            )  # Remove and return the first item from the queue
            if current_key in ["W", "UP"] and (game.direction != "DOWN"):
                game.direction = "UP"
            elif current_key in ["S", "DOWN"] and game.direction != "UP":
                game.direction = "DOWN"
            elif current_key in ["A", "LEFT"] and game.direction != "RIGHT":
                game.direction = "LEFT"
            elif current_key in ["D", "RIGHT"] and game.direction != "LEFT":
                game.direction = "RIGHT"

        current_time = time.time()
        if current_time - last_update > update_interval:
            game.move_snake()
            game.draw()
            last_update = current_time

    print("\033[?25h", end="")  # Show cursor
    print("Game Over")
    print(f"Final Score: {game.score}")
    #input("Press 'Enter' to return to the main menu...")
   # if __name__ == "__main__":
    #play_game()