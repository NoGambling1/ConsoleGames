# Tetris Game Documentation

## Module Overview
this module implements a console-based version of tetris. it has colored pieces, a guideline grid, score tracking, and leveling

## Dependencies
- random
- time
- os
- sys
- keyboard

## Constants
- `WIDTH`: game board width (10)
- `HEIGHT`: game board height (20)
- `EMPTY`: character for empty cells (' ')
- `BLOCK`: character for filled cells ('█')
- `GUIDE`: character for guideline grid ('·')
- `SHAPES`: lidt of tetromino shapes
- `COLORS`: list of ANSI color codes for tetrominoes
- `RESET_COLOR`: ANSI code to reset text color
- `GUIDE_COLOR`: ANSI code for guideline grid color

## Classes

### Tetromino
repredents a single Tetris piece.

#### Attributes
- `x` (int): x-coordinate of the tetromino
- `y` (int): y-coordinate of the tetromino
- `shape` (List[List[int]]): shape of the tetromino
- `color` (str): ANSI color code for the tetromino

#### Methods
- `__init__(self, x, y, shape, color)`: init a new tetromino
- `move(self, dx, dy)`: move the tetromino by given deltas
- `rotate(self)`: rotate the tetromino 90 degrees clockwise

### TetrisGame
manages the game logic and state.

#### Attributes
- `board` (List[List[str]]): game board
- `score` (int): current score
- `level` (int): current level
- `lines_cleared` (int): total number of lines cleared
- `current_piece` (Tetromino): current falling piece
- `next_piece` (Tetromino): next piece to fall
- `game_over` (bool): game over flag

#### Methods
- `__init__(self)`: init a new game
- `new_piece(self)`: genetated a new random tetromino
- `valid_move(self, piece, dx=0, dy=0)`: check if a move is valid
- `place_piece(self, piece)`: place a piece on the board
- `remove_completed_lines(self)`: rm completed lines and return the number cleared
- `update_score(self, lines_cleared)`: update the score based on lines cleared
- `move_piece(self, dx, dy)`: move the current piece if possible
- `rotate_piece(self)`: rotate the current piece if possible
- `drop_piece(self)`: hard drop the current piece
- `step(self)`: perform a game step (move piece down or place new piece)
- `draw(self)`: draw the current game state

## Functions

### get_input(timeout=0.1)
wait for a key press and return the corresponding action

#### Parameters
- `timeout` (float): max time to wait for a key press in seconds

#### Returns
- `str`: action mapped to the key pressed, or 'None' if no key was pressed

### play_game()
main game loop function.

## Usage
to play a tetris game, select it from the main menu screen. the game will display in the console with the following controls:
- A/←: move left
- D/→: move right
- S/↓: soft drop
- W/↑: rotate
- Space: hard drop
- Q: quit

## Game Features
- colored tetrominoes
- guidelines on the grid for easier piece placement
- score tracking and level progression
- next piece preview
- increasing difficulty (faster piece falling speed) as levels increase

## Notes
- the game uses ANSI color codes for display, which may not work in all console environments
- the input handling is designed to work on both Windows and Unix-based systems
- thr game speed increases with each level

## Customization
the game can be customized by modifying the constants at the beginning of the script, such as board size, shapes, and colors