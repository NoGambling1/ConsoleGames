import random
import time
import os
import sys
import select

# add an if statement to see if windows or not, if not then use unix
if os.name == 'nt':
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
    """
    core game logic for the game
    
    attributes:
        width (int): the width of the game grid.
        height (int): the height of the game grid.
        snake (List[List[int]]): current state of the snake, represented by coords in a list
        direction (str): current direction the snake is moving 
        fruit (List[int]): current pos of the fruit on the grid
        score (int): current score
        game_over (bool): game over bool to tell if game over (ofc)
        
    methods:
        spawn_fruit(): generates a new fruit at a random location within the game grid
        move_snake(): moves the snake according to its current direction and checks for collisions
        draw(): responsible for terminal screen state
    """

    def __init__(self):
        """init a new instance of game."""
        self.width = WIDTH
        self.height = HEIGHT
        self.snake = [[4, 5], [3, 5], [2, 5]]
        self.direction = "RIGHT"
        self.fruit = self.spawn_fruit()
        self.score = 0
        self.game_over = False

    def spawn_fruit(self):
        """generate a new fruit at a random location within the game grid."""
        while True:
            pos = [
                random.randint(0, self.width - 1),
                random.randint(0, self.height - 1),
            ]
            if pos not in self.snake:
                return pos

    def move_snake(self):
        """moves the snake according to its current direction and checks for collisions."""
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
        """clear terminal screen and draws current game state"""
        os.system('cls' if os.name == 'nt' else 'clear')
        terminal_width = os.get_terminal_size().columns
        left_padding = (terminal_width - (self.width * 2 + 2)) // 2

        print("\n" * 2)  # automatic padding for all terminals
        print(" " * left_padding + "┌" + "─" * (self.width * 2) + "┐")

        for y in range(self.height):
            print(" " * left_padding + "│", end="")
            for x in range(self.width):
                char = EMPTY_CHAR
                if [x, y] == self.snake[0]:  # head
                    char = GREEN + SNAKE_CHAR + RESET
                elif [x, y] in self.snake:  # body
                    char = GREEN + SNAKE_CHAR + RESET
                elif [x, y] == self.fruit: 
                    char = RED + FRUIT_CHAR + RESET
                print(char, end=" ")
            print("│")

        print(" " * left_padding + "└" + "─" * (self.width * 2) + "┘")

        info = f"Score: {self.score}"
        print(" " * ((terminal_width - len(info)) // 2) + info)

        controls = [
            "Controls:",
            "W/↑: Up",
            "A/←: Left",
            "S/↓: Down",
            "D/→: Right",
            "Q: Quit",
        ]
        print(
            "\n"
            + "\n".join(
                " " * ((terminal_width - len(line)) // 2) + line for line in controls
            )
        )

def get_key(timeout=0.1):
    """
    wait for key press and returns the direction
    
    arguments:
        timeout (float): the max time to wait for a key press IN SECONDS NOT MS
    
    returns:
        str: direction corresponding to the pressed key or none if no key was pressed within the timeout period
    """
    if os.name == "nt":  # for Windows
        start_time = time.time()
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\xe0':  # special keys (arrows, function keys, etc.)
                    key = msvcrt.getch()
                    return {b'H': 'UP', b'P': 'DOWN', b'K': 'LEFT', b'M': 'RIGHT'}.get(key)
                return key.decode('utf-8').upper()
            if time.time() - start_time > timeout:
                return None
    else:  # for Unix systems (Linux, macOS)
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if rlist:
                key = sys.stdin.read(1)
                if key == '\x1b':  # Special key prefix
                    key += sys.stdin.read(2)
                    return {'[A': 'UP', '[B': 'DOWN', '[D': 'LEFT', '[C': 'RIGHT'}.get(key[1:])
                return key.upper()
            else:
                return None
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def play_game():
    """
    game loop
    """
    game = SnakeGame()
    last_update = time.time()
    update_interval = 0.15

    print("Snake Game")
    print("Use arrow keys or WASD to control the snake.")
    print("Press 'Q' to quit.")
    input("Press 'Enter' to start...")

    while not game.game_over:
        key = get_key()
        if key == "Q":
            break
        elif key in ["UP", "DOWN", "LEFT", "RIGHT", "W", "A", "S", "D"]:
            if key in ["W", "UP"] and game.direction != "DOWN":
                game.direction = "UP"
            elif key in ["S", "DOWN"] and game.direction != "UP":
                game.direction = "DOWN"
            elif key in ["A", "LEFT"] and game.direction != "RIGHT":
                game.direction = "LEFT"
            elif key in ["D", "RIGHT"] and game.direction != "LEFT":
                game.direction = "RIGHT"

        current_time = time.time()
        if current_time - last_update > update_interval:
            game.move_snake()
            game.draw()
            last_update = current_time

    print("Game Over")
    print(f"Final Score: {game.score}")
    input("Press 'Enter' to return to the main menu...")

if __name__ == "__main__":
    play_game()