import os

def clear_screen():
    """clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu(games):
    """print the main menu with the list of currently available games."""
    print("welcome to console games!")
    print("select a game to play:")
    for index, game in enumerate(games, 1):
        print(f"{index}. {game['name']}")
    print(f"{len(games) + 1}. Quit")

def play_game(game_module):
    """import and play the selected game."""
    clear_screen()
    print(f"Starting {game_module['name']}...")
    game = __import__(game_module['file'])
    game.play_game()
    input("press 'Enter' to return to the main menu...")

def main():
    # list of available games
    # <!> to add a new game, append a dictionary with 'name' and 'file' keys to this list <!>
    games = [
        {'name': 'tic-tac-toe', 'file': 'tic-tac-toe'},
        {'name': 'checkers', 'file': 'checkers'},
        {'name': 'tetris', 'file': 'tetris'}
    ]

    while True:
        clear_screen()
        print_menu(games)
        choice = input(f"which game would you like to play?(1-{len(games) + 1}): ")
        
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(games):
                play_game(games[choice - 1])
            elif choice == len(games) + 1:
                print("thanks for playing! ILY <3 - orangejuiceplz")
                break
            else:
                print("not a valid choice. try again?")
                input("press 'Enter' to continue...")
        else:
            print("not a valid input. please enter a number.")
            input("press 'Enter' to continue...")

if __name__ == "__main__":
    main()