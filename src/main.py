import time
import os
import random
import platform
from ai.ai_chat import talk_to_ai
from datetime import datetime

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_animated_title():
    """Print an animated title for Console Games."""
    title = """
     ____                      _        ____                       
    / ___|___  _ __  ___  ___ | | ___  / ___| __ _ _ __ ___   ___  ___
   | |   / _ \| '_ \/ __|/ _ \| |/ _ \| |  _ / _` | '_ ` _ \ / _ \/ __|
   | |__| (_) | | | \__ \ (_) | |  __/| |_| | (_| | | | | | |  __/\__ \\
    \____\___/|_| |_|___/\___/|_|\___| \____|\__,_|_| |_| |_|\___||___/
    """
    
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
    reset = '\033[0m'
    
    for line in title.split('\n'):
        colored_line = ''.join(random.choice(colors) + char + reset for char in line)
        print(colored_line)
        time.sleep(0.1)

def print_main_menu():
    """Print the main menu options.""" # update
    print("\nMAIN MENU:")
    print("1. View Games")
    print("2. View Credits")
    print("3. System Information")
    print("4. Talk to AI")
    print("5. Quit")

def print_games_menu(games):
    """Print the games menu with the list of currently available games."""
    print("\nAVAILABLE GAMES:")
    for index, game in enumerate(games, 1):
        print(f"{index}. {game['name']}")
    print(f"{len(games) + 1}. Return to Main Menu")

def play_game(game_module):
    """Import and play the selected game."""
    clear_screen()
    print(f"Starting {game_module['name']}...")
    game = __import__(game_module['file'])
    game.play_game()
    input("press 'Enter' to return to the main menu...")

def view_credits():
    """Display the credits."""
    clear_screen()
    print("CREDITS:")
    print("Console Games created w/ love by NoGambling && orangejuiceplz <3")
    print("thanks for playing! ILY <3")
    input("\npress 'Enter' to return to the main menu...")

def system_info():
    """Display system information and current date/time."""
    clear_screen()
    print("SYSTEM INFORMATION:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"PY Version: {platform.python_version()}")
    input("\npress 'Enter' to return to the main menu...")

def main():
    games = [
        {'name': 'Tic-Tac-Toe', 'file': 'tic-tac-toe'},
        {'name': 'Checkers', 'file': 'checkers'},
        {'name': 'Tetris', 'file': 'tetris'},
        {'name': 'Snake', 'file': 'snake'},
        {'name': 'sudoku', 'file': 'sudoku'}
    ]

    while True:
        clear_screen()
        print_animated_title()
        print_main_menu()
        
        choice = input("\nwhich option would you like to select? (1-5): ")
        if choice == '1':
            while True:
                clear_screen()
                print_animated_title()
                print_games_menu(games)
                game_choice = input(f"\nwhich game would you like to play? (1-{len(games) + 1}): ")
                if game_choice.isdigit():
                    game_choice = int(game_choice)
                    if 1 <= game_choice <= len(games):
                        play_game(games[game_choice - 1])
                    elif game_choice == len(games) + 1:
                        break
                    else:
                        print("not a valid choice. try again?")
                        time.sleep(1)
                else:
                    print("not a valid input. please enter a number.")
                    time.sleep(1)
        elif choice == '2':
            view_credits()
        elif choice == '3':
            system_info()
        elif choice == '4':
            talk_to_ai()
        elif choice == '5':
            print("\nthanks for playing! ILY <3 - orangejuiceplz")
            time.sleep(2)
            break
        else:
            print("not a valid choice. try again?")
            time.sleep(1)

if __name__ == "__main__":
    main()