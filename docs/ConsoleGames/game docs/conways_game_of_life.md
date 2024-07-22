# Unofficial Conway's Game of Life Documentation

## Module Overview
this module implements a console-based version of Conway's classic Game of Life. it provides a visual representation of the cellular automaton, with the grid size adjusting to the terminal dimensions automagically

## Dependencies
- random
- time
- os
- shutil

## Classes

### GameOfLife
managess the game state and logic for Conway's Game of Life

#### Attributes
- `width` (int): width of the game grid (based on terminal width)
- `height` (int): height of the game grid (based on terminal height minus 2)
- `grid` (List[List[int]]): 2D list representing the game grid

#### Methods
- `__init__(self)`: init a new Game of Life with a random initial state
- `print_grid(self, generation)`: display the current grid state and generation count
- `get_neighbors(self, x, y)`: count the number of live neighbors for a given cell
- `next_generation(self)`: compute the next generation of the grid
- `is_game_over(self)`: check if all cells have died

## Functions

### clear_screen()
clr the console screen for a clean display.

### play_game()
the main game loop function that manages the game flow and user interaction

## Usage
to start Conway's Game of Life, select this game from the `main.py` title screen. the game will automatically:
1. init a random grid based on the terminal size
2. display the evolving grid state
3. update the grid state each generation
4. continue until all cells die or the user interrupts the game

## Game Features
- dynamic grid size based on terminal dimensions
- visual representation of live cells using '■' character
- generation counter display
- automatic progression of generations
- game over detection when all cells die

## Input Handling
- the game runs automatically without requiring user input for each generation
- the user can stop the game at any time by pressing `Ctrl+C`

## Notes
- the game uses the terminal dimensions to set the grid size, ensuring it fits different console environments
- the initial state is randomly generated, providing a unique starting point each time the game is run
- the game implements "wrapping" at the edges

## Customization
the game can be customized by modifying:
- the sleep time between generations (currently set to 0.1 seconds)
- the character used to represent live cells (currently '■')
- the logic for the init random state generation
