import random
import time
import os
import shutil

class GameOfLife:
    def __init__(self):
        self.width, self.height = shutil.get_terminal_size()
        self.height -= 2  # space
        self.grid = [[random.choice([0, 1]) for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self, generation):
        output = ""
        for row in self.grid:
            output += ''.join(['■' if cell else ' ' for cell in row]) + '\n'
        output += f"Generation: {generation}".ljust(self.width) + '\n'
        output += "Press Ctrl+C to quit".ljust(self.width)
        print(output, end='')

    def get_neighbors(self, x, y):
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbors += self.grid[(x + i) % self.height][(y + j) % self.width]
        return neighbors

    def next_generation(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.get_neighbors(i, j)
                if self.grid[i][j]:
                    if neighbors in [2, 3]:
                        new_grid[i][j] = 1
                elif neighbors == 3:
                    new_grid[i][j] = 1
        self.grid = new_grid

    def is_game_over(self):
        return all(cell == 0 for row in self.grid for cell in row)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_game():
    clear_screen()
    game = GameOfLife()
    generation = 0
    try:
        while not game.is_game_over():
            clear_screen()
            game.print_grid(generation)
            game.next_generation()
            generation += 1
            time.sleep(0.1)
        print("all cells have died. simulation over")
    except KeyboardInterrupt:
        clear_screen()
        print("game stopped by user")
    
    input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    play_game()