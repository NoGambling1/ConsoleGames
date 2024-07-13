from colorama import init as colorama_init

from colorama import Fore, Back, Style

colorama_init()


def play_game():
    """main function to play checkers."""
    board = (
        [" O ", "  "] * 4
        + ["  ", " O "] * 4
        + [" O ", "  "] * 4
        + ["  "] * 16
        + ["  ", " X "] * 4
        + [" X ", "  "] * 4
        + ["  ", " X "] * 4
    )

    def create_board(board):
        print("\n" + Fore.YELLOW + "welcome to checkers!" + Style.RESET_ALL)
        print(Fore.CYAN + "\ncurrent board:" + Style.RESET_ALL)
        for count in range(8):
            print(Fore.CYAN + f"{count+1} |", end="  " + Style.RESET_ALL)

            for newCount in range(8):
                spot = (count * 8) + newCount
                if board[spot] == " O ":
                    print(
                        Back.WHITE
                        + Fore.RED
                        + "["
                        + board[spot]
                        + "]"
                        + Style.RESET_ALL,
                        end=" ",
                    )
                elif board[spot] == " X ":
                    print(
                        Back.WHITE
                        + Fore.BLACK
                        + "["
                        + board[spot]
                        + "]"
                        + Style.RESET_ALL,
                        end=" ",
                    )
                else:
                    print(
                        Back.WHITE + "[" + board[spot] + "]" + Style.RESET_ALL, end=" "
                    )

            print("\n  |  ")
        print("   ----------------------------------------------")
        print("      A     B    C     D     E    F    G     H")

    def cord_to_num(coordinate):
        coord_arr = list(coordinate.lower())
        return (int(coord_arr[1]) - 1) * 8 + (ord(coord_arr[0]) - 97)

    def add_move(move):
        move_from, move_to = move.split("-")
        from_num = cord_to_num(move_from)
        to_num = cord_to_num(move_to)

        piece = board[from_num]
        board[from_num] = "  "
        board[to_num] = piece

        # capture logic (VERY SIMPLE) -- todo: doesn't have multiple capture
        if abs(from_num - to_num) > 9:  # if it's a capture move
            captured_pos = (from_num + to_num) // 2
            board[captured_pos] = "  "

    def get_valid_move():
        while True:
            move = input(
                Fore.GREEN
                + "\enter your move (for example, A3-B4) or 'q' to quit: "
                + Style.RESET_ALL
            )
            if move.lower() == "q":
                return None
            if (
                len(move) == 5
                and move[2] == "-"
                and move[0].isalpha()
                and move[3].isalpha()
                and move[1].isdigit()
                and move[4].isdigit()
            ):
                return move
            print(
                Fore.RED
                + "invalid move format. please use the format 'A3-B4' to play a move."
                + Style.RESET_ALL
            )

    # Main game loop
    while True:
        create_board(board)
        move = get_valid_move()
        if move is None:
            break
        add_move(move)

    print(Fore.YELLOW + "\nthanks for playing checkers!" + Style.RESET_ALL)


if __name__ == "__main__":
    play_game()
