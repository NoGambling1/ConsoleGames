# ConsoleGames Main File Documentation

## Module Overview
this module serves as the main entry point for the collection of currently added games. it provides a user interface for selecting and playing various games, viewing credits, sys info, and interacting with an AI chat feature (not added right now)

## Dependencies
- time
- os
- random
- platform
- datetime
- ai.ai_chat (custom module for AI interaction)

## Functions

### clear_screen()
clears the console screen, providing a clean interface for the user

### print_animated_title()
display an animated ASCII art title with colored text

### print_main_menu()
prints the main menu options for the user to choose from

### print_games_menu(games)
prints the menu of available games for the user to select

#### Parameters
- `games` (list): a list of dictionaries containing game information

### play_game(game_module)
imports and runs the selected game module

#### Parameters
- `game_module` (dict): a dictionary containing the game's name and file name

### view_credits()
displays the credits for the project

### system_info()
shows system information including OS, py version, and current date/time

### main()
the main function that runs the game selection loop and manages user interactions

## Usage
to start the main terminal app, run this script. (`python main.py` or `sudo python main.py`). the main menu will be displayed, allowing the user to:

1. view and select games to play
2. view credits
3. check system information
4. talk to an AI (when added)
5. quit the application

### Available Games
the current list of available games includes:
- Tic-Tac-Toe
- Checkers
- Tetris
- Snake
- Sudoku
- Conway's Game of Life

## Game Integration
to add new games to the collection:
1. create a new Python file for the game in the same directory
2. implement a `play_game()` function in the new game file
3. add the game information to the `games` list in the `main()` function

## Customization
the animated title, credit information, and available games can be easily modified within the script to update or expand the collection

> [!NOTE]  
>ensure that all game modules and the AI chat module (`ai.ai_chat`) are present in the correct directories for >the script to function properly