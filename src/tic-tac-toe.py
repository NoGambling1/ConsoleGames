from time import sleep

from colorama import init, Fore

init()


def play_game():
    """Main function to play Tic-Tac-Toe."""
    game_array = [" "] * 9

    user1 = ""

    user2 = ""

    def add_move(spot, user):

        game_array[spot - 1] = user

    def check_win(user):
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],  # rows
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],  # columns
            [0, 4, 8],
            [2, 4, 6],  # diag lines
        ]

        for combo in winning_combinations:

            if all(game_array[i] == user for i in combo):

                return f"user ({'1' if user == user1 else '2'}) ({user}) won the game!"

        return None

    def get_available_spots():

        return [i + 1 for i, val in enumerate(game_array) if val == " "]

    def build_full_board():

        for i in range(0, 9, 3):

            print(
                Fore.GREEN + " ".join(f"[{game_array[j]}]" for j in range(i, i + 3)),
                end="",
            )

            print(Fore.BLUE + " | ", end="")

            print(
                Fore.RED
                + " ".join(
                    f"[{j+1 if game_array[j] == ' ' else ' '}]" for j in range(i, i + 3)
                )
            )

        print()

    def get_valid_input(player):

        while True:

            try:
                pos = int(
                    input(
                        f"which spot would you like to go, User {player} ({user1 if player == 1 else user2})? "
                    )
                )

                if pos not in get_available_spots():

                    print("that spot is not available. Please try again.")

                else:
                    return pos
            except ValueError:
                print("please enter a valid number.")

    print("welcome to Tic-Tac-Toe, Shitty NoGambling (and orangejuiceplz) edition!")

    sleep(1)

    while True:
        user1 = input("is user 1 'x' or '-'? ").lower()

        if user1 in ["x", "-"]:

            user2 = "-" if user1 == "x" else "x"

            break
        print("thats not a valid input, please try again.")

    print(f"User 1 is playing {user1}, while User 2 is playing {user2}")

    sleep(0.5)

    for turn in range(9):

        build_full_board()

        print(Fore.CYAN + "--------------------------" + Fore.RESET)

        sleep(0.5)

        current_player = 1 if turn % 2 == 0 else 2

        current_user = user1 if current_player == 1 else user2

        pos = get_valid_input(current_player)

        add_move(pos, current_user)

        sleep(0.3)

        result = check_win(current_user)

        if result:

            build_full_board()

            print(Fore.MAGENTA + result)

            break

        if turn == 8:  # draw

            build_full_board()

            print(Fore.YELLOW + "the game ended in a draw, dipshits.")


if __name__ == "__main__":
    play_game()
