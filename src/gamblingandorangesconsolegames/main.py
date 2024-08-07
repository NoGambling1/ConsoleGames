import time
import os
import random
from system_info import display_system_info
from ai.ai_chat import talk_to_ai
from games import checkers, chess, conways_game_of_life, pacman, snake, solitare, sudoku, tetris, tic_tac_toe
from calc.calculator import calculate

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_animated_title():
    """Print an animated title for Console Games."""
    title = r"""
     ____                      _        ____                       
    / ___|___  _ __  ___  ___ | | ___  / ___| __ _ _ __ ___   ___  ___
   | |   / _ \| '_ \/ __|/ _ \| |/ _ \| |  _ / _` | '_ ` _ \ / _ \/ __|
   | |__| (_) | | | \__ \ (_) | |  __/| |_| | (_| | | | | | |  __/\__ \
    \____\___/|_| |_|___/\___/|_|\___| \____|\__,_|_| |_| |_|\___||___/
    """

    colors = [
        '\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m'
    ]
    reset = '\033[0m'

    for line in title.split('\n'):
        colored_line = ''.join(
            random.choice(colors) + char + reset for char in line)
        print(colored_line)
        time.sleep(0.1)

def print_main_menu():
    """Print the main menu options."""
    print("\nMAIN MENU:")
    print("1. View Games")
    print("2. View Credits")
    print("3. System Information")
    print("4. AI chat")
    print("5. Calculator")
    print("6. Quit")

def print_games_menu(games):
    """Print the games menu with the list of currently available games."""
    print("\nAVAILABLE GAMES:")
    for index, game in enumerate(games, 1):
        print(f"{index}. {game['name']}")
    print(f"{len(games) + 1}. Return to Main Menu")

def play_game(game_module):
    """Play the selected game."""
    clear_screen()
    print(f"Starting {game_module['name']}...")
    game_module['module'].play_game()
    input("Press 'Enter' to return to the main menu...")

def view_credits():
    """Display the credits."""
    clear_screen()
    print("CREDITS:")
    print("Console Games created w/ love by NoGambling && orangejuiceplz <3")
    print("Thanks for playing! ILY <3")
    input("\nPress 'Enter' to return to the main menu...")

def system_info():
    """Display system information and current date/time."""
    clear_screen()
    display_system_info()
    input("\nPress 'Enter' to return to the main menu...")

def main():
    games = [
        {'name': 'Tic-Tac-Toe', 'module': tic_tac_toe},
        {'name': 'Checkers', 'module': checkers},
        {'name': 'Chess', 'module': chess},
        {'name': 'Tetris', 'module': tetris},
        {'name': 'Snake', 'module': snake},
        {'name': 'Sudoku', 'module': sudoku},
        {'name': 'Game of Life', 'module': conways_game_of_life},
        {'name': 'Pacman', 'module': pacman},
        {'name': 'Solitaire', 'module': solitare},
    ]

    while True:
        clear_screen()
        print_animated_title()
        print_main_menu()

        choice = input("\nWhich option would you like to select? (1-6): ")
        if choice == '1':
            while True:
                clear_screen()
                print_animated_title()
                print_games_menu(games)
                game_choice = input(f"\nWhich game would you like to play? (1-{len(games) + 1}): ")
                if game_choice.isdigit():
                    game_choice = int(game_choice)
                    if 1 <= game_choice <= len(games):
                        play_game(games[game_choice - 1])
                    elif game_choice == len(games) + 1:
                        break
                    else:
                        print("Not a valid choice. Try again?")
                        time.sleep(1)
                else:
                    print("Not a valid input. Please enter a number.")
                    time.sleep(1)
        elif choice == '2':
            view_credits()
        elif choice == '3':
            system_info()
        elif choice == '4':
            talk_to_ai()
        elif choice == '5':
            calculate()
        elif choice == '6':
            print("\nThanks for playing! ILY <3 - orangejuiceplz")
            time.sleep(2)
            break
        else:
            print("Not a valid choice. Try again?")
            time.sleep(1)

if __name__ == "__main__":
    main()