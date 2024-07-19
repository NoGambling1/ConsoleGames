# Checkers Game Official Documentation

## Module Overview
this module implements a cli version of checkers. it uses the `colorama` library for colored output in the terminal

## Dependencies needed
- colorama

## Functions

### play_game()
the main function to play a game of Checkers. this is what the main file calls when user selects checkers from the menu

#### Description
initializes the game board, manages player turns, and handles the main game loop

### create_board(board, hee)
draws the current state of the game board

#### Parameters
- `board` (list): the current game board state
- `hee` (int): the index of the last moved piece to highlight

### cord_to_num(coordinate)
converts a board coordinate (e.g., 'A4') to its corresponding index in the board list

#### Parameters
- `coordinate` (str): a string representing a board position (e.g., 'A4')

#### Returns
- int: the index in the board list corresponding to the given coordinate

### add_move(move)
process a player's move, updating the board state relative to the move

#### Parameters
- `move` (str): a string representing the move (e.g., 'A3-B4')

### get_valid_move()
prompts the user for a valid move input

#### Returns
- str: a valid move string or `None` if the user chooses to quit

### count_valid_moves(player_piece)
counts the number of valid moves available for a given player

#### Parameters
- `player_piece` (str): the piece type of the player, either: ('O' or 'X')

#### Returns
- int: the number of valid moves available

### check_win_condition(player_piece)
checks if the current board state represents a win for the given player

#### Parameters
- `player_piece` (str): the piece type of the player to check for a win ('O' or 'X')

#### Returns
- bool: `True` if the player has won, `False` otherwise

## Usage
to start the game, run main.py and select the game. follow the prompts to make moves. moves should be entered in the format 'A3-B4', where the first part represents the starting position of a piece and the second part represents its final destination (HA, I GOT ONE! - <3 orangejuiceplz)

## Game Rules
- players take turns moving their pieces diagonally forward
- pieces can capture opponent pieces by jumping over them
- when a piece reaches the opposite end of the board, it becomes a king and can move backwards
- the game ends when one player captures all of the opponent's pieces or when no more moves are possible

## Customization
the game board size and initial piece placement can be modified by changing the `board` initialization in the `play_game()` function. you shouldn't really touch this as it automatically scales with your terminal size